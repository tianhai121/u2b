# coding:utf-8
import json
import os
import socket

import requests
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

project_dir = os.getcwd()
logging.basicConfig(
    filename=os.path.join(project_dir, 'log/log/log'),
    level=logging.WARNING,
    format='%(levelname)s:%(asctime)s:%(message)s'
)


# 钉钉预警
def dingtalk(msg, ding_bodys):
    webhook = "https://oapi.dingtalk.com/robot/send?access_token" \
              "=86addaf9ad29dd428ccdffcb16469f0809a1d0389c72fe3bce320c0f04396c88"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    data = {
        'msgtype': 'text', 'text': {'title': "自动上传油管", "content": msg},
        'at': {'atMobiles': ding_bodys, 'isAtAll': False}
    }
    post_data = json.dumps(data)
    response = requests.post(webhook, headers=headers, data=post_data)
    return response.text


def send_browser():
    try:
        # 列出所有正在运行的进程
        tasklist_output = os.popen('tasklist').read()
        # 搜索名为"chromedriver.exe"的进程
        if 'chromedriver.exe' in tasklist_output or 'chrome.exe' in tasklist_output:
            # 关闭名为"chromedriver.exe"的进程
            os.system('taskkill /f /im chromedriver.exe')
            os.system('taskkill /f /im chrome.exe')

        options = Options()
        options.add_argument("--lang=en")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument("--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome Beta\\User Data")
        options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        options.add_argument(
            "--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome Beta\\User Data\\Default")
        service = Service(executable_path=r"C:\Program Files\Google\Chrome Beta\Application\chromedriver.exe")
        bot = webdriver.Chrome(service=service, options=options)
        return bot
    except Exception as e:
        print(e.args)
        logging.error(e.args)
        os.system('taskkill /im chromedriver.exe /F')
        os.system('taskkill /im chrome.exe /F')


def get_ip():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr