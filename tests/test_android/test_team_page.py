import allure
from helper.android_helper.adb_helper import AdbHelper
from pages.android_pages.team_page import TeamPage


@allure.feature("Андройд тесты на получение корректных запросов и ответов")
class TestTeamPage:

    @allure.title("Проверка получения корректного запроса на табе 'Team'")
    def test_get_team_tab_request(self, android_driver):
        page = TeamPage(android_driver)

        page.move_to_home_page()
        AdbHelper.clear_log()
        page.move_to_team_tab()
        page.get_team_id()

        assert page.is_get_true_requests_on_team_tab

    @allure.title("Проверка получения корректного запроса на табе 'Coaching staff'")
    def test_get_team_tab_request(self, android_driver):
        page = TeamPage(android_driver)

        page.move_to_home_page()
        AdbHelper.clear_log()
        page.move_to_team_tab()
        page.get_team_id()
        AdbHelper.clear_log()
        page.move_to_coaching_staff_tab()

        assert page.is_get_true_requests_on_coaching_staff_tab

    @allure.title("Проверка, что позиции игрока в приложении соответствуют позициям игрока в json")
    def test_check_player_positions_in_app_match_player_positions_in_json(self, android_driver):
        page = TeamPage(android_driver)

        page.move_to_home_page()
        AdbHelper.clear_log()
        page.move_to_team_tab()

        assert page.is_player_positions_true
