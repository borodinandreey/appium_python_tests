import allure
from helper.android_helper.adb_helper import AdbHelper
from helper.android_helper.response_helper import ResponseHelper
from locators.android_locators.base_locators import FACE_BOOK_BUTTON_LOCATOR, MATCHES_SLIDER_LOCATOR
from locators.android_locators.team_page_locators import TEAM_PAGE_BUTTON_LOCATOR, TAPBAR_LOCATOR, MAIN_COACHING_STAFF_TAB_LOCATOR, \
    NESTED_COACHING_STAFF_TAB_LOCATOR, FIRST_COACH_POSITION_LOCATOR, MAIN_PLAYER_POSITIONS_LOCATOR, NESTED_PLAYER_POSITIONS_LOCATOR
from pages.android_pages.base_page import BasePage
from requests.team_page_requests import TEAM_REQUEST, TEAM_ID_REQUEST, COACHING_STAFF_ID_REQUEST


class TeamPage(BasePage):

    @allure.step("Переход на главную страницу")
    def move_to_home_page(self):
        self.click_element(FACE_BOOK_BUTTON_LOCATOR)
        self.wait_element(MATCHES_SLIDER_LOCATOR)

    @allure.step("Переход на таб 'Team'")
    def move_to_team_tab(self):
        self.click_element(TEAM_PAGE_BUTTON_LOCATOR)
        self.wait_element(TAPBAR_LOCATOR)

    @allure.step("Получение Team ID")
    def get_team_id(self):
        response = AdbHelper.get_responses_from_adb_logs()
        team_id = ResponseHelper.get_team_id(response)
        return team_id

    @allure.step("Проверка, что получены правильные запросы на табе 'Team'")
    def is_get_true_requests_on_team_tab(self, team_id):
        expected_result = [
                f"{TEAM_ID_REQUEST}{team_id}",
                TEAM_REQUEST
            ]
        return sorted(AdbHelper.get_requests()) == expected_result

    @allure.step("Переход на таб 'Coaching staff'")
    def move_to_coaching_staff_tab(self):
        self.click_nested_element(MAIN_COACHING_STAFF_TAB_LOCATOR, NESTED_COACHING_STAFF_TAB_LOCATOR)
        self.wait_element(FIRST_COACH_POSITION_LOCATOR)

    @allure.step("Проверка, что получены правильные запросы на табе 'Coaching staff'")
    def is_get_true_requests_on_coaching_staff_tab(self, team_id):
        expected_result = [f"{COACHING_STAFF_ID_REQUEST}{team_id}"]
        return AdbHelper.get_requests() == expected_result

    @allure.step("Проверка, что позиции игроков в приложении соответствуют позициям игроков в json")
    def is_player_positions_true(self):
        response = AdbHelper.get_responses_from_adb_logs()
        actual_result = self.get_all_visible_nested_texts(MAIN_PLAYER_POSITIONS_LOCATOR, NESTED_PLAYER_POSITIONS_LOCATOR)
        expected_result = ResponseHelper.get_job_titles(response)

        return actual_result == expected_result
