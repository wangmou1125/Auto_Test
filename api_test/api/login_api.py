from api_test.api.base_api import BaseApi
from common.model.function import read_yaml


class LoginApi(BaseApi):
    def __init__(self):
        super().__init__()
        # 使用api_config.yaml作为配置文件
        self.config = read_yaml('common/config/api_config.yaml')
        self.login_url = self.config['api']['login']['url']
        self.login_headers = self.config['api']['login']['headers']

    def login(self, username, password, role_id=1):
        """
        登录接口
        :param username: 用户名
        :param password: 密码
        :param role_id: 角色ID，默认为1
        :return: 响应结果
        """
        self.logger.info(f"开始登录，用户名: {username}")

        # 构建请求数据
        data = {
            "username": username,
            "password": password,
            "roleId": role_id
        }

        # 发送请求
        response = self.requests("POST", self.login_url, json=data, headers=self.login_headers)
        return response

    def valid_login(self, username, password, role_id=1):
        """
        有效登录测试
        :param username: 用户名
        :param password: 密码
        :param role_id: 角色ID，默认为1
        :return: 响应结果
        """
        response = self.login(username, password, role_id)
        # 提取响应中的code
        code = self.extract_response(response, "code")
        # 验证code是否为200
        assert code == 200, f"登录成功，响应code: {code}"
        return response

    def invalid_login(self, username, password, role_id=1, expected_msg=None, expected_code=500):
        """
        无效登录测试
        :param username: 用户名
        :param password: 密码
        :param role_id: 角色ID，默认为1
        :param expected_msg: 预期错误信息
        :param expected_code: 预期错误码，默认为500
        :return: 响应结果
        """
        response = self.login(username, password, role_id)
        # 提取响应中的code和msg
        code = self.extract_response(response, "code")
        # 验证code是否为预期值
        assert code == expected_code, f"登录响应code不符合预期，预期: {expected_code}，实际: {code}"

        # 如果有预期错误信息，则验证msg是否符合预期
        if expected_msg:
            msg = self.extract_response(response, "msg")
            assert msg == expected_msg, f"登录响应msg不符合预期，预期: {expected_msg}，实际: {msg}"

        return response

    def get_token(self, username, password, role_id=1):
        """
        获取登录token
        :param username: 用户名
        :param password: 密码
        :param role_id: 角色ID，默认为1
        :return: token字符串
        """
        response = self.login(username, password, role_id)
        # 提取响应中的token
        token = self.extract_response(response, "data")
        if not token:
            self.logger.error("获取token失败")
            return None

        else:
            self.logger.info(f"成功获取token{token}")
            return token
