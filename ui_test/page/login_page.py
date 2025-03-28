import os
from time import sleep
from selenium import webdriver

from ui_test.page.base_page import BasePage
from common.model.function import read_yaml


class LoginPage(BasePage):
    def __init__(self, driver=None):
        if driver is None:
            driver = webdriver.Chrome()
        # 读取配置文件
        super().__init__(driver)
        config_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)))),'common','config', 'ui_config.yaml')
        self.config = read_yaml(config_path)
        self.locators = self.config.get('login_page_locators', {})

    def open_login_page(self):
        """打开登录页面"""
        url = self.config.get('env', {}).get('url')
        if url:
            self.open_url(url)
        else:
            self.logger.error("配置文件中未找到登录页面URL")

    def input_username(self, username):
        """输入用户名"""
        self.logger.info(f'输入用户名:{username}')
        locator = self.get_locator('username_input')
        if locator:
            self.input_text(locator, username)

    def input_password(self, password):
        """输入密码"""
        self.logger.info(f'输入密码:{password}')
        locator = self.get_locator('password_input')
        if locator:
            self.input_text(locator, password)

    def click_login_button(self):
        """点击登录按钮"""
        locator = self.get_locator('login_button')
        if locator:
            self.click(locator)

    def login(self, username, password):
        """执行登录操作"""
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()
        sleep(1)

    def get_error_message(self):
        """获取登录错误信息"""
        locator = self.get_locator('login_error_message')
        if locator:
            return self.get_text(locator)
        return None
