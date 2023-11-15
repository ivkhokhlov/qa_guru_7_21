import os

import pydantic_settings
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)


class Config(pydantic_settings.BaseSettings):
    context: str = 'local_real'
    timeout: float = 10.0


config = Config()

if config.context == 'bstack':
    load_dotenv()
    load_dotenv(os.path.join(BASE_DIR, '.env.bstack'))
elif config.context == 'local_real':
    load_dotenv(os.path.join(BASE_DIR, '.env.local_real'))
else:
    load_dotenv(os.path.join(BASE_DIR, '.env.local_emulator'))

remote_url = os.getenv('REMOTE_URL')
udid = os.getenv('UDID')
device_name = os.getenv('DEVICE_NAME')

apk_path = os.getenv('APP_ID') if config.context == 'bstack' \
    else os.path.join(BASE_DIR, 'apk', os.getenv('APP_ID'))


def driver_options():
    options = UiAutomator2Options().load_capabilities({
        'platformName': 'Android',
        'app': apk_path,
        'appWaitActivity': 'org.wikipedia.*',

    })

    if device_name:
        options.set_capability('deviceName', os.getenv('DEVICE_NAME'))

    if config.context == 'bstack':
        options.set_capability('platformVersion', '9.0')
        options.set_capability(
            "bstack:options", {
                "userName": os.getenv('BSTACK_USER'),
                "accessKey": os.getenv('BSTACK_ACCESS_KEY'),
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test"
            },
        )

    return options
