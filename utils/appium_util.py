# -- coding: utf-8 --
import os
import logging


class AppiumServer:
    @staticmethod
    def start_appium_server(device_name: str, port: int = 4723):
        """启动appium服务，如果端口被占用视为手动启动了appium desktop"""
        # appium_home = r'C:\Users\XX\AppData\Local\Programs\Appium\resources\app\node_modules\appium\build\lib'
        if port is not None and device_name is not None:
            is_port_used = os.popen(f'netstat -ano | findstr {port}').read()
            if 'LISTENING' not in is_port_used:
                logging.info(f"端口{port}未被占用，开始启动appium服务")
                # os.system(r'start /b node %APPIUM_HOME%\main.js -p={port} -bp={bp} -U={udid}'
                #           .format(port=port, bp=(port - 2000), udid=device_name))  # Bootstrap是基于UiAutomator1的
                os.system(r'start /b node %APPIUM_HOME%\main.js -p={port} -U={udid}'
                          .format(port=port, udid=device_name))
            else:
                logging.info(f"端口{port}已被占用，视为appium服务已启动")

    @staticmethod
    def stop_appium_server():
        """关闭命令行启动的appium服务"""
        logging.info("执行关闭appium服务")
        try:
            os.system(r'start /b taskkill /F /t /IM node.exe')
            logging.info("关闭appium服务成功")
            print("关闭appium服务成功")
        except Exception:
            logging.error("ERROR：关闭appium服务失败\n", exc_info=True)


if __name__ == '__main__':
    AppiumServer.stop_appium_server()
