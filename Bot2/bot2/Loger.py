# coding:utf-8
import logging
class Log():
    def __init__(self,app_name=''):
        self.logger = logging.getLogger(app_name)
        logging.basicConfig(level=logging.INFO)
        self.file_handler = logging.FileHandler('Info.log')
        self.file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        self.logger.addHandler(self.file_handler)

    def getlog(self):
        return self.logger