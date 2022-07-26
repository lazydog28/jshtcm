# -*- coding: utf-8 -*-
# @Time : 2022年03月15日 21时24分
# @Email : yun981128@gmail.com
# @Author : 王从赟
# @Project :ToolKit
# @File : Logger.py
# @notice :
# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         log_color
# Author:       yunhgu
# Date:         2022/2/25 13:52
# Description:
# -------------------------------------------------------------------------------
import logging, os, time
from logging.handlers import RotatingFileHandler

import colorlog

# 定义不同日志等级颜色
log_colors_config = {
    "DEBUG": "bold_cyan",
    "INFO": "bold_green",
    "WARNING": "bold_yellow",
    "ERROR": "bold_red",
    "CRITICAL": "red",
}


class Logger(logging.Logger):
    def __init__(self, name, level="DEBUG", file=None, encoding="utf-8"):
        rq = time.strftime("%Y%m%d", time.localtime(time.time()))

        logfile = "log/" + rq + "-" + name + ".log"
        current_path = os.getcwd()
        path = current_path + "/log"
        if not os.path.exists(path):
            os.makedirs(path)
        super().__init__(name)
        self.encoding = encoding
        self.file = file
        self.level = level
        # 针对所需要的日志信息 手动调整颜色
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s:%(asctime)s [%(filename)s:%("
            "lineno)d]%(log_color)s:%(message)s",
            reset=True,
            log_colors=log_colors_config,
            secondary_log_colors={
                "message": {
                    "DEBUG": "blue",
                    "INFO": "blue",
                    "WARNING": "blue",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                }
            },
            style="%",
        )  # 日志输出格式
        # 创建一个FileHandler，用于写到本地
        rotatingFileHandler = logging.handlers.RotatingFileHandler(
            filename=logfile, maxBytes=1024 * 1024 * 50, backupCount=5, encoding="utf-8"
        )
        rotatingFileHandler.setFormatter(
            logging.Formatter(
                "%(levelname)-8s : %(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s"
            )
        )
        rotatingFileHandler.setLevel(logging.DEBUG)
        self.addHandler(rotatingFileHandler)

        # 创建一个StreamHandler,用于输出到控制台
        console = colorlog.StreamHandler()
        console.setLevel(logging.ERROR)
        console.setFormatter(formatter)
        self.addHandler(console)
        self.setLevel(logging.DEBUG)


if __name__ == "__main__":
    logger = Logger("测试")
    logger.info("log")
    logger.error("log")
    logger.debug("log")
    logger.warning("WARNING")
