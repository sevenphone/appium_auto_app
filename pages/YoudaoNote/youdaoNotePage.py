# -- coding: utf-8 --
from common.BasePage import BasePage
from appium.webdriver.common.mobileby import MobileBy
import allure


class YouDaoNote(BasePage):
    advertisement_close_btn = ['//android.widget.ImageView', MobileBy.XPATH]
    me_tab = ['//*[contains(@resource-id, "tab_name") and @text="我的"]', MobileBy.XPATH]
    sign_in_btn = 'sign_in'
    sign_win_text = 'sign_result'
    finish_sign_btn = 'btn_ok'

    @allure.step("关闭广告弹窗")
    def close_advertisement_win(self):
        ele_list = self.find_elements(self.advertisement_close_btn[0], by=self.advertisement_close_btn[1])
        if len(ele_list) == 2:
            ele_list[1].cick()

    @allure.step("进入我的页面")
    def enter_me_page(self):
        self.click(self.me_tab[0], by=self.me_tab[1])

    @allure.step("完成签到操作")
    def deal_sign_up(self):
        self.click(self.sign_in_btn)
        win_text = self.find_element(self.sign_win_text).text
        assert '今日已签到' == win_text, "判断签到完成弹窗出现"
        self.click(self.finish_sign_btn)
