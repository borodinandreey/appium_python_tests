ANDROID_CAPABILITIES = {
        "platformName": "Android",
        "appium:automationName": "uiautomator2",
        "appium:deviceName": "Samsung A51",
        "appium:appPackage": "match.day.app.online.debug",
        "appium:appActivity": "match.day.app.MatchDayActivity",
        "appium:noReset": False
    }

IOS_CAPABILITIES = {
        "platformName": "iOS",
        "platformVersion": "17.5",
        "deviceName": "iPhone 13",
        "app": "app.crespo.core",
        "appium:udid": "00008110-000930881AEA801E",
        "automationName": "XCUITest",
        "appium:noReset": False
}

DOMAIN_FILTER = "sandbox4.matchplatform.org"