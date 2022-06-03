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

    def press_back(self):
        self.driver.press_keycode(4)  # keycode Back

    def test_lab8(self, textSize, filepath):
        tv = self.driver.find_element(AppiumBy.ID, 'textView')
        tv.click()
        time.sleep(1)

        try:
            title = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Name"]')
        except:
            print('프레퍼런스 Name을 찾을 수 없음')
            return False
        title.click()
        time.sleep(1)

        try:
            editText = self.driver.find_element(AppiumBy.XPATH, '//android.widget.EditText')
            editText.clear()
            editText.send_keys('Android')
        except:
            print('프레퍼런스 수정 다이얼로그가 표시되지 않음')
            return False

        try:
            ok = self.driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="OK"]')
            ok.click()
            time.sleep(1)
        except:
            print('프레퍼런스 수정 다이얼로그가 표시되지 않음')
            return False

        try:
            title = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Size"]')
        except:
            print('프레퍼런스 Size를 찾을 수 없음')
            return False
        title.click()
        time.sleep(1)

        try:
            big = self.driver.find_element(AppiumBy.XPATH, f'//android.widget.CheckedTextView[@text="{textSize}"]')
        except:
            print('프레퍼런스 수정 다이얼로그에서 big을 찾을 수 없음')
            return False
        big.click()
        time.sleep(1)

        try:
            title = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Italic"]')
        except:
            print('프레퍼런스 Italic을 찾을 수 없음')
            return False
        title.click()
        time.sleep(1)

        self.press_back()
        time.sleep(1)

        tv = self.driver.find_element(AppiumBy.ID, 'textView')
        if tv.text != 'Android':
            print('TextView의 내용이 Android로 변경되지 않음')
            return False
        self.driver.save_screenshot(filepath)

        return True


if __name__ == '__main__':
    # 테스트할 APK 파일의 위치
    DEF_APP_LOCATION = r'C:\Users\aksid\OneDrive\Desktop\repository\ch12\app\build\outputs\apk\debug\app-debug.apk'
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
    textSize = 'big'  # textSize는 'small', 'medium', 'big'
    r = chw.test_lab8(textSize, 'lab8.png')
    if r:
        score = 100
    else:
        score = 0  # 100 - len(r) * 10
    print(score, r)
    print(f'캡쳐 파일(lab8.png)에 나타난 글자의 크기와 모양이 설정 변경 내용({textSize}, Italic)과 다르면 감점 -50점')