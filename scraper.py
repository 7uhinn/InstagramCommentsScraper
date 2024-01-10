from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from langdetect import detect
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
from selenium.webdriver.chrome.service import Service


def init_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.wait = WebDriverWait(driver, 5)
    return driver


def get_comments(plain_html):
    lan = input("Only English Comments (y/n): ")
    soup = bs(plain_html, 'html.parser')
    comments = soup.find_all('div', {'class':'_ap3a _aaco _aacw _aacx _aad7 _aade'})
    encount = 0
    all_comments = []
    en_comments = []
    print(comments)
    for i in range(len(comments)):
        if i == 0:
            continue
        res = comments[i]
        txt = res.find("span").text
        all_comments.append(txt)
        try:
            if detect(txt)=='en':
                en_comments.append(txt)
                encount = encount + 1
        except:
            pass
    print("===================================================")
    if lan == 'y':
        print(*en_comments, sep='\n')
    else:
        print(*all_comments, sep='\n')
    print("===================================================")
    print("Number of English Comments: ", len(en_comments))
    print("Number of all comments:", len(comments))
    time.sleep(1)


def click_more_comments(driver):
    post_address = input("Enter the Instagram Post Address and Press Enter: ")
    username = input("Enter the Instagram Username and Press Enter: ")
    password = input("Enter the Instagram Password and Press Enter: ")
    print("Please wait...")
    driver.get(post_address)
    driver.implicitly_wait(5)
    try:
        button = driver.find_element(By.XPATH, "//a[contains(text(), 'Log in')]")
        button.click()
        login_name = driver.find_element(By.XPATH, "//input[@class='_aa4b _add6 _ac4d _ap35']")
        login_name.send_keys(username)
        pass_name = driver.find_element(By.XPATH, "//input[@type='password']")
        pass_name.send_keys(password)
        button2 = driver.find_element(By.XPATH, "//div[contains(text(), 'Log in')]")
        button2.click()
        button3 = driver.find_element(By.XPATH, "//div[contains(text(), 'Not now')]")
        button3.click()
        driver.implicitly_wait(10)
    except:
        pass
    
    
    return driver.page_source


if __name__ == "__main__":
    driver = init_driver()
    expanded_page_source = click_more_comments(driver)
    get_comments(expanded_page_source)
    driver.quit()