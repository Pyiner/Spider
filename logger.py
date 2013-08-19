#coding=utf-8
import  logging

formatter_dict = {
    1 : logging.Formatter("%(message)s"),
    2 : logging.Formatter("%(levelname)s - %(message)s"), 
    3 : logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"),
    4 : logging.Formatter("%(asctime)s - %(levelname)s - %(message)s - [%(name)s]"),
    5 : logging.Formatter("%(asctime)s - %(levelname)s - %(message)s - [%(name)s:%(lineno)s]")
}

class Logger(object):
    def __init__(self, logname, loglevel, callfile):
        """
            指定日志文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        """
        self.logger = logging.getLogger(callfile)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logname)

        fh.setFormatter(formatter_dict[int(loglevel)])
        self.logger.addHandler(fh)

    @property
    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    logger = Logger(logname='hahaha', loglevel=1,callfile='l.txt')
    logger.get_logger.info('test level1')
