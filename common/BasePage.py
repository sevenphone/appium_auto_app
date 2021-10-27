# -- coding: utf-8 --
import allure
from selenium.common.exceptions import TimeoutException, InvalidSelectorException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By as OriginalBy
from appium.webdriver.common.mobileby import MobileBy as By
from selenium.webdriver.support import expected_conditions as EC
from common import logger, GetDriver
from config import pathconf
from utils import math_util, file_util
import time
import logging


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver_name = GetDriver.get_name_from_webdriver(driver)

    def wait_element_exist(self, location: str, timeout: int = 20, by: str = By.ID):
        """等待元素在页面中可见
        :param location: 元素定位表达式
        :param timeout: 超时时间，默认20s
        :param by: 元素定位方式，默认采用id/resource-id定位方式
        """
        logging.info(f"设备{self.driver_name}等待元素：{location}可见，定位方式为：{by}")
        if (by not in By.__dict__.values()) and (by not in OriginalBy.__dict__.values()):
            logging.error(f"ERROR：元素定位方式：{by}错误")
        try:
            # 元素是否可见
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, location)))
            # 元素是否存在页面中
            # WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, location)))
            logging.info(f"元素：{location}已可见")
        except TimeoutException as e:
            self.screen_shot()
            logging.error(f"ERROR：等待元素：{location}可见超时\n", exc_info=True)
            raise e
        except InvalidSelectorException as e:
            self.screen_shot()
            logging.error(f"ERROR：元素表达式：{location}错误\n", exc_info=True)
            raise e
        except Exception as e:
            self.screen_shot()
            logging.error(f"ERROR：发生其他异常，等待元素：{location}可见失败\n", exc_info=True)
            raise e

    def find_element(self, location: str, timeout: int = 20, by: str = By.ID):
        """查找单个元素
        :param location: 元素定位表达式
        :param timeout: 超时时间，默认20s
        :param by: 元素定位方式，默认采用id/resource-id定位方式
        :return: 找到的元素
        """
        logging.info(f"设备{self.driver_name}开始查找元素：{location}，定位方式为：{by}")
        try:
            self.wait_element_exist(location, timeout, by)
            result = self.driver.find_element(by, location)
            logging.info(f"元素：{location}查找成功")
            return result
        except Exception as e:
            self.screen_shot()
            logging.error(f"ERROR：元素：{location}查找失败\n", exc_info=True)
            raise e

    def find_elements(self, location: str, timeout: int = 20, by: str = By.ID):
        """查找一组元素
        :param location: 元素定位表达式
        :param timeout: 超时时间，默认20s
        :param by: 元素定位方式，默认采用id/resource-id定位方式
        :return: 找到的元素list
        """
        logging.info(f"设备{self.driver_name}开始查找一组元素：{location}")
        try:
            self.wait_element_exist(location, timeout, by)
            result = self.driver.find_elements(by, location)
            logging.info(f"一组元素：{location}查找成功，且找到{len(result)}个元素")
            return result
        except Exception as e:
            self.screen_shot()
            logging.error(f"ERROR：一组元素：{location}查找失败\n", exc_info=True)
            raise e

    def click(self, location: str, timeout: int = 20, by: str = By.ID, scroll_down_2_find: bool = False):
        """对元素进行点击操作
        :param location: 元素定位表达式
        :param timeout: 超时时间，默认20s
        :param by: 元素定位方式，默认采用id/resource-id定位方式
        :param scroll_down_2_find: 是否需要下滑页面查找元素，默认不需要
        """
        if scroll_down_2_find:
            ele = self.scroll_to_find_element_exist(location, timeout, by)
        else:
            logging.info(f"设备{self.driver_name}开始操作点击元素：{location}，定位方式为：{by}")
            ele = self.find_element(location, timeout, by)

        try:
            ele.click()
            logging.info(f"操作元素：{location}点击成功")
        except Exception as e:
            self.screen_shot()
            logging.error(f"ERROR：操作元素：{location}点击失败\n", exc_info=True)
            raise e

    def double_click(self, coordinate: list = None, location: str = None, timeout: int = 20, by: str = By.ID):
        """对元素进行双击操作，如抖音点赞；支持坐标或元素定位两种方式
        :param coordinate: 要操作的坐标，如[123, 456]；用坐标则不传定位表达式
        :param location: 元素定位表达式；用定位表达式则不传坐标；都传了则以location为主
        :param timeout: 超时时间，默认20s
        :param by: 元素定位方式，默认采用id/resource-id定位方式
        """
        if location is not None:
            logging.info(f"设备{self.driver_name}开始操作双击元素{location}，定位方式：{by}")
            ele = self.find_element(location, timeout, by)
            try:
                self.driver.tap(element=ele, count=2)
                logging.info(f"操作元素：{location}双击成功")
            except Exception as e:
                self.screen_shot()
                logging.error(f"ERROR：操作元素{location}双击失败\n", exc_info=True)
                raise e
        else:
            logging.info(f"设备{self.driver_name}开始对{str(coordinate)}操作双击")
            try:
                self.driver.tap(x=coordinate[0], y=coordinate[1], count=2)
                logging.info(f"对{coordinate}操作双击成功")
            except Exception as e:
                self.screen_shot()
                logging.error(f"ERROR：对{coordinate}操作双击失败\n", exc_info=True)
                raise e

    def is_element_exist(self, location: str, timeout: int = 5, by: str = By.ID, can_not_catch: bool = False):
        """判断元素是否存在（默认判断是否在页面中可见）
        :param location: 元素定位表达式
        :param timeout: 超时时间，默认5s
        :param by: 元素定位方式，默认采用id/resource-id定位方式
        :param can_not_catch: 元素是否无法在appium-desktop中捕抓；默认false，若true则判断元素存在于页面中而非在页面可见
        :return: 存在返回true，不存在或超时仍找不到返回false
        """
        logging.info(f"设备{self.driver_name}开始检查元素：{location}是否存在，定位方式为：{by}")
        try:
            if can_not_catch:
                logging.info(f"元素{location}是个toast提示，判断元素是否存在于页面中")
                WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, location)))
            else:
                logging.info(f"元素{location}是个可见元素，判断元素是否在页面中可见")
                WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, location)))
            result = True
        except Exception:
            result = False
        logging.info(f"检查元素：{location}是否存在，结果为{result}")
        return result

    def scroll_to_find_element_exist(self, location: str, timeout: int = 10, by: str = By.ID):
        """往下查找元素
        :param location: 元素定位表达式
        :param timeout: 停留在页面内查找元素的超时时间，默认10s
        :param by: 元素定位表达式，默认采用id/resource-id定位方式
        :return: 滑到最底部仍没有找到返回"ERR"；在页面内找到了则返回对应的元素
        """
        if not self.is_element_exist(location, timeout, by):
            logging.info(f"当前页面没有找到元素：{location}，开始进行往下查找")
            before_swipe = self.driver.page_source
            self.swipe_to_up()
            time.sleep(1)
            after_swipe = self.driver.page_source
            if before_swipe != after_swipe:
                logging.info(f"滑动成功，继续查找元素：{location}")
                return self.scroll_to_find_element_exist(location, timeout, by)
            else:
                logging.error(f"已经滑动到了最底部，还没有找到元素：{location}")
                return "ERR"
        else:
            logging.info(f"已在当前页面找到了元素：{location}，无需继续下滑页面")
            return self.find_element(location, timeout, by)

    def get_size(self):
        """获取屏幕尺寸
        :return: 屏幕尺寸
        """
        logging.info("开始获取屏幕尺寸")
        try:
            size = self.driver.get_window_size()
            logging.info(f"屏幕尺寸为{size}")
            return size
        except Exception as e:
            self.screen_shot()
            logging.error("ERROR：获取屏幕尺寸失败\n", exc_info=True)
            return None

    def swipe_to_left(self):
        """向左滑"""
        logging.info(f"设备{self.driver_name}开始操作左滑")
        size = self.get_size()
        width = size.get('width')
        height = size.get('height')
        try:
            self.driver.swipe(width*0.2, height*0.5, width*0.9, height*0.5)
            logging.info("操作左滑成功")
            time.sleep(0.5)
        except Exception as e:
            self.screen_shot()
            logging.error("ERROR：左滑失败\n", exc_info=True)

    def swipe_to_right(self):
        """向右滑"""
        logging.info(f"设备{self.driver_name}开始操作右滑")
        size = self.get_size()
        width = size.get('width')
        height = size.get('height')
        try:
            self.driver.swipe(width*0.9, height*0.5, width*0.2, height*0.5)
            logging.info("操作右滑成功")
            time.sleep(0.5)
        except Exception as e:
            self.screen_shot()
            logging.error("ERROR：右滑失败\n", exc_info=True)

    def swipe_to_up(self):
        """向上滑"""
        logging.info(f"设备{self.driver_name}开始操作往上滑")
        size = self.get_size()
        width = size.get('width')
        height = size.get('height')
        try:
            self.driver.swipe(width*0.5, height*0.7, width*0.5, height*0.3)
            logging.info("操作上滑成功")
            time.sleep(0.5)
        except Exception as e:
            self.screen_shot()
            logging.error("ERROR：上滑失败\n", exc_info=True)

    def swipe_to_down(self):
        """向下滑、下拉刷新"""
        logging.info(f"设备{self.driver_name}开始操作往下滑")
        size = self.get_size()
        width = size.get('width')
        height = size.get('height')
        try:
            self.driver.swipe(width*0.5, height*0.3, width*0.5, height*0.7)
            logging.info("操作下滑成功")
            time.sleep(0.5)
        except Exception as e:
            self.screen_shot()
            logging.error("ERROR：下滑失败\n", exc_info=True)

    def finish_input(self):
        """收起键盘结束输入状态"""
        try:
            self.driver.execute_script("mobile:performEditorAction", {"action": "done"})    # 点键盘上的完成
            logging.info(f"设备{self.driver_name}执行收起键盘结束输入状态成功")
        except Exception:
            logging.error("ERROR：执行收起键盘结束输入状态失败\n", exc_info=True)

    def press_keycode(self, keycode: int):
        """设备键盘操作,可模拟操作特定按键或输入等,用于不能send_keys的情况来进行输入
        :param keycode: 要输入的按键码，数字或字母的按键码请看utils.math_util.get_keycode()
        """
        logging.info(f"设备{self.driver_name}开始操作输入指令码{str(keycode)}")
        try:
            self.driver.press_keycode(keycode)
            logging.info("输入指令码成功")
        except Exception:
            logging.error("ERROR：操作输入指令码失败\n", exc_info=True)

    def execute_back(self):
        """操作返回键"""
        logging.info(f"设备{self.driver_name}开始操作返回")
        try:
            # self.driver.press_keycode(4)
            self.press_keycode(4)
            logging.info("操作返回成功")
            time.sleep(1)
            # self.driver.keyevent(4)
        except Exception as e:
            self.screen_shot()
            logging.error("ERROR：操作返回失败\n", exc_info=True)
            raise e

    def execute_home(self):
        """操作HOME键"""
        logging.info(f"设备{self.driver_name}开始操作返回HOME")
        try:
            # self.driver.press_keycode(3)
            self.press_keycode(3)
            logging.info("操作返回HOME成功")
            time.sleep(1)
            # self.driver.keyevent(3)
        except Exception as e:
            self.screen_shot()
            logging.error("ERROR：操作返回HOME失败\n", exc_info=True)

    def screen_shot(self, write_error_log: bool = True):
        """截图操作
        :param write_error_log: 是否需要写错误日志并将截图插入allure报告
        """
        t = time.strftime("%Y-%m-%d_%H%M%S")
        d = time.strftime("%Y-%m-%d")
        filename = file_util.return_full_file(pathconf.screen_dir, d, f"SCT_{t}_{math_util.random_str(4)}.png")
        self.driver.get_screenshot_as_file(filename)
        if write_error_log:
            logging.error(f"已截图，请注意查看文件{filename}")
            with open(filename, mode='rb') as f:
                allure.attach(f.read(), filename, allure.attachment_type.PNG)   # 错误截图加入allure报告中
        else:
            logging.info(f"截图成功,请注意查看文件{filename}")

    def switch_application(self, package: str, activity: str):
        """切换应用
        :param package: 要切换到的应用的appPackage
        :param activity: 要切换到的应用的appActivity
        """
        logging.info(f"设备{self.driver_name}开始执行切换至应用{package}")
        try:
            self.driver.start_activity(package, activity)
            logging.info(f"切换至应用{package}成功")
        except Exception as e:
            logging.error(f"ERROR：切换应用{package}失败\n", exc_info=True)
            raise e

    def click_by_coordinates(self, coordinate_list: list, duration: int = None, sleep_time: int = 1):
        """根据坐标进行点击
        :param coordinate_list: 坐标的列表(最多支持5个手指，即为5组坐标)
        :param duration: 点击按住的时长(毫秒)
        :param sleep_time: 点击后缓冲时长，默认1s
        """
        logging.info(f"设备{self.driver_name}开始执行根据坐标{coordinate_list}点击")
        try:
            self.driver.tap(positions=coordinate_list, duration=duration)
            time.sleep(sleep_time)
            logging.info(f"根据坐标{coordinate_list}点击成功")
        except Exception:
            logging.error(f"ERROR：执行根据坐标{coordinate_list}点击失败\n", exc_info=True)

    def swipe_by_coordinates(self, start_coordinate_list: list, end_coordinate_list: list, duration: int = 0):
        """根据坐标进行移动
        :param duration: 执行移动所需时间，单位是毫秒
        :param start_coordinate_list: 起始坐标 [start_x,start_y]
        :param end_coordinate_list: 终点坐标 [end_x,end_y]
        """
        logging.info(f"设备{self.driver_name}开始执行根据坐标{start_coordinate_list}移动到{end_coordinate_list}")
        try:
            self.driver.swipe(start_coordinate_list[0], start_coordinate_list[1],
                              end_coordinate_list[0], end_coordinate_list[1], duration)
            logging.info(f"执行根据坐标移动成功")
        except Exception:
            logging.error("ERRPR：执行根据坐标移动失败\n", exc_info=True)

    def close_driver(self):
        """关闭当前应用"""
        logging.info("开始执行关闭driver驱动")
        try:
            self.driver.close_app()
            self.driver.quit()
            logging.info("关闭driver驱动成功")
        except Exception:
            logging.error("ERROR：执行关闭驱动失败\n", exc_info=True)
