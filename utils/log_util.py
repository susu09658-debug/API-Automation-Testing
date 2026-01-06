import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


# 定义日志工具类，封装日志初始化的相关逻辑
class LogUtils:
    # 定义静态方法，无需实例化类即可调用
    @staticmethod
    def init_logger(log_name=None):
        """
        初始化日志记录器
        :param log_name: 日志名称（可选），用于区分不同业务的日志文件
        :return: 配置好的logger对象
        """
        # 拼接日志目录路径：当前文件的父目录的父目录下的log文件夹
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
        # 如果日志目录不存在，则创建该目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # 拼接日志文件路径：日志目录 + 年月日 + 日志名称 + .log后缀
        log_file_name = os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}_{log_name}.log')
        # 创建/获取logger对象，使用日志文件路径作为logger的唯一标识
        logger = logging.getLogger(log_file_name)
        # 设置logger的基础日志级别为DEBUG（会捕获DEBUG及以上级别的日志）
        logger.setLevel(logging.DEBUG)
        # 如果logger已经配置过处理器（避免重复添加handler），直接返回logger
        if logger.handlers:
            return logger

        # 创建按时间轮转的文件处理器
        file_handler = TimedRotatingFileHandler(
            filename=log_file_name,  # 日志文件路径
            when='D',  # 轮转周期：按天轮转
            interval=1,  # 轮转间隔：1天
            backupCount=30,  # 保留的日志文件备份数量：30个
            encoding="utf-8"  # 日志文件编码：UTF-8（避免中文乱码）
        )
        # 设置文件处理器的日志级别为INFO（仅将INFO及以上级别日志写入文件）
        file_handler.setLevel(logging.INFO)

        # 创建控制台处理器（将日志输出到控制台）
        console_handler = logging.StreamHandler()
        # 设置控制台处理器的日志级别为DEBUG（控制台输出DEBUG及以上级别日志）
        console_handler.setLevel(logging.DEBUG)

        # 定义日志格式：时间 - 日志器名称 - 日志级别 - 模块名:行号 - 日志消息
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"  # 时间格式：年-月-日 时:分:秒
        )
        # 为文件处理器设置日志格式
        file_handler.setFormatter(log_format)
        # 为控制台处理器设置日志格式
        console_handler.setFormatter(log_format)

        # 给logger添加文件处理器（日志写入文件）
        logger.addHandler(file_handler)
        # 给logger添加控制台处理器（日志输出到控制台）
        logger.addHandler(console_handler)

        # 返回配置完成的logger对象
        return logger


# 初始化全局logger对象（log_name为None时，日志文件名会包含None，建议调用时传入具体名称）
logger = LogUtils.init_logger()
