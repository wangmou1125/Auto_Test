import os
from time import sleep
from selenium import webdriver

from ui_test.page.base_page import BasePage
from common.model.function import read_yaml

class add_manage_page(BasePage):
    def __init__(self, driver=None):
        if driver is None:
            driver = webdriver.Chrome()
         # 读取配置文件
        super().__init__(driver)
        config_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)))), 'common', 'config', 'ui_config.yaml')
        self.config = read_yaml(config_path)
        self.locators = self.config.get('add_manage_page_locators', {})
