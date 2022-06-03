from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


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

    def open_nav_drawer(self, menu):
        try:
            btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Open navigation drawer')
        except:
            self.err_str.append('네비게이션 드로어 버튼을 찾을 수 없음')
            return
        btn.click()

        try:
            self.driver.find_element(AppiumBy.ID, menu).click()
        except:
            self.err_str.append(f'{menu} ID를 찾을 수 없음')

    def check_text(self, widget_ID, text_wanted):
        try:
            title = self.driver.find_element(AppiumBy.ID, widget_ID)
        except:
            self.err_str.append(f'{widget_ID} ID를 찾을 수 없음')
            return

        if title.text != text_wanted:
            self.err_str.append(f'ID {widget_ID}의 텍스트가 {text_wanted}가 아님')

    def check_text2(self, widget_ID, widget_ID2, text_wanted):
        try:
            title = self.driver.find_element(AppiumBy.ID, widget_ID)
        except:
            try:
                title = self.driver.find_element(AppiumBy.ID, widget_ID2)
            except:
                self.err_str.append(f'{widget_ID} 또는 {widget_ID2} ID를 찾을 수 없음')
                return

        if title.text != text_wanted:
            self.err_str.append(f'ID {widget_ID} 또는 {widget_ID2}의 텍스트가 {text_wanted}가 아님')

    def test_lab6(self, title, message):
        self.err_str = []

        self.open_nav_drawer('page1Fragment')
        self.check_text('textView', 'Page1Fragment')

        self.open_nav_drawer('myDialogFragment')
        self.check_text2('alertTitle', 'android:id/alertTitle', title)
        self.check_text2('android:id/message', 'message', message)
        try:
            ok = self.driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="OK"]')  # android:id/button1')
            ok.click()
        except:
            self.err_str.append('OK 버튼을 찾을 수 없음')

        self.open_nav_drawer('page2Fragment')
        self.check_text('textView', 'Page2Fragment')

        return self.err_str


if __name__ == '__main__':
    # 테스트할 APK 파일의 위치
    DEF_APP_LOCATION = r'C:\Users\aksid\OneDrive\Desktop\repository\ch10\app\build\intermediates\apk\debug\app-debug.apk'
    ANDROID_VERSION = '12.0'

    print('''
    1. Appium 서버는 실행 했나요?
    2. 에뮬레이터를 실행하거나 디바이스를 연결 했나요?
    3. 에뮬레이터는 정상적으로 동작 중인가요? 에뮬레이터가 멈춰있다면 cold boot하세요.
    4. DEF_APP_LOCATION은 본인의 app-debug.apk를 제대로 가리키고 있나요?
    5. ANDROID_VERSION은 에뮬레이터나 디바이스의 안드로이드 버전과 일치하나요?
    ''')

    chw = CheckHW(DEF_APP_LOCATION, ANDROID_VERSION)
    r = chw.test_lab6('1991283', '김제환')  # 학번, 이름
    if len(r) == 0:
        score = 100
    else:
        score = 0  # 100 - len(r) * 10
    print(score, r)