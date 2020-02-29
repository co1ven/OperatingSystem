from time import sleep
import re
import json
from threading import Thread
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


class OperatingSystem:
    URL = "https://vk.com"
    opts = Options()
    opts.profile = (r"/home/victor/.mozilla/firefox/yifmws2l.default")
    is_thread = False

    def save_data_to_json(self, data, filename="file.json", post_id=True, post_text=True, post_links=True, post_img_links=True):
        """Сохранение данных в файл"""
        final_data = []
        for item in data:
            q = {}
            q.update(id=item["post_id"]) if post_id else q.update()
            q.update(text=item["post_text"]) if post_text else q.update()
            q.update(links=item["post_links"]) if post_links else q.update()
            q.update(img_links=item["post_image_links"]) if post_img_links else q.update()
            final_data.append(q)
        with open(filename, 'w') as file:
            file.write(json.dumps(final_data, sort_keys=True, ensure_ascii=False, indent=3, separators=(',', ': ')))

    def check_modal_window(self, driver):
        """Проверка на выпадающее модальное окно"""
        if driver.find_element_by_id("box_layer").is_displayed():
            driver.find_element_by_class_name("box_x_button").click()

    def get_info(self, driver):
        """Парсинг новостей"""
        self.check_modal_window(driver)
        news = driver.find_element_by_id("feed_rows")
        # next_news = news.find_element_by_id("feed_rows_next") # Следующие новости
        # unshown_news = news.find_element_by_class_name("feed_row_unshown") # Новые новости
        items = news.find_elements_by_class_name("feed_row")
        data = []
        for item in items:
            # Проверка на содержимое поста (реклама, новость или рекомендованные друзья)
            try:
                post = item.find_element_by_class_name("post")
                post_id = post.get_attribute("id")
                post_content = post.find_element_by_class_name("post_content")
                # Проверка на наличие текста в новости
                try:
                    text = post_content.find_element_by_class_name("wall_post_text").text
                    links = re.findall(r'((https?)?://[^\s]+)', text)
                except NoSuchElementException:
                    text = ""
                    links = ""
                # Проверка на наличие картинки в новости
                img_links = []
                try:
                    post_image_container = post.find_element_by_class_name("page_post_sized_thumbs")
                    image_a = post_image_container.find_elements_by_class_name("image_cover")
                    for a in image_a:
                        sleep(5)
                        if 'showPhoto' in a.get_attribute("onclick"):
                            a.click()
                            img_link = driver.find_element_by_id("pv_photo").find_element_by_tag_name("img").get_attribute("src")
                            img_links.append(img_link)
                            driver.find_element_by_class_name("pv_close_btn").click()
                except NoSuchElementException:
                    continue
            except NoSuchElementException:
                continue
            data.append({"post_id": post_id, "post_text": text, "post_links": links, "post_image_links": img_links})
        return data

    def run(self):
        """Запуск программы"""
        driver = webdriver.Firefox(options=self.opts)
        driver.get(self.URL)
        result = self.get_info(driver)
        time_start = datetime.now()
        if self.is_thread:
            thread1 = Thread(target=self.save_data_to_json, kwargs={
                "data": result,
                "filename": "file1.json",
                "post_links": False,
                "post_img_links": False
            })
            thread2 = Thread(target=self.save_data_to_json, kwargs={
                "data": result,
                "filename": "file2.json",
                "post_text": False,
                "post_links": False
            })
            thread3 = Thread(target=self.save_data_to_json, kwargs={
                "data": result,
                "filename": "file3.json",
                "post_text": False,
                "post_img_links": False
            })
            thread1.start()
            thread2.start()
            thread3.start()
            thread1.join()
            thread2.join()
            thread3.join()
        else:
            self.save_data_to_json(result, "file1.json", post_links=False, post_img_links=False)
            self.save_data_to_json(result, "file2.json", post_links=False, post_text=False)
            self.save_data_to_json(result, "file3.json", post_text=False, post_img_links=False)
        print(datetime.now() - time_start)
        driver.close()
