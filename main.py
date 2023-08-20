from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


import time
import json
import requests

from twocaptcha import TwoCaptcha

from config import *


class Bot:
    def __init__(self) -> None:
        if self.CreateBotDriver() == False:
            return
        with open('elements.json') as fp:
            self.elements = json.loads(fp.read())
        self.solver = TwoCaptcha(TWO_CAPTCHA_KEY)

    def CreateBotDriver(self):
        try:
            response_octo = requests.request("GET", OCTO_SEARCH_URL, headers=OCTO_HEADER)
            data_uuid = response_octo.json()
            uuid = data_uuid.get('data')[0]['uuid']
            debug_port = requests.post(
                f'{LOCAL_API}/start', json={'uuid': uuid, 'headless': False, 'debug_port': True}
            ).json()['debug_port']
            chrome_options = Options()
            chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{debug_port}')
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            self.driver.maximize_window()
        except:
            print("Error: >> Create WebDriver happen Error")
            return False
        return True
    
    def SignIn(self, email, password):
        WebDriverWait(self.driver, 90).until(EC.visibility_of_element_located((By.XPATH, self.elements['login_email']))).send_keys(email)
        WebDriverWait(self.driver, 90).until(EC.visibility_of_element_located((By.XPATH, self.elements['login_password']))).send_keys(password)
        data_site_key = WebDriverWait(self.driver, 90).until(EC.visibility_of_element_located((By.XPATH, self.elements['data_site_key_iframe']))).get_attributes("src")
        print(data_site_key)
        result = self.solver.recaptcha(sitekey=data_site_key, url=TARGET_URL)
        print(result)
if __name__ == "__main__":
    bot = Bot()
    bot.SignIn(LOGIN_EMAIL, LOGIN_PASSWORD)