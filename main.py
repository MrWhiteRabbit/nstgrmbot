from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from auth_data import auth_data
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

options = Options()
ua = UserAgent()
userAgent = ua.random

options.add_argument(f'user-agent={userAgent}')

s = Service(ChromeDriverManager().install())


class NstgrmBot():

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(options=options, service=s)

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(self.username)

        time.sleep(2)

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(self.password)

        password_input.send_keys(Keys.ENTER)

        time.sleep(5)

    def like_photo_by_hashtag(self, hashtag):
        # Лайк на фотографии по хэштегу
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 3):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements(By.TAG_NAME, 'a')
        post_urls = []
        for item in hrefs:
            href = item.get_attribute('href')

            try:
                if '/p/' in href:
                    post_urls.append(href)
            except Exception as ex:
                print(ex)
                pass

        print(len(post_urls))
        like_posts = []
        for url in post_urls[0:5]:
            if url not in like_posts:
                browser.get(url)
                print(url)
                try:
                    self.make_like()
                    print('like!')
                    like_posts.append(url)
                except Exception as ex:
                    print(ex)
                print('go out')
                time.sleep(5)

    def xpath_exist(self, url):
        # Проверка существования URL
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False

        return exist

    def put_exactly_like(self, userpost):
        # Лайк по прямой ссылке
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = '/html/body/div[1]/section/main/div/div/h2'
        if self.xpath_exist(wrong_userpage):
            print('Такого поста не существует')
            self.close_browser()
        else:
            time.sleep(random.randrange(1, 2))
            self.make_like()
            time.sleep(random.randrange(2, 4))
            print(f'Поставлен лайк на пост {userpost}')
            self.close_browser()


    def make_like(self):

        browser = self.browser
        like_button = '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
        browser.find_element(By.XPATH, like_button).click()

    def put_many_likes(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = '/html/body/div[1]/section/main/div/div/h2'
        if self.xpath_exist(wrong_userpage):
            print('Такого пользователя не существует')
            self.close_browser()
        else:
            time.sleep(random.randrange(1, 2))

            posts_count = int(browser.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            loops_count = int(posts_count / 12)

            post_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements(By.TAG_NAME, 'a')

                for item in hrefs:
                    href = item.get_attribute('href')

                    try:
                        if '/p/' in href:
                            post_urls.append(href)
                    except Exception as ex:
                        print(ex)
                        pass

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f'Итерация #{i}')

            file_name = userpage.split('/')[-2]

            post_urls_set = set(post_urls)
            post_urls = list(post_urls_set)

            with open(f'{file_name}', 'a') as file:
                for post_url in post_urls:
                    file.write(post_url + '\n')

            liked_post = []
            with open(f'{file_name}', 'r') as file:
                urls_list = file.readlines()

                for url in urls_list:
                    try:
                        if url not in liked_post:
                            browser.get(url)
                            time.sleep(2)

                            self.make_like()

                            liked_post.append(url)
                            time.sleep(random.randrange(30, 50))
                            time.sleep(random.randrange(2, 4))

                    except Exception as ex:
                        print(ex)
                        self.close_browser()

            self.close_browser()


def main():
    #auth_data = {'username': 'password', ...}
    for key in auth_data.keys():
        bot = NstgrmBot(username=key, password=auth_data.get(key))
        bot.login()
        bot.put_exactly_like('https://www.instagram.com/p/CVhof9NA0Nb/')
        # bot.put_many_likes(url)


if __name__ == '__main__':
    main()
