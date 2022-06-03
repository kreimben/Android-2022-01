from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import time
import sys, os


class CheckHW():
    MAIN_ACTIVITY = '.MainActivity'
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
            if len(items) != len(e_text):
                return False
            return items == e_text
        except:
            print('ID textView인 위젯을 찾을 수 없음')
            return False

    def add_item(self, name):
        try:
            fab = self.driver.find_element(AppiumBy.ID, 'floatingActionButton')
            fab.click()
        except:
            print('ID floatingActionButton 위젯을 찾을 수 없음')
            return False

        try:
            ok = self.driver.find_element(AppiumBy.ID,
                                          'buttonOK')  # AppiumBy.XPATH, '//android.widget.Button[@text="OK"]')
            editText = self.driver.find_element(AppiumBy.ID, 'editTextName')
            editText.clear()
            editText.send_keys(name)
            ok.click()
            return True
        except:
            print('buttonOK 또는 editTextName을 찾을 수 없음')
            return False

    def update_item(self, idx, name):
        try:
            elements = self.driver.find_elements(AppiumBy.ID, 'textView')
        except:
            print('ID textView인 위젯을 찾을 수 있음')
            return False

        if idx >= len(elements):
            return False

        actions = TouchAction(self.driver)
        actions.long_press(elements[idx])
        actions.perform()

        try:
            edit = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Edit"]')
            edit.click()
        except:
            print('Edit를 찾을 수 없음')
            return False

        try:
            ok = self.driver.find_element(AppiumBy.ID,
                                          'buttonOK')  # AppiumBy.XPATH, '//android.widget.Button[@text="OK"]')
            editText = self.driver.find_element(AppiumBy.ID, 'editTextName')
            editText.clear()
            editText.send_keys(name)
            ok.click()
            return True
        except:
            print('OK 버튼 또는 EditText를 찾을 수 없음')
            return False

    def delete_item(self, idx):
        try:
            elements = self.driver.find_elements(AppiumBy.ID, 'textView')
        except:
            print('ID textView인 위젯을 찾을 수 있음')
            return False

        if idx >= len(elements):
            return False

        actions = TouchAction(self.driver)
        actions.long_press(elements[idx])
        actions.perform()

        try:
            edit = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Delete"]')
            edit.click()
        except:
            print('Delete를 찾을 수 없음')
            return False
        return True

    def test_lab7(self):
        if not self.add_item('android'): return False
        if not self.add_item('jetpack'): return False
        items = self.get_list_items()

        if not self.update_item(0, 'android12'): return False
        items[0] = 'android12'
        time.sleep(1)  # 리싸이클러 뷰 항목이 업데이트될 때 뷰홀더가 바뀌는데, 이 작업이 정상 완료될때까지 잠시 기다림
        if not self.delete_item(1): return False
        del items[1]
        time.sleep(1)

        print(items)
        return self.check_list_items(items)


if __name__ == '__main__':
    # 테스트할 APK 파일의 위치
    DEF_APP_LOCATION = r'C:\Users\aksid\OneDrive\Desktop\repository\ch11\app\build\intermediates\apk\debug\app-debug.apk'
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
    5. ANDROID_VERSION은 에뮬레이터나 디바이스의 안드로이드 버전과 일치하나요?
    ''')

    chw = CheckHW(DEF_APP_LOCATION, ANDROID_VERSION)
    r = chw.test_lab7()
    if r:
        score = 100
    else:
        score = 0  # 100 - len(r) * 10
    print(score, r)