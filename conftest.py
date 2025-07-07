import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium import webdriver
from data.base_data import ANDROID_CAPABILITIES, IOS_CAPABILITIES


@pytest.fixture()
def android_driver():
    driver = None
    options = UiAutomator2Options()
    capabilities = ANDROID_CAPABILITIES
    options.load_capabilities(capabilities)
    url = "http://localhost:4723"

    try:
        driver = webdriver.Remote(command_executor=url, options=options)
        yield driver
    except Exception as e:
        pytest.fail(f"Ошибка при запуске android драйвера: {e}")
    finally:
        if driver:
            driver.quit()

@pytest.fixture()
def ios_driver():
    driver = None
    options = XCUITestOptions()
    capabilities = IOS_CAPABILITIES
    options.load_capabilities(capabilities)
    url = "http://localhost:4725"

    try:
        driver = webdriver.Remote(command_executor=url, options=options)
        yield driver
    except Exception as e:
        pytest.fail(f"Ошибка при запуске android драйвера: {e}")
    finally:
        if driver:
            driver.quit()
