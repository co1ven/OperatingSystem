from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.firefox.options import Options
import re
import json


class OperatingSystem:
    URL = "https://vk.com"
    opts = Options()
    opts.profile = (r"/home/victor/.mozilla/firefox/yifmws2l.default")

    def save_data_to_file(self, data, filename="file.json"):
        """Сохранение данных в файл"""
        with open(filename, 'w') as file:
            file.write(data)

    def check_modal_window(self, driver):
        """Проверка на выпадающее модальное окно"""
        if driver.find_element_by_id("box_layer").is_displayed():
            driver.find_element_by_class("box_x_button").click()

    def find_info(self, driver):
        """Парсинг id, text и image_url новостей"""
        self.check_modal_window(driver)
        news = driver.find_elements_by_class_name("feed_row")
        image_links = []
        data = []
        for item in news:
            try:
                content = item.find_element_by_class_name("wall_post_text").text
                urls = re.match(r"(?P<url>https?://[^\s]+)", content)
            except:
                content = "Text not exists."
                urls = "Links are not exist."
            id = item.find_element_by_tag_name("div").get_attribute("id")[5:]
            try:
                if 'showPhoto' in item.find_element_by_class_name("page_post_thumb_wrap").get_attribute("onclick"):
                    image_links.append(item.find_element_by_class_name("page_post_thumb_wrap"))
                else:
                    image_links.append(None)
            except:
                pass

            data.append({"content": content, "id": id, "image_url": None, "urls": urls})
        for i in range(len(image_links)):
            if image_links[i] == None:
                continue
            else:
                try:
                    image_links[i].click()
                    image_url = driver.find_element_by_id("pv_photo").find_element_by_tag_name("img").get_attribute(
                        "src")
                    driver.find_element_by_class_name("pv_close_btn").click()
                    data[i]["image_url"] = image_url
                except (ElementClickInterceptedException, NoSuchElementException):
                    pass
        return json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))



    def run(self):
        """Запуск программы"""
        driver = webdriver.Firefox(options=self.opts)
        driver.get(self.URL)
        result = self.find_info(driver)
        self.save_data_to_file(result)
