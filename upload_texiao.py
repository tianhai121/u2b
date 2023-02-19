
import time, os
import logging
import traceback
from selenium.webdriver.common.by import By
from datetime import date, datetime

from base.base import dingtalk
from base.base import send_browser
from base.base import get_ip


def upload_video(bot, video_dir, nameofvid):
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
            upload_video(bot, video_dir, filename)
            break
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        logging.error(err_msg)
        msg = "{},失败" + err_msg + "IP:{}".format(today, get_ip())
        dingtalk(msg, "13143351231")


if __name__ == "__main__":
    upload_videos_dir = r"C:\Users\Administrator\Desktop\upload_videos_out"
    now_hour = datetime.now().hour
    main(upload_videos_dir)
    if now_hour in (11, 13, 15, 17, 19, 21):
        main(upload_videos_dir)
