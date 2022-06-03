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
        'locale': 'US',
        'autoGrantPermissions': 'true'
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

    def get_list_items(self):
        ret_list = []
        try:
            elements = self.driver.find_elements(AppiumBy.ID, 'textView')
            ret_list = [e.text for e in elements]
        except:
            print('ID textView인 위젯을 찾을 수 없음')
        return ret_list

    def check_list_items(self, items):
        try:
            elements = self.driver.find_elements(AppiumBy.ID, 'textView')
            e_text = [e.text for e in elements]
            return items[:3] == e_text[:len(items)]
        except:
            print('ID textView인 위젯을 찾을 수 없음')
            return False

    def test_lab10(self, adb, media_image_list):
        # 리싸이클러뷰 테스트
        if self.check_list_items(media_image_list) is False:
            return '리싸이클러뷰에 미디어스토어 이미지들이 제대로 로드되지 않음'

        try:
            tv = self.driver.find_element(AppiumBy.ID, 'textViewBroadcast')
        except:
            return 'textViewBroadcast 를 찾을 수 없음'
        if tv.text == 'ACTION_MY_BROADCAST':
            return 'Broadcast 수신 전에 textViewBroadcast의 내용이 ACTION_MY_BROADCAST 이면 안됨'

        # 브로드캐스트, action은 ACTION_MY_BROADCAST
        broadcast_action_name = 'ACTION_MY_BROADCAST'
        os.system(f'{adb} shell am broadcast -a {broadcast_action_name}')

        time.sleep(2)
        if tv.text != 'ACTION_MY_BROADCAST':
            return 'Broadcast 수신 후에 textViewBroadcast의 내용이 ACTION_MY_BROADCAST가 아님'

        return 'OK'


if __name__ == '__main__':
    # 테스트할 APK 파일의 위치
    DEF_APP_LOCATION = r'C:\Users\jyheo\AndroidStudioProjects\Lab10\app\build\intermediates\apk\debug\app-debug.apk'
    # ADB.EXE 의 위치. 보통 Android SDK 밑에 platform-tools 밑에 있음, 맥이나 리눅스는 exe 확장자는 없음
    ADB_LOCATION = r'C:\Users\jyheo\AppData\Local\Android\Sdk\platform-tools\adb.exe'
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

    media_image_list = ['IMG_20220525_212830', 'IMG_20220525_224834',
                        'IMG_20220525_224835']  # 이미지 이름 목록, 3개만, 테스트하는 장치에 저장된 이미지 이름 3개까지만 테스트함
    r = chw.test_lab10(ADB_LOCATION, media_image_list)  # 실습 검사할 때 초기값은 랜덤하게 정함
    if r == 'OK':
        score = 100
    else:
        score = 0  # 100 - len(r) * 10
    print(score, r)