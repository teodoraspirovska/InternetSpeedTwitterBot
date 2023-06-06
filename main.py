import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

PROMISED_DOWN = 70
PROMISED_UP = 50
chrome_driver_path = os.environ.get("DRIVER_PATH")
username = os.environ.get("TWITTER_USERNAME")
password = os.environ.get("TWITTER_PASSWORD")


class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(3)
        go_button = self.driver.find_element_by_class_name("start-text")
        go_button.click()

        time.sleep(40)
        self.up = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div['
                                                    '3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        self.down = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div['
                                                      '3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
        print(self.up, self.down)

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/i/flow/login")
        wait = WebDriverWait(self.driver, 20)

        username_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                 '/html/body/div/div/div/div['
                                                                 '1]/div/div/div/div/div/div/div[2]/div['
                                                                 '2]/div/div/div[2]/div[2]/div/div/div/div['
                                                                 '5]/label/div/div[2]/div/input')))

        username_button.send_keys(username)

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]")))
        next_button.click()

        password_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div['
                                                                                 '1]/div/div/div/div/div/div/div['
                                                                                 '2]/div[2]/div/div/div[2]/div['
                                                                                 '2]/div[1]/div/div/div['
                                                                                 '3]/div/label/div/div[2]/div['
                                                                                 '1]/input')))
        password_button.send_keys(password)

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']")))
        login_button.click()
        time.sleep(10)

        send_msg = self.driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Tweet text"]')
        send_msg.clear()
        send_msg.send_keys(f"Dear Internet Service Provider, I find myself wondering why my internet speed of {self.up} Mbps upload and {self.down} Mbps download falls short, especially considering the subscription I have diligently paid for, promising a superior performance of {PROMISED_UP} Mbps upload and {PROMISED_DOWN} Mbps download.")
        tweet = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div['
                                                  '3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div['
                                                  '3]/div/span/span')
        tweet.click()


bot = InternetSpeedTwitterBot(chrome_driver_path)
bot.get_internet_speed()
bot.tweet_at_provider()
