from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests
import time
import os


def googleCommentsSearch(query, maximum=50):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    if os.environ.get("ENV") == "development":
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
    else:
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=options)

    url = 'https://www.google.com/search?q=' + query

    finalComments = []

    try:
        driver.get(url)
        time.sleep(2)

        viewComments = driver.find_element_by_class_name('qB0t4')
        viewComments.click()

        time.sleep(2)

        dialog = driver.find_element_by_class_name('review-dialog-list')

        while True:
            driver.execute_script("arguments[0].scrollTo(0, 10000)", dialog)

            time.sleep(2)
            modalPage = dialog.get_attribute("innerHTML")

            soup = BeautifulSoup(modalPage, 'html.parser')
            comments = soup.find_all('span', attrs={'jscontroller': 'P7L8k'})

            print(len(comments))

            for i in comments:
                if i in finalComments:
                    continue
                else:
                    finalComments.append(i.text)

            if len(finalComments) >= maximum:
                break

        print('Google crawling done!')
        return finalComments

    except Exception as x:
        print(x)
        print("Error on loading comments")
        driver.quit()
        return -1

    driver.quit()
