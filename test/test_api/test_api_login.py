import pytest
import allure
import os

from api_test.api.login_api import LoginApi
from common.model.function import read_yaml


@allure.epic("API测试")
@allure.feature("登录功能")
class TestLoginApi:
    def setup_class(self):
        self.login_api = LoginApi()
        data_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)))), 'api_test', 'data', 'login_api_data.yaml')
        self.test_data = read_yaml(data_path)

    @allure.story("登录测试")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("test_case", read_yaml(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'api_test', 'data', 'login_api_data.yaml'))['login'])
    def test_login(self, test_case):
        """登录测试"""
        # 提取测试数据
        case_name = test_case['case']
        username = test_case['username']
        password = test_case.get('password', '')
        role_id = test_case.get('roleId', 1)
        expected = test_case['expected']
        test_type = test_case['type']

        # 添加测试标题
        allure.dynamic.title(case_name)

        # 根据测试类型执行不同的测试方法
        if test_type == 'valid_login':
            # 有效登录测试
            response = self.login_api.valid_login(username, password, role_id)
            # 验证响应码
            assert self.login_api.extract_response(response, "code") == expected['code']
        elif test_type == 'invalid_login':
            # 无效登录测试
            expected_msg = expected.get('msg')
            expected_code = expected.get('code', 500)
            response = self.login_api.invalid_login(
                username,
                password,
                role_id,
                expected_msg=expected_msg,
                expected_code=expected_code
            )
            # 验证响应码和错误信息
            assert self.login_api.extract_response(response, "code") == expected_code
            if expected_msg:
                assert self.login_api.extract_response(response, "msg") == expected_msg

    @allure.story("获取Token测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_token(self):
        """获取Token测试"""
        # 使用有效的用户名和密码获取token
        valid_data = next(item for item in self.test_data['login'] if item['type'] == 'valid_login')
        username = valid_data['username']
        password = valid_data['password']
        role_id = valid_data.get('roleId', 1)

        # 获取token
        token = self.login_api.get_token(username, password, role_id)

        # 验证token不为空
        assert token is not None, "获取token成功"
