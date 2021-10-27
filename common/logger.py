# -- coding: utf-8 --
import logging
from config import pathconf
import time
from logging.handlers import RotatingFileHandler
from utils import file_util


fmt = "%(asctime)s  %(levelname)s %(filename)s %(funcName)s [ line:%(lineno)d ] %(message)s"

datefmt = '%Y-%m-%d %H:%M:%S'
handle_1 = logging.StreamHandler()

cur_time = time.strftime("%Y-%m-%d_%H%M")
cur_date = time.strftime("%Y-%m-%d")

log_file_name = file_util.return_full_file(pathconf.log_dir, cur_date, f"LOG_{cur_time}.log", create_file=True)

handle_2 = RotatingFileHandler(log_file_name, backupCount=20, encoding="UTF-8")
# noinspection PyArgumentList
logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.INFO, handlers=[handle_1, handle_2])
