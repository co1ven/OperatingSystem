from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class OperatingSystem:
    URL = "https://vk.com"
    PROFILE = (r"/home/victor/.mozilla/firefox/yifmws2l.default")

    def get_info(self):
        pass

    def run(self):
        opts = Options()
        opts.profile = self.PROFILE
        driver = webdriver.Firefox(options=opts)
        driver.get(self.URL)