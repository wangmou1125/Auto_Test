import os
import allure
import pytest


from common.model.function import read_csv_as_dict
from ui_test.page.login_page import LoginPage
from common.utils.logger_util import get_logger

# 初始化日志记录器
logger = get_logger(__name__)


@pytest.fixture(scope='session')
def test_data():
    """加载测试数据，作为session级别的fixture"""
    logger.info('开始登录测试')
    # 初始化测试数据
    data_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)))), 'ui_test', 'data', 'ui_login_data.csv')
    test_data = read_csv_as_dict(data_path)
    logger.info(f'加载测试数据: {data_path}')
    yield test_data
    logger.info('结束登录测试')


@pytest.fixture(autouse=True)
def setup_teardown():
    """测试环境的设置和清理，自动应用于所有测试"""
    logger.info('初始化测试环境')
    # 初始化浏览器
    login_page = LoginPage()
    login_page.open_login_page()
    yield login_page
    logger.info('清理测试环境')
    login_page.close_browser()


@allure.feature('登录功能')
@allure.story('有效登录')
def test_valid_login(setup_teardown, test_data):
    """测试有效登录场景"""
    login_page = setup_teardown
    logger.info('开始测试有效登录')

    # 获取有效登录测试数据
    valid_login_data = next((data for data in test_data if data['type'] == 'valid_login'), None)
    if valid_login_data:
        username = valid_login_data['username']
        password = valid_login_data['password']
        expected = valid_login_data['expected']

        logger.info(f'使用用户名: {username} 进行登录测试')
        # 执行登录操作
        login_page.login(username, password)

        # TODO: 登录成功后验证登陆成功后跳转网址(没做版)
        # 可以通过检查当前URL或页面元素来验证登录成功
        # assert "index" in login_page.driver.current_url, "登录后未跳转到首页"

        logger.info('有效登录测试完成')
    else:
        pytest.fail("未找到有效登录测试数据")


def get_invalid_login_test_data():
    """获取无效登录测试数据，用于参数化测试"""
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'ui_test', 'data', 'ui_login_data.csv')
    test_data = read_csv_as_dict(data_path)
    return [pytest.param(
        data['username'],
        data['password'],
        data['expected'],
        id=data['case']
    ) for data in test_data if data['type'] == 'invalid_login']


@allure.feature('登录功能')
@allure.story('无效登录')
@pytest.mark.parametrize('username,password,expected', get_invalid_login_test_data())
def test_invalid_login(setup_teardown, username, password, expected):
    """测试无效登录场景，使用参数化测试多种情况"""
    login_page = setup_teardown
    logger.info('开始测试无效登录')
    logger.info(f'测试用例参数 - 用户名: {username}, 密码: {password}')

    # 执行登录操作
    login_page.login(username, password)

    # 获取错误信息
    error_message = login_page.get_error_message()

    # 验证错误信息
    assert expected in error_message, f"测试失败: 期望包含 '{expected}', 实际错误信息为 '{error_message}'"
    logger.info(f'验证错误信息: {error_message}')
