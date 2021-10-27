# -- coding: utf-8 --
import os.path
import pytest
from common.BasePage import BasePage
from common.GetDriver import *
from config import pathconf, env
from utils.appium_util import AppiumServer
from utils.file_util import read_yaml
_driver_list = []


@pytest.fixture()
def driver_list():
    """启动appium服务
    :return: 返回devices.yaml文件内配置数量的driver list
    """
    # global _driver_list
    device_info = read_yaml(os.path.join(pathconf.config_dir, "devices.yaml"))
    for index in range(len(device_info)):
        desired_caps = device_info[index]["desired_caps"]
        port = device_info[index]["port"]
        desired_caps["platformVersion"] = str(desired_caps.pop("platformVersion"))  # 有时候读取出来是int或float，统一处理转str
        desired_caps["automationName"] = 'UiAutomator2'    # 默认使用UiAutomator2
        desired_caps["systemPort"] = port + 3480    # systemPort用于设备并发操作，要注意systemPort范围是8200~8299
        desired_caps["unicodeKeyboard"] = True      # 支持输入中文
        desired_caps["resetKeyboard"] = True        # 测试完成后恢复设备原输入法
        if ("noReset" not in desired_caps) or (not desired_caps["noReset"]):    # 应用需要重置下面自动授权才会生效
            desired_caps["autoGrantPermissions"] = True  # 自动授权app权限,但国内各大安卓系统不一定好使
        _driver_list.append(my_driver(desired_caps, port))
    return _driver_list


def pytest_configure(config):
    """测试用例标记添加"""
    mark_list = ["youdao_signup"]
    for mark in mark_list:
        config.addinivalue_line("markers", mark)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """测试结束后关闭driver和appium服务"""
    result = yield
    rep = result.get_result()
    # setup -> call -> teardown # call是用例执行完成的阶段,当用例rerun的时候会走到teardown但当时不会走到call(踩坑了)
    if rep.when == 'teardown':
        if len(_driver_list) > 0:
            for i in range(len(_driver_list)):
                BasePage(_driver_list[i]).close_driver()
        AppiumServer.stop_appium_server()
        time.sleep(2)
        clear_driver_name_dict()
        _driver_list.clear()    # 清空旧的driver list,以免影响下一个测试用例driver = driver_list[0]


# def pytest_addoption(parser):
#     parser.addoption('--reruns')  # pytest增加自定义命令
