import os
import pytest
import time
from config import pathconf
from utils import file_util

if __name__ == '__main__':
    current_date = time.strftime("%Y-%m-%d")
    current_time = time.strftime("%Y-%m-%d_%H%M%S")
    html_report = file_util.return_full_file(pathconf.result_dir, current_date, f"{current_time}.html")
    # 目前使用allure报告,可以不打开html报告生成
    allure_report = file_util.return_full_file(pathconf.report_dir, current_date, current_time)
    pytest.main(['./',  # 指定用例文件 ./指当前文件所在目录的所有test开头和结尾的py文件
                 '-s',  # 控制台输出log和print
                 '-v',  # 展示用例的具体信息，文件:类:方法
                 '-m', 'youdao_signup',  # 指定执行某些标记的用例；使用时建议注释--allure-features
                 '--count=1',  # 执行次数
                 # '--reruns', '1',  # 失败重试次数
                 '--html=' + html_report, '--self-contained-html',  # 生成html报告,目前使用allure报告,建议不打开html报告生成
                 '--alluredir=' + allure_report,  # 生成allure报告
                 # '--allure-features', "用例例子",  # 运行某个模块的测试用例；使用时建议注释-m
                 # '--disable-warnings',  # 忽略pytest的warning
                 '--cache-clear'  # 清空pytest缓存文件
                 ])
    os.system('start /b allure serve ' + allure_report)  # 打开allure报告
