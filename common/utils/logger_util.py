# Description: 日志模块
import os
import yaml
import logging
import logging.config

from datetime import datetime



# 存储已创建的Logger实例
loggers = {}


def get_logger(name):
    # 如果已经创建过该名称的logger，直接返回
    if name in loggers:
        return loggers[name].logger
    # 否则创建新的Logger实例
    logger_instance = Logger(name)
    loggers[name] = logger_instance
    return logger_instance.logger


class Logger:
    def __init__(self, name):
        # 创建日志目录
        log_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)))), 'reports', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 加载日志配置
        config_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__))), 'config', 'logger.yaml')
        with open(config_path, 'r', encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # 修改日志文件路径为绝对路径
        # 使用当前时间创建包含模块名和日期的文件名
        current_date = datetime.now().strftime('%Y%m%d')
        log_filename = f"{name.replace('.', '_')}_{current_date}.log"
        config['handlers']['file']['filename'] = os.path.join(log_dir, log_filename)

        # 确保只配置一次日志系统
        if not hasattr(logging, 'logger_config_done'):
            logging.config.dictConfig(config)
            setattr(logging, 'logger_config_done', True)

        self.logger = logging.getLogger(name)
        # 确保日志级别正确设置
        self.logger.setLevel(logging.DEBUG)
        self.name = name

    def info(self, message):
        """记录info级别日志"""
        self.logger.info(message)

    def error(self, message):
        """记录error级别日志"""
        self.logger.error(message)

    def debug(self, message):
        """记录debug级别日志"""
        self.logger.debug(message)

    def warning(self, message):
        """记录warning级别日志"""
        self.logger.warning(message)