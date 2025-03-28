import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.utils.logger_util import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.logger = get_logger(__name__)

    def open_url(self, url):
        self.logger.info(f'打开网址: {url}')
        self.driver.get(url)

    def click(self, locator):
        self.logger.info(f'点击元素: {locator}')
        try:
            element = self.find_element(locator)
            element.click()
        except Exception as e:
            self.logger.error(f'点击元素失败: {e}')
            self.take_screenshot('click_error')
            raise

    def close_browser(self):
        self.logger.info('关闭浏览器')
        self.driver.quit()

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def input_text(self, locator, text):
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f'输入文本失败: {e}')
            self.take_screenshot('input_error')
            raise

    def get_text(self, locator):
        try:
            element = self.find_element(locator)
            return element.text
        except Exception as e:
            self.logger.error(f'获取文本失败: {e}')
            self.take_screenshot('get_text_error')
            raise

    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def get_locator(self, element_name):
        """根据元素名称获取定位器"""
        element = self.locators.get(element_name)
        if not element:
            self.logger.error(f"元素 {element_name} 未在配置文件中定义")
            return None

        by_method = element.get('by')
        value = element.get('value')

        # 将字符串形式的定位方式转换为 By 类的属性
        by_dict = {
            'id': By.ID,
            'name': By.NAME,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
            'xpath': By.XPATH,
            'css_selector': By.CSS_SELECTOR
        }

        by = by_dict.get(by_method)
        if not by:
            self.logger.error(f"不支持的定位方式: {by_method}")
            return None

        return by, value

    def take_screenshot(self, name=None):
        """
        截图并保存到指定路径。

        :param name: 截图文件名（可选）
        :return: 截图保存路径
        """
        try:
            if name is None:
                from datetime import datetime
                name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

            screenshot_dir = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(os.path.abspath(__file__))))), 'reports', 'screenshot')
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            file_path = os.path.join(screenshot_dir, f'{name}.png')
            self.driver.save_screenshot(file_path)
            self.logger.info(f'截图已保存: {file_path}')
            return file_path
        except Exception as e:
            self.logger.error(f"截图失败: {e}")
            return None
