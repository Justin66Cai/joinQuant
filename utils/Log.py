import io
import logging
import os
import sys
import time


class Log():

    def __init__(self,path=None):
        self.logger = logging.getLogger("myLogger")
        if not self.logger.handlers:
            day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            self.logger.setLevel(logging.INFO)
            logPath=os.path.abspath('../')
            logName = logPath + "\logs\%s.log" % day
            logFiles = path if path else logName
            # print('logfiles=',logFiles)
            # print(logFiles)
            # 创建handler,将log写入
            file = logging.FileHandler(logFiles,mode = 'a')
            file.setLevel(logging.INFO)
            # 创建一个handler,将log输出到控制台
            # consolePrint = logging.StreamHandler()
            # consolePrint.setLevel(logging.INFO)
            # 设置输出格式
            logFormat = "[%(asctime)s]: %(message)s"
    #         添加格式
            formatter = logging.Formatter(logFormat)
            file.setFormatter(formatter)
            # consolePrint.setFormatter(formatter)

    #         吧handler 添加到logger里
            self.logger.addHandler(file)
            # self.logger.addHandler(consolePrint)
    def info(self,content):

        self.logger.info(content.encode("gbk", 'ignore').decode("gbk", "ignore"))

    def error(self,content):
        self.logger.error(content)



