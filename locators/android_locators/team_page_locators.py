from appium.webdriver.common.appiumby import AppiumBy

TEAM_PAGE_BUTTON_LOCATOR = [AppiumBy.XPATH, '//android.widget.FrameLayout[@content-desc="Team"]']
TAPBAR_LOCATOR = [AppiumBy.XPATH, '//android.widget.HorizontalScrollView[@resource-id="match.day.app.online.debug:id/tab_teams"]/android.widget.LinearLayout']
MAIN_COACHING_STAFF_TAB_LOCATOR = [AppiumBy.XPATH, '//android.widget.HorizontalScrollView[@resource-id="match.day.app.online.debug:id/tab_teams"]/android.widget.LinearLayout']
NESTED_COACHING_STAFF_TAB_LOCATOR = [AppiumBy.XPATH, './/android.widget.LinearLayout']
FIRST_COACH_POSITION_LOCATOR = [AppiumBy.XPATH, '(//android.widget.LinearLayout[@resource-id="match.day.app.online.debug:id/ts_title"])[1]']
MAIN_PLAYER_POSITIONS_LOCATOR = [AppiumBy.XPATH, '//android.widget.LinearLayout[@resource-id="match.day.app.online.debug:id/ts_title"]']
NESTED_PLAYER_POSITIONS_LOCATOR = [AppiumBy.XPATH, './/android.widget.TextView[@resource-id="match.day.app.online.debug:id/tv_title"]']
