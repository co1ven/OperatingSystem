from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class OperatingSystem:
    URL = "https://vk.com"
    PROFILE = (r"/home/victor/.mozilla/firefox/yifmws2l.default")

    def run(self):
        opts = Options()
        opts.profile = self.PROFILE
        driver = webdriver.Firefox(options=opts)
        driver.get(self.URL)
        result = driver.find_elements_by_xpath("//div[@class='feed_row']")
        print(dir(result))
        for item in result:
            try:
                post_id = item.find_element_by_xpath("//div[@class=post]").get_attribute("id")
            except:
                post_id = "1333"
            try:
                text = item.find_element_by_xpath("//div[@class='wall_post_text']")
            except:
                text = ""
            # try:
            #     image_a = item.find_element_by_xpath("//a[@class='page_post_thumb_wrap image_cover  page_post_thumb_last_column page_post_thumb_last_row']")
            #     image_a.click()
            # except:
            #     image_a = ""
            print(text.text, post_id)
        # driver.close()