from time import sleep
import re
import json
# import queue
from threading import Thread
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


class OperatingSystem:

    def __init__(self):
        self.URL = "https://vk.com"
        opts = Options()
        opts.profile = (r"/home/victor/.mozilla/firefox/yifmws2l.default")
        # open browser
        self.driver = webdriver.Firefox(options=opts)

    def check_modal_window(self):
        """Проверка на выпадающее модальное окно"""
        if self.driver.find_element_by_id("box_layer").is_displayed():
            self.driver.find_element_by_class_name("box_x_button").click()

    def get_info(self):
        """Парсинг новостей"""
        # checking for modal window
        self.check_modal_window()
        # parse data
        for _ in range(5):
            news = self.driver.find_element_by_id("feed_rows")
            items = news.find_elements_by_class_name("feed_row")
            for item in items:
                # Скроллинг к текущему посту
                self.driver.execute_script("arguments[0].scrollIntoView();", item)
                # Проверка на содержимое поста (реклама, новость или рекомендованные друзья)
                try:
                    post = item.find_element_by_class_name("post")
                    post_id = post.get_attribute("id")
                    post_content = post.find_element_by_class_name("post_content")
                    # Проверка на наличие текста в новости
                    try:
                        text = post_content.find_element_by_class_name("wall_post_text").text
                        links = re.findall(r'((?:https?://)?(?:[\w.]+)\.(?:[a-z]{2,6}\.?)(?:/[\w.]*)*/?)', text)
                    except NoSuchElementException:
                        text = ""
                        links = ""
                    # Проверка на наличие картинки в новости
                    try:
                        img_links = []
                        post_image_container = post.find_element_by_class_name("page_post_sized_thumbs")
                        image_a = post_image_container.find_elements_by_class_name("image_cover")
                        for a in image_a:
                            sleep(5)
                            if 'showPhoto' in a.get_attribute("onclick"):
                                a.click()
                                img_link = self.driver.find_element_by_id("pv_photo").find_element_by_tag_name(
                                    "img").get_attribute("src")
                                img_links.append(img_link)
                                self.driver.find_element_by_class_name("pv_close_btn").click()
                    except NoSuchElementException:
                        img_links = []
                    # with threads writing data to file
                    self.write_json("file1.json", post_id=post_id, post_text=text)
                    self.write_json("file2.json", post_id=post_id, post_links=links)
                    self.write_json("file3.json", post_id=post_id, post_image_links=img_links)
                except NoSuchElementException:
                    continue
            self.update_page(5)

    def repeat_check(self, old_data, new_data):
        flag = False
        for old_item in old_data:
            if new_data["post_id"] == old_item["post_id"]:
                flag = True
        if not flag:
            old_data.append(new_data)
        return old_data

    def read_json(self, filename):
        # reading data from json file
        with open(filename, 'r') as file:
            return json.load(file)

    def write_json(self, filename, **data):
        # writing data to json file
        try:
            old_data = self.read_json(filename)
            old_data = self.repeat_check(old_data, data)
            # old_data.append(data)
            with open(filename, 'r+') as file:
                file.write(json.dumps(old_data, sort_keys=True, ensure_ascii=False, indent=3, separators=(',', ': ')))
        except FileNotFoundError:
            with open(filename, 'w') as file:
                new_data = list()
                new_data.append(data)
                file.write(json.dumps(new_data, sort_keys=True, ensure_ascii=False, indent=3, separators=(',', ': ')))

    def update_page(self, interval=0):
        # updates page every `interval` seconds
        sleep(interval)
        self.driver.get(self.URL)

    def run(self):
        # run function
        self.driver.get(self.URL)
        self.get_info()
        self.driver.close()
