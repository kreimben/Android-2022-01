import random

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import time
import sys, os


class CheckHW():
    EXECUTOR = 'http://127.0.0.1:4723/wd/hub'
    ANDROID_BASE_CAPS = {
        'app': 'app-debug.apk',  # path to the app package
        'automationName': 'UIAutomator2',
        'platformName': 'Android',
        'platformVersion': '12.0',  # platform version of emulator or device where app will be tested
        'deviceName': 'Android Emulator',
        'allowTestPackages': 'true',  # add -t flags to adb command when install the app package
        'enforceAppInstall': 'true',
        'uiautomator2ServerInstallTimeout': 20000,
        'adbExecTimeout': 20000,
        'language': 'en',
        'locale': 'US'
    }

    def __init__(self, appLocation, platformVersion='12.0'):
        self.ANDROID_BASE_CAPS['app'] = appLocation
        self.ANDROID_BASE_CAPS['platformVersion'] = platformVersion

        self.driver = webdriver.Remote(
            command_executor=self.EXECUTOR,
            desired_capabilities=self.ANDROID_BASE_CAPS
        )
        self.driver.implicitly_wait(10)

    def press_home(self):
        self.driver.press_keycode(3)  # keycode HOME

    def press_back(self):
        self.driver.press_keycode(4)  # keycode Back

    def test_lab9(self, adb, initial_value):
        try:
            button = self.driver.find_element(AppiumBy.ID, 'buttonGet')
            tv = self.driver.find_element(AppiumBy.ID, 'textView')
        except:
            return 'buttonGet 이나 textView 를 찾을 수 없음'

        button.click()
        time.sleep(1)
        if tv.text != '0':
            return '서비스 시작 전에는 textView의 내용이 0이어야 함'

        # 서비스 시작, 패키지 이름, 서비스 이름 고정. 절대 다른 것으로 하면 안됨
        package_name = 'com.example.lab9'
        service_name = 'MyService'
        os.system(
            f'{adb} shell am start-foreground-service -n {package_name}/{package_name}.{service_name} --ei init {initial_value}')

        time.sleep(2)
        button.click()
        time.sleep(2)
        num1 = int(tv.text)
        button.click()
        time.sleep(2)
        num2 = int(tv.text)

        print(f'num1: {num1}')
        print(f'num2: {num2}')

        if num1 > initial_value and num2 > num1:
            return 'OK'
        else:
            return 'textView의 숫자 변화가 실습 요구사항에 맞지 않음'


if __name__ == '__main__':
    # 테스트할 APK 파일의 위치
    DEF_APP_LOCATION = r'C:\Users\aksid\OneDrive\Desktop\repository\ch13\app\build\outputs\apk\debug\app-debug.apk'
    # ADB.EXE 의 위치. 보통 Android SDK 밑에 platform-tools 밑에 있음, 맥이나 리눅스는 exe 확장자는 없음
    ADB_LOCATION = r'C:\Users\aksid\OneDrive\Desktop\platform-tools\adb.exe'
    ANDROID_VERSION = '12.0'
    if len(sys.argv) >= 2:  # apk 파일을 명령줄 인자로 받을 수 있도록
        if sys.argv[1][-3:] == 'apk':
            DEF_APP_LOCATION = os.path.abspath(sys.argv[1])
            print('Test with ' + DEF_APP_LOCATION)

    print('''
    1. Appium 서버는 실행 했나요?
    2. 에뮬레이터를 실행하거나 디바이스를 연결 했나요?
    3. 에뮬레이터는 정상적으로 동작 중인가요? 에뮬레이터가 멈춰있다면 cold boot하세요.
    4. DEF_APP_LOCATION은 본인의 app-debug.apk를 제대로 가리키고 있나요?
    5. ****** ADB_LOCATION ****** 은 제대로 설정했나요?
    6. ANDROID_VERSION은 에뮬레이터나 디바이스의 안드로이드 버전과 일치하나요?
    ''')

    chw = CheckHW(DEF_APP_LOCATION, ANDROID_VERSION)

    rand = random.randint(1, 10000)
    print(f"rand: {rand}")
    r = chw.test_lab9(ADB_LOCATION, rand)  # 실습 검사할 때 초기값은 랜덤하게 정함
    if r == 'OK':
        score = 100
    else:
        score = 0  # 100 - len(r) * 10
    print(score, r)