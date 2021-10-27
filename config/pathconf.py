# -- coding: utf-8 --
import os
import sys


if sys.platform == "win32":
    base_dir = os.path.dirname(os.path.dirname(__file__)).replace("/", "\\")
else:
    base_dir = os.path.dirname(os.path.dirname(__file__))

log_dir = os.path.join(base_dir, "logs")
report_dir = os.path.join(base_dir, "report")
result_dir = os.path.join(base_dir, "result")
screen_dir = os.path.join(base_dir, "screen")
static_dir = os.path.join(base_dir, "static")
testcase_dir = os.path.join(base_dir, "testcases")
utils_dir = os.path.join(base_dir, "utils")
config_dir = os.path.join(base_dir, "config")
