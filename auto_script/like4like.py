import logging
import os

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time, json,traceback


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


class AMFBot:
    def __init__(self, twitter_user, twitter_pwd):
        self.twitter_user = twitter_user
        self.twitter_pwd = twitter_pwd

    def send_browser(self, user_data_dir):
        try:
            options = Options()
            prefs = {
                'profile.default_content_setting_values':
                    {
                        'notifications': 2
                    }
            }
            options.add_experimental_option('prefs', prefs)
            options.add_argument("--lang=en")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
            options.add_argument(user_data_dir)
            service = Service(executable_path=r"C:\Program Files\Google\Chrome Beta\Application\chromedriver.exe")
            bot = webdriver.Chrome(service=service, options=options)
            return bot
        except Exception as e:
            print(e.args)
            logging.error(e.args)

    # 登like4like网站
    def open(self, bot):
        bot.get("https://www.like4like.org/")
        bot.maximize_window()
        # Load the cookies from the JSON file
        with open('../cookies.json', 'r') as f:
            cookies = json.load(f)
            # Add the cookies to the non-headless browser
        for cookie in cookies:
            bot.add_cookie(cookie)
        time.sleep(3)
        # Refresh the page
        bot.refresh()
        time.sleep(3)
        self.earn_twitter_favorites(bot)

    # 获取积分
    def earn_twitter_favorites(self, bot):
        url_twitter_favorites = "https://www.like4like.org/user/earn-twitter-favorites.php"
        bot.get(url_twitter_favorites)
        time.sleep(5)
        flag = True
        while flag:
            bot.find_element(By.CSS_SELECTOR, "a[class^='cursor earn_pages_button profile_view_img']").click()
            time.sleep(5)
            bot.switch_to.window(bot.window_handles[1])
            try:
                # # 取消通知
                # notice_path = '//*[@id="layers"]//span//span[text()="Turn on notifications"]'
                # notice_xpath = WebDriverWait(bot, 20).until(
                #     EC.presence_of_element_located((By.XPATH, notice_path))
                # )
                # if notice_xpath:
                #     notice_xpath.click()
                #     time.sleep(1)
                # 点击喜欢
                time.sleep(1)
                favorite = bot.find_element(By.XPATH, '//div[@aria-label="Like"]')
                if favorite.is_displayed():
                    favorite.click()
                time.sleep(5)

                # 登录twitter
                log_btn = WebDriverWait(bot, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="group"]//span/span[text()="Log in"]'))
                )
                if log_btn.is_displayed():
                    log_btn.click()
                    usuario = WebDriverWait(bot, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
                    )
                    usuario.send_keys(self.twitter_user)
                    bot.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]').click()
                    time.sleep(3)

                    # 判断手机号是否存在
                    try:
                        phone = bot.find_element(By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']")
                        if phone.is_displayed():
                            phone.send_keys('+8613143351231')
                            bot.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]').click()
                            time.sleep(3)
                    except:
                        pass

                    senha = bot.find_element(By.XPATH, "//input[@type='password']")
                    senha.send_keys(self.twitter_pwd)
                    bot.find_element(By.XPATH,
                                     '//div[@role="button" and @data-testid="LoginForm_Login_Button"]').click()

                    # 点击喜欢
                    favorite = bot.find_element(By.XPATH, '//*[@id="id__k4q9t1g3z3d"]//div[@aria-label="Like"]')
                    if favorite.is_displayed():
                        favorite.click()
                    time.sleep(5)
                    bot.close()
                    # 点击确认
                    bot.switch_to.window(bot.window_handles[0])
                    confirm = bot.find_element(By.CSS_SELECTOR, "a[class^='cursor pulse-checkBox']")
                    if confirm.is_displayed():
                        confirm.click()
                        time.sleep(3)
                else:
                    # 点击喜欢
                    favorite = bot.find_element(By.XPATH, '//*[@id="id__k4q9t1g3z3d"]//div[@aria-label="Like"]')
                    if favorite.is_displayed():
                        favorite.click()
                    time.sleep(5)
                    bot.close()
                    # 点击确认
                    bot.switch_to.window(bot.window_handles[0])
                    confirm = bot.find_element(By.CSS_SELECTOR, "a[class^='cursor pulse-checkBox']")
                    if confirm.is_displayed():
                        confirm.click()
                        time.sleep(3)
            except:
                bot.quit()
                print(traceback.format_exc())
                flag = False
                dingtalk("获取积分失败", [13143351231])

    # 获取积分
    def twttwo(self):
        bot = self.bot
        confirm = bot.find_element(By.CSS_SELECTOR, "a[class^='cursor pulse-checkBox']")
        if confirm.is_displayed():
            confirm.click()
            time.sleep(3)
            bot.find_element(By.CSS_SELECTOR, "a[class^='cursor earn_pages_button profile_view_img']").click()
            bot.switch_to.window(bot.window_handles[1])
            # window
        else:
            bot.find_element(By.CSS_SELECTOR, "a[class^='cursor earn_pages_button profile_view_img']").click()
            bot.switch_to.window(bot.window_handles[1])
            time.sleep(5)
            # window

        try:
            follow = WebDriverWait(bot, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@role="button" and @data-testid="confirmationSheetConfirm"]'))
            )
            if follow.is_displayed():
                follow.click()
            time.sleep(5)

        except bot.NoSuchElementException:
            bot.close()
            bot.switch_to.window(bot.window_handles[0])
            time.sleep(3)
            bot.get("https://www.like4like.org/free-twitter-followers.php")
            ed.twttwo()

        # window
        bot.close()
        bot.switch_to.window(bot.window_handles[0])
        time.sleep(3)
        ed.twttwo()


if __name__ == "__main__":
    ed = AMFBot('hai050400@gmail.com', 'zaq1xsw2a@!')
    user_data_dir = r"C:\chrome_1"
    bot = ed.send_browser(user_data_dir)
    ed.open(bot)
