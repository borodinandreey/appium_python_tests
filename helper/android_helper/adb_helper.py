import subprocess
import re
import json
import allure
import logging
import time
from data.base_data import DOMAIN_FILTER


class AdbHelper:

    @staticmethod
    @allure.step("Очистка логов")
    def clear_log(timeout=5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            subprocess.run(["adb", "logcat", "-c"], check=True)

            result = subprocess.run(
                ["adb", "logcat", "-d"],
                capture_output=True,
                text=True
            )
            output = result.stdout.strip()

            lines = output.splitlines()
            suspicious_line = [line for line in lines if line.startswith(DOMAIN_FILTER)]

            if not suspicious_line:
                return
            time.sleep(0.5)

        raise RuntimeError(f"Не удалось очистить логи по фильтру {DOMAIN_FILTER} за {timeout} секунд")

    @staticmethod
    @allure.step("Получение запросов")
    def get_requests():
        try:
            logs = subprocess.check_output(["adb", "logcat", "-d"]).decode("utf-8")
            request_pattern = r'http[s]?://[^\s"]+'
            captured_requests = re.findall(request_pattern, logs)
            captured_requests = list(set(captured_requests))

            result = []
            for url in captured_requests:
                if DOMAIN_FILTER in url:
                    result.append(url)
            return result
        except subprocess.CalledProcessError as e:
            return []

    @staticmethod
    @allure.step("Получение тела ответа")
    def get_responses_from_adb_logs(index=None):
        try:
            all_logs = subprocess.check_output(["adb", "logcat", "-d"], encoding="utf-8")
            lines = all_logs.splitlines()

            relevant_lines = [line for line in lines if "okhttp.OkHttpClient" in line]

            responses = []
            json_buffer = []
            in_json = False

            for line in relevant_lines:
                parts = line.split("okhttp.OkHttpClient:", 1)
                if len(parts) < 2:
                    continue
                stripped_line = parts[-1].strip()

                if not in_json:
                    if stripped_line.startswith("{") or stripped_line.startswith("["):
                        in_json = True
                        json_buffer = [stripped_line]
                else:
                    json_buffer.append(stripped_line)

                if in_json and (stripped_line.endswith("}") or stripped_line.endswith("]")):
                    full_json = "\n".join(json_buffer)
                    full_json_sanitized = re.sub(r'(?<!\\)\n', '', full_json)

                    try:
                        parsed = json.loads(full_json_sanitized)
                        responses.append(parsed)
                    except json.JSONDecodeError as e:
                        raise AssertionError(
                            f"Не удалось распарсить JSON-ответ! Причина: {e}\n"
                        )
                    finally:
                        in_json = False
                        json_buffer = []

            if in_json and json_buffer:
                full_json = "\n".join(json_buffer)
                full_json_sanitized = re.sub(r'(?<!\\)\n', '', full_json)
                try:
                    parsed = json.loads(full_json_sanitized)
                    responses.append(parsed)
                except json.JSONDecodeError as e:
                    raise AssertionError(
                        f"Не удалось распарсить JSON-ответ (висячий буфер)! Причина: {e}\n"
                    )

            for i, response in enumerate(responses, start=1):
                if isinstance(response, dict) and "data" in response:
                    data_field = response["data"]
                    if isinstance(data_field, list) and len(data_field) == 0:
                        logging.info(f"Ответ #{i}: поле 'data' пустое.")

                allure.attach(
                    json.dumps(response, indent=4, ensure_ascii=False),
                    name=f"Extracted JSON Response #{i}",
                    attachment_type=allure.attachment_type.JSON
                )

            if index is None:
                return responses

            if not 0 <= index < len(responses):
                raise IndexError(
                    f"Запрошенный индекс {index} выходит за пределы списка JSON-ответов. "
                    f"Доступные индексы: 0..{len(responses) - 1}."
                )

            return responses[index]

        except subprocess.CalledProcessError as e:
            raise AssertionError(f"Не удалось выполнить команду ADB! Причина: {e}")
