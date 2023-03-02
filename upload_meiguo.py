import time, os
import traceback
import csv
import random
import logging
from selenium.webdriver.common.by import By
from datetime import date, datetime,timedelta
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from base.base import send_browser
from base.base import dingtalk
from base.base import get_ip


filename=r'C:\u2b\log\meiguo.log'
if not filename:
    os.mkdir(filename)
logging.basicConfig(
    filename=filename,
    level=logging.WARNING,
    format='%(levelname)s:%(asctime)s:%(message)s'
)
def get_title_content(file):
    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
        random_row = random.choice(rows)
        title = random_row[0]
        content = random_row[1]
        return title, content


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


def main(video_dir,title_file):
    now = datetime.utcnow()+timedelta(hours=8)
    try:
        bot = send_browser()
        file_name_lst = sorted(os.listdir(video_dir))
        for n, filename in enumerate(file_name_lst, 1):
            title, content = get_title_content(title_file)
            upload_video(bot, video_dir, filename, title, content)
            break
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        msg = "{}失败".format(now) + err_msg + "\n美国IP:{}".format(get_ip())
        logging.error(msg)
        dingtalk("美国上传失败，日期{}".format(now), "13143351231")


if __name__ == "__main__":
    video_dir = r"C:\Users\Administrator\Desktop\upload_videos"
    title_file = r'C:\u2b\title_content.csv'
    if not os.path.exists(video_dir):
        os.mkdir(video_dir)

    now_hour = datetime.utcnow().hour - 6
    # if now_hour in (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22):
    if now_hour in (7, 12, 19, 23):
        main(video_dir,title_file)
