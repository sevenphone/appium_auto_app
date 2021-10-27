# -- coding: utf-8 --
import time
from appium import webdriver
from utils.appium_util import AppiumServer
nameDriverDict = {}


def my_driver(desired_caps: dict, port: int = 4723):
    """建立设备与appium连接,返回对应webdriver"""
    AppiumServer.start_appium_server(desired_caps["udid"], port)
    time.sleep(2)
    driver = webdriver.Remote(f'http://127.0.0.1:{str(port)}/wd/hub', desired_caps)
    nameDriverDict[desired_caps["udid"]] = driver
    return driver


def get_name_from_webdriver(driver) -> str:
    """根据webdriver返回对应设备udid"""
    name = str()
    for k, v in nameDriverDict.items():
        if v == driver:
            name = k
    return name


def clear_driver_name_dict():
    """结束后清空nameDriverDict"""
    nameDriverDict.clear()
