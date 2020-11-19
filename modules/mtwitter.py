from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests
import time
import html
import os


def twitterSearch(query, maximum=10):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-javascript")
    options.add_argument("--no-sandbox")

    options.add_experimental_option(
        "prefs", {'profile.managed_default_content_settings.javascript': 2})

    print('Options setted...')

    if os.environ.get("ENV") == "development":
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
    else:
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=options)
        print('Driver mounted...')

    url = 'https://mobile.twitter.com/search?q='+query

    finalComments = []

    try:
        driver.get(url)
        time.sleep(5)

        print('Driver opened...')
        # button = driver.find_element_by_tag_name("body")
        # a = button.get_attribute("innerHTML")
        # q = BeautifulSoup(a, 'html.parser')
        # print(q)
        # time.sleep(60)
        # button.click()

        print('Twitter acessed...')

        while True:
            javaScript = "window.scrollBy(0, document.body.scrollHeight);"
            driver.execute_script(javaScript)
            element = driver.find_element_by_tag_name("body")
            commentsDiv = element.get_attribute("innerHTML")

            soup = BeautifulSoup(commentsDiv, 'html.parser')

            print(soup)

            comments = soup.find_all('div', attrs={
                                     'class': 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})

            for i in comments:
                if i in finalComments:
                    continue
                else:
                    finalComments.append(html.escape(i.text))

            # moreButton = driver.find_element_by_class_name("w-button-more")
            # moreButton.click()
            time.sleep(2)

            print(len(finalComments))
            if len(finalComments) >= maximum:
                break

        print('Twitter crawling done!')
        driver.quit()
        return finalComments

    except Exception as x:
        print(x)
        print("Error on loading comments")
        driver.quit()
        return -1
