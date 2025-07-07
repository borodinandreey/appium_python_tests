import allure
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver, timeout=2):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=timeout)

    @allure.step("Ожидание элемента")
    def wait_element(self, locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException as e:
            raise TimeoutException(f"Не удалось найти элемент с локатором {locator}")

    @allure.step("Клик на элемент")
    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException as e:
            raise TimeoutException(f"Не удалось кликнуть на элемент с локатором {locator}: {e}")

    @allure.step("Клик на вложенный элемент")
    def click_nested_element(self, main_locator, nested_locator, index=0):
        try:
            parent_element = self.driver.find_element(*main_locator)
        except NoSuchElementException as e:
            raise NoSuchElementException(f"Не удалось найти родительский элемент с локатором {main_locator}: {e}")

        nested_elements = parent_element.find_elements(*nested_locator)

        if not nested_elements:
            raise AssertionError(f"Не удалось найти ни один вложенный элемент с локатором {nested_locator} внутри {main_locator}")
        if index >= len(nested_elements) or index < 0:
            raise AssertionError(f"Запрошенный индекс: {index} выходит за границы списка вложенных элементов")

        try:
            nested_elements[index].click()
        except TimeoutException as e:
            raise TimeoutException(f"Не удалось кликнуть на вложенный элемент с локатором {nested_locator}: {e}")

    @allure.step("Ввод текста в поле")
    def enter_text(self, locator, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.send_keys(text)
        except TimeoutException as e:
            raise TimeoutException(f"Не удалось ввести текст в поле с локатором: {locator}: {e}")

    @allure.step("Получение текста элемента")
    def get_text(self, locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.text
        except TimeoutException as e:
            raise TimeoutException(f"Не удалось получить текст элемента с локатором {locator}: {e}")

    @allure.step("Получение текста вложенного элемента")
    def get_nested_text(self, main_locator, nested_locator, index=0):
        try:
            parent_element = self.driver.find_element(*main_locator)
        except NoSuchElementException as e:
            raise NoSuchElementException(f"Не удалось найти родительский элемент с локатором {main_locator}: {e}")

        nested_elements = parent_element.find_elements(*nested_locator)

        if not nested_elements:
            raise AssertionError(f"Не удалось найти ни один вложенный элемент с локатором {nested_locator} внутри {main_locator}")
        if index >= len(nested_elements) or index < 0:
            raise AssertionError(f"Запрошенный индекс: {index} выходит за границы списка вложенных элементов")

        try:
            return nested_elements[index].text
        except TimeoutException as e:
            raise TimeoutException(f"Не удалось получить текст вложенного элемента с локатором {nested_locator}: {e}")

    @allure.step("Свайп экрана")
    def swipe_screen(self, direction, start_x=0.5, start_y=0.5, end_x=0.5, end_y=0.5, duration=700):
        try:
            window_size = self.driver.get_window_size()
            width = window_size["width"]
            height = window_size["height"]

            start_x_abs = int(width * start_x)
            start_y_abs = int(height * start_y)
            end_x_abs = int(width * end_x)
            end_y_abs = int(height * end_y)

            if direction == "down":
                self.driver.swipe(start_x_abs, start_y_abs, end_x_abs, end_y_abs, duration)
            elif direction == "up":
                self.driver.swipe(start_x_abs, end_y_abs, end_x_abs, start_y_abs, duration)
            elif direction == "left":
                self.driver.swipe(start_x_abs, start_y_abs, end_x_abs, start_y_abs, duration)
            elif direction == "right":
                self.driver.swipe(end_x_abs, start_y_abs, start_x_abs, start_y_abs, duration)
            else:
                raise ValueError("Неправильное направление, используй 'down', 'up', 'left', 'right'")
        except Exception as e:
            raise Exception(f"Ошибка при свайпе экране: {e}")

    @allure.step("Свайп экрана до элемента")
    def swipe_screen_to_element(self, direction, start_x=0.5, start_y=0.5, end_x=0.5, end_y=0.5, duration=700, locator=None, max_swipes=15):
        try:
            window_size = self.driver.get_window_size()
            width = window_size["width"]
            height = window_size["height"]

            start_x_abs = int(width * start_x)
            start_y_abs = int(height * start_y)
            end_x_abs = int(width * end_x)
            end_y_abs = int(height * end_y)

            swipe_count = 0

            while swipe_count < max_swipes:
                element = self.wait.until(EC.visibility_of_element_located(locator))
                if element:
                    return element

                if direction == "down":
                    self.driver.swipe(start_x_abs, start_y_abs, end_x_abs, end_y_abs, duration)
                elif direction == "up":
                    self.driver.swipe(start_x_abs, end_y_abs, end_x_abs, start_y_abs, duration)
                elif direction == "left":
                    self.driver.swipe(start_x_abs, start_y_abs, end_x_abs, start_y_abs, duration)
                elif direction == "right":
                    self.driver.swipe(end_x_abs, start_y_abs, start_x_abs, start_y_abs, duration)
                else:
                    raise ValueError("Неправильное направление, используй 'down', 'up', 'left', 'right'")

                swipe_count += 1

            raise Exception(f"Элемент с локатором {locator} не найден за {max_swipes} свайпов")

        except Exception as e:
            raise Exception(f"Ошибка при свайпе экране: {e}")

    def swipe_element(self, element, direction, start_percentage=0.0, end_percentage=1.0, duration=700):
        try:
            if element is None:
                raise ValueError("Элемент не найден для прокрутки")

            location = element.location
            size = element.size

            start_x = location['x'] + int(size['width'] * start_percentage)
            end_x = location['x'] + int(size['width'] * end_percentage)
            start_y = location['y'] + int(size['height'] * start_percentage)
            end_y = location['y'] + int(size['height'] * end_percentage)

            if direction == 'right':
                self.driver.swipe(start_x, start_y, end_x, start_y, duration)
            elif direction == 'left':
                self.driver.swipe(end_x, start_y, start_x, start_y, duration)
            elif direction == 'down':
                self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            elif direction == 'up':
                self.driver.swipe(start_x, end_y, end_x, start_y, duration)
            else:
                raise ValueError("Неправильное направление, используй 'down', 'up', 'left', 'right'")

        except Exception as e:
            raise Exception(f"Ошибка при свайпе элемента': {e}")

    def get_all_visible_nested_texts(
            self,
            main_locator,
            nested_locator,
            max_scrolls=10,
            use_element_scroll=False,
            scroll_direction="up",
            element_start_percentage=0.2,
            element_end_percentage=0.8,
            duration=700
    ):
        texts = []
        previous_texts = []
        scroll_count = 0

        while scroll_count < max_scrolls:
            parent_elements = self.driver.find_elements(main_locator)

            for parent in parent_elements:
                try:
                    nested_elements = parent.find_elements(*nested_locator)

                    for nested_element in nested_elements:
                        text = nested_element.get_attribute("text")
                        if text and text not in texts:
                            texts.append(text)

                except NoSuchElementException as e:
                    raise NoSuchElementException(f"Вложенные элементы с локатором {nested_locator} не найдены: {e}")

            if texts == previous_texts:
                break

            previous_texts = texts.copy()

            if use_element_scroll:
                if parent_elements:
                    self.swipe_element(element=parent_elements[0],
                                       direction=scroll_direction,
                                       start_percentage=element_start_percentage,
                                       end_percentage=element_end_percentage,
                                       duration=duration
                    )
                else:
                    break
            else:
                self.swipe_screen(direction=scroll_direction, start_x=0.5, start_y=0.2, end_x=0.5, end_y=0.8, duration=700)

            scroll_count += 1

        return texts
