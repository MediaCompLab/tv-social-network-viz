import logging
import time, os
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
# print( os.path.dirname(os.getcwd()))
# 创建访问日志Logconf.py
class config_log(object):
    strftime = time.strftime("%Y%m%d", time.localtime())
    # 当前目录
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "."))
    # base_dir=os.path.dirname(os.getcwd())
    # logs目录
    log_dir = (os.path.join(base_dir, "logs"))
    # 存放日志的文件名,用时间作为日志格式
    file_name = (os.path.join(log_dir, strftime + ".log"))
    #file_name = (os.path.join('d:\logs\\'+strftime+".log"))
    # 设置日志的记录等级
    logging.basicConfig(level=logging.INFO)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = TimedRotatingFileHandler(file_name, when="D", interval=1, backupCount=15, encoding='utf-8',
                                                delay=False, utc=True)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter( "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    # logging.getLogger().addHandler(file_log_handler)


