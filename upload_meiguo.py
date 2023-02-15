import json
import socket
import time, os
import traceback
import csv
import random
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def send_browser():
    try:
        os.system('taskkill /im chromedriver.exe /F')
        os.system('taskkill /im chrome.exe /F')
        options = Options()
        options.add_argument("--lang=en")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome Beta\\User Data")
        options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        service = Service(executable_path=r"C:\Program Files\Google\Chrome Beta\Application\chromedriver.exe")
        bot = webdriver.Chrome(service=service, options=options)
        return bot
    except Exception as e:
        print(e.args)
        os.system('taskkill /im chromedriver.exe /F')
        os.system('taskkill /im chrome.exe /F')


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


def get_ip():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def get_title_content(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        random_row = random.choice(rows)
        return random_row[0], ','.join(random_row[1:])


def upload_video(bot, video_dir, nameofvid, title, content):
    try:
        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(5)

        file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
        simp_path = '{}/{}'.format(video_dir, nameofvid)
        abs_path = os.path.abspath(simp_path)
        file_input.send_keys(abs_path)
        time.sleep(7)

        # 标题
        title_xpath = '//ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input//*[@id="textbox"]'
        title_input = bot.find_element(By.XPATH, title_xpath)
        title_input.clear()
        title_input.send_keys(title)
        time.sleep(5)

        # 描述
        # description = nameofvid.split('_')[:-1]
        description = content
        description_xpath = '//*[@id="description-textarea"]//*[@id="textbox"]'
        description_input = bot.find_element(By.XPATH, description_xpath)
        description_input.clear()
        description_input.send_keys(description)
        time.sleep(1)

        # 选择频道
        item_down_xpath = '//*[@id="basics"]/div[4]/div[3]/div[1]/ytcp-video-metadata-playlists/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div'
        # 下拉框
        item_input = bot.find_element(By.XPATH, item_down_xpath)
        item_input.click()
        time.sleep(1)
        item_select_xpath = '//span[text()="A Dreamy Landscape"]'
        item_select = wait(bot, 10).until(EC.presence_of_element_located((By.XPATH, item_select_xpath)))
        item_select.click()
        time.sleep(2)

        # 完成
        complete_xpath = '//div[text()="Done"]'
        complete_ele = bot.find_element(By.XPATH, complete_xpath)
        complete_ele.click()
        time.sleep(1)
        # 继续
        next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
        for i in range(3):
            next_button.click()
            time.sleep(5)

        done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
        done_button.click()
        time.sleep(5)
        bot.quit()
        os.remove(os.path.join(video_dir, nameofvid))
    except Exception as e:
        print(traceback.format_exc())


def main(video_dir):
    today = date.today()
    try:
        bot = send_browser()
        file_name_lst = sorted(os.listdir(video_dir))
        for n, filename in enumerate(file_name_lst, 1):
            title_file = r"C:\u2b\title_content.csv"
            title, content = get_title_content(title_file)
            upload_video(bot, video_dir, filename, title, content)
            break
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        msg = "{}失败".format(today) + err_msg + "\n美国IP:{}".format(get_ip())
        dingtalk(msg, "13143351231")


if __name__ == "__main__":
    # 11点开始奇数发布
    import datetime

    video_dir = r"C:\Users\Administrator\Desktop\upload_videos"
    if not os.path.exists(video_dir):
        os.mkdir(video_dir)

    now_hour = datetime.datetime.now().hour
    # if now_hour in (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22):
    if now_hour in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23):
        main(video_dir)
