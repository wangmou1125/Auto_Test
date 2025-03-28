import json
import requests

from common.utils.logger_util import get_logger
from common.model.function import read_yaml

class BaseApi:
    def __init__(self):
        self.logger = get_logger('BaseApi')
        self.config = read_yaml('common/config/api_config.yaml')
        self.base_url = self.config['env']['base_url']
        self.headers = self.config['env']['headers']
        self.session = requests.Session()
        
    def requests(self,method,url,**kwargs):
        """
        发送请求
        :param method: 请求方法
        :param url: 请求URL
        :param kwargs: 请求参数
        :return: 响应结果
        """
        
        if not url.startswith('http'):
            url = f"{self.base_url}{url}"
            
        self.logger.info(f'请求URL: {url}')
        self.logger.info(f'请求方法: {method}')
        
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
            
        if 'json' in kwargs:
            self.logger.info(f'请求参数: {json.dumps(kwargs["json"],ensure_ascii=False)}')
            
        try:
            response = self.session.request(method,url,**kwargs)
            self.logger.info(f'响应状态码: {response.status_code}')
            self.logger.info(f'响应结果: {response.text}')
            return response
        except Exception as e:
            self.logger.error(f'请求错误: {str(e)}')
            raise
    
    def extract_response(self, response, extract_key=None):
        """
        提取响应结果中的数据
        :param response: 响应结果
        :param extract_key: 提取的key
        :return: 提取结果
        """
        if response.status_code != 200:
            self.logger.warning(f"响应状态码错误: {response.status_code}")
            
        try:
            response_json = response.json()
        except Exception as e:
            self.logger.error(f"响应结果不是json格式: {str(e)}")
            return response.text
        
        if not extract_key:
            return response_json
        
        keys = extract_key.split(',')
        result = response_json
        for key in keys:
            if key in result:
                result = result[key]
            else:
                self.logger.warning(f"response中不存在key: {key}")
                return None
            
        return result
        
    def get(self, url, **kwargs):
        """GET请求方法"""
        return self.request("GET", url, **kwargs)
    
    def post(self, url, **kwargs):
        """POST请求方法"""
        return self.request("POST", url, **kwargs)
    
    def put(self, url, **kwargs):
        """PUT请求方法"""
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url, **kwargs):
        """DELETE请求方法"""
        return self.request("DELETE", url, **kwargs)
    