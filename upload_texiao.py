import time, os
import logging
import traceback
from selenium.webdriver.common.by import By
from datetime import date, datetime

from base.base import dingtalk
from base.base import send_browser
from base.base import get_ip


def upload_video(bot, video_dir, nameofvid, title, content):
    try:
        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(5)

        file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
        abs_path = video_dir + "\{}".format(str(nameofvid))
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
        bot.quit()


def main(video_dir):
    today = datetime.now()
    try:
        bot = send_browser()
        for filename in os.listdir(video_dir):  # ‘logo/’是文件夹路径，你也可以替换其他
            title = "感悟人生"
            content = filename.split('_')[:-1]
            upload_video(bot, video_dir, filename, title, content)
            break
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        logging.error(err_msg)
        msg = "{},失败" + err_msg + "IP:{}".format(today, get_ip())
        dingtalk(msg, "13143351231")


if __name__ == "__main__":
    upload_videos_dir = r"C:\Users\Administrator\Desktop\hongkong_videos"
    now_hour = datetime.now().hour
    # main(upload_videos_dir)
    if now_hour in (11, 15, 19, 21):
        main(upload_videos_dir)
