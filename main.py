from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from auth_data import username, password
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

s = Service(ChromeDriverManager().install())


def browser_close(browser):
    browser.close()
    browser.quit()


def hashtag_search(username, password, hashtag):
    browser = webdriver.Chrome(options=options, service=s)

    try:
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

        time.sleep(5)

        try:
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)

            for i in range(1, 4):
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
            for url in post_urls[0:1]:
                if url not in like_posts:
                    browser.get(url)
                    print(url)
                    try:
                        like_button = browser.find_element(By.XPATH, '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
                        print('like!')
                        like_posts.append(url)
                    except Exception as ex:
                        print(ex)
                    print('go out')
                    time.sleep(5)




            browser_close(browser)

        except Exception as ex:
            print(ex)
            browser_close(browser)

        browser_close(browser)
    except Exception as ex:
        print(ex)
        browser_close(browser)


hashtag_search(username, password, 'surfing')
