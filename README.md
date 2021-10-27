# APPIUM-AUTO-APP

### 一、介绍
pytest+appium 安卓自动化项目

### 二、软件架构
```
┌ common  
│   └ 基础方法  
│       └ BasePage.py 封装基本方法  
├ config  
│   └ 配置文件  
│       └ devices.yaml 管理测试机  
│       └ env.py 环境变量  
├ logs  
│   └ 日志报告  
├ pages  
│   └ 页面元素  
│       └ 继承BasePage编写对应page的文件  
├ report  
│   └ allure报告  
├ result  
│   └ html报告  
├ screen  
│   └ 截图文件
├ static  
│   └ 存储文件,如需上传的图片等(暂未使用)  
├ testcases  
│   └ 业务测试用例  
│       ├ conftest.py 公共操作文件(如登录)  
│       ├ test开头或结尾的测试用例  
│       └ run.py 用例启动文件  
├ utils  
└   └ 辅助功能函数  
```

### 三、安装教程
1. `pip install -r requirements.txt`
2. 给`appium`的安装路径配置环境变量,  
   如`APPIUM_HOME = 'C:\Users\XX\AppData\Local\Programs\Appium\resources\app\node_modules\appium\lib'`,  
   注意`android sdk`的环境变量名要配置为`ANDROID_HOME`
3. `config\devices.yaml`添加自己的设备,  
   `testcases\conftest.py`中会根据devices.yaml来启动设备,返回driver_list,测试用例里传入driver来控制操作对应设备  
4. `config\env.py`是存储环境变量的文件，如账号密码等，可酌情使用  

### 四、使用说明
1. Page-Object设计思想
2. testcases/run.py启动测试
3. 如果项目第一次跑报错,请根据架构创建对应缺少的文件夹
4. 项目中会用命令行启动appium服务,可不手动启动appium_desktop,具体看`utils\appium_util.py`文件  
5. pytest格式限制：  
5.1 测试用例文件是用test_开头或_test结尾的py文件  
5.2 测试用例的类用Test开头,测试类中不应该有构造函数  
5.3 测试用例中的方法用test_开头  
6. `testcases\conftest.py`只提供调起driver等非业务的公共方法，如果是业务的公共操作如登录，
   建议在`testcases`子目录下新增`conftest.py`，如`testcases\test_sd\conftest.py`里就是声洞的登录操作  