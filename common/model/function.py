# Function: 通用功能函数模块 - 读取 CSV 文件、YAML文件等功能函数
import os
import csv
import yaml

from common.utils.logger_util import get_logger



logger = get_logger(__name__)  # 初始化日志记录器
def read_csv_as_dict(file_path):
    """
    读取 CSV 文件并返回一个包含字典的列表，每一行作为一个字典。
    
    :param file_path: CSV 文件的路径
    :return: 包含字典的列表
    """
    try:
        logger.info(f"开始读取 CSV 文件: {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"文件未找到: {file_path}")
            return None
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            logger.info(f"成功读取 CSV 文件: {file_path}, 共 {len(data)} 行")
            return data
    except FileNotFoundError:
        logger.error(f"文件未找到: {file_path}")
        return []
    except Exception as e:
        logger.error(f"读取 CSV 文件时发生错误: {e}")
        return []


def read_yaml(file_path):
    """
    读取YAML文件并返回其内容。
    
    :param file_path: YAML文件的路径
    :return: YAML文件的内容
    """
    try:
        logger.info(f"开始读取YAML文件: {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"文件未找到: {file_path}")
            return None
        with open(file_path, mode='r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            logger.info(f"成功读取YAML文件: {file_path}")
            return data
    except FileNotFoundError:
        logger.error(f"文件未找到: {file_path}")
        return None
    except Exception as e:
        logger.error(f"读取YAML文件时发生错误: {e}")
        return None