import os

import allure
import allure_commons
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from dotenv import load_dotenv
from selene import browser, support

import utils
from config import config


@pytest.fixture(scope='session', autouse=True)
def load_end():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    user_name = os.getenv('BSTACK_USER')
    access_key = os.getenv('BSTACK_ACCESS_KEY')

    if request.param == 'Android':
        options = UiAutomator2Options().load_capabilities({
            "platformName": "android",
            "platformVersion": "9.0",
            "deviceName": "Google Pixel 3",

            "app": config.app_id,

            'bstack:options': {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",

                "userName": user_name,
                "accessKey": access_key
            }
        })
    else:
        options = XCUITestOptions().load_capabilities({
            "app": config.app_id,

            "deviceName": "iPhone 11 Pro",
            "platformName": "ios",
            "platformVersion": "13",

            "bstack:options": {
                "userName": user_name,
                "accessKey": access_key,
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test"
            }
        })
    with allure.step('Init app session'):
        browser.config.driver = webdriver.Remote(
            config.browser_url,
            options=options
        )

    browser.config.timeout = config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    browser.config.driver_remote_url = config.browser_url
    browser.config.driver_options = options

    browser.config.timeout = config.timeout

    yield

    utils.add_screenshot(browser)
    utils.add_xml(browser)

    session_id = browser.driver.session_id

    with allure.step('Tear down app session'):
        browser.quit()

    utils.attach_bstack_video(session_id, user_name, access_key)


# Device name parameters
ios = pytest.mark.parametrize('mobile_management', ['IOS'], indirect=True)
android = pytest.mark.parametrize('mobile_management', ['Android'], indirect=True)
