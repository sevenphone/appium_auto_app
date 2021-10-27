# -- coding: utf-8 --
from pages.YoudaoNote.youdaoNotePage import YouDaoNote
import allure
import pytest


@allure.feature("用例例子")
class TestYouDao:
    @allure.story("有道云笔记自动化")
    @allure.title("有道云笔记签到")
    @allure.description("描述随便写的")
    @pytest.mark.run(order=1)
    @pytest.mark.youdao_signup
    def test_youdao_daily_sign(self, driver_list):
        simulator = YouDaoNote(driver_list[0])
        simulator.close_advertisement_win()
        simulator.enter_me_page()
        simulator.deal_sign_up()
