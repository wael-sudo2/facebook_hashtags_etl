import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import re



SCROLL_WAIT_TIME = 2
PAGE_LOAD_WAIT_TIME = 3

def webdriver_set_up():
    """chrome driver setup"""
    global driver
    options = Options()

    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    options.add_argument("--start-maximized")
    # options.add_argument("headless")

    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(e, "Failed setting up webdriver")
        exit(1)


def scroll():
    """scroll page and fetch data"""
    step_size = 3000
    nb = 0
    equal = 0
    # List of each post for hashtag search
    post_list = []

    while True:
        # get page old height
        page_old_height = driver.execute_script(
            "return document.body.scrollHeight")
        time.sleep(SCROLL_WAIT_TIME)

        # Scroll
        driver.execute_script(
            "window.scrollTo(0," + str(step_size) + ")")

        time.sleep(SCROLL_WAIT_TIME)
        page_new_height = driver.execute_script(
            "return document.body.scrollHeight")
        if page_new_height == page_old_height:
            print('please wait..... loading page data ......')
            # wait 1 minute to load the page info
            time.sleep(PAGE_LOAD_WAIT_TIME)
            equal += 1
        else:
            equal = 0

        # if the incrementation happens 10 times in arrow then we reached the bottom of the page
        if equal == 10:
            break

        nb += 1
        step_size += 2500
        print('scroll number:', nb)
        if nb == 100 :
            break


def fetch_video_link(default_link:str):
    link = re.compile(r"https:\/\/www\.facebook\.com\/[\w.-]+\/videos\/\d+")
    match = link.search(default_link)
    if match:
        return match.group()
    else:
        return None


def fetch_photo_link(default_link:str):
    link = re.compile(r"https:\/\/www\.facebook\.com\/photo\/\?fbid=\d+")
    match = link.search(default_link)
    if match:
        return match.group()
    else:
        return None


def fetch_all_links() -> list:
    posts_links = list()
    all_a = driver.find_elements(By.TAG_NAME, value="a")
    for a in all_a:
        if fetch_photo_link(a.get_attribute('href')):
            posts_links.append(fetch_photo_link(a.get_attribute('href')))
        elif fetch_video_link(a.get_attribute('href')):
            posts_links.append(fetch_video_link(a.get_attribute('href')))
    return posts_links


def fetch_video_post_web_element():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.ID,
                 "mobile_injected_video_feed_pagelet")))
    except TimeoutException:
        print("timed out")

    divs = driver.find_elements(By.ID, value='mobile_injected_video_feed_pagelet')
    post_webelement = divs[0]
    return post_webelement


def fetch_post_link(key:str,post_webelement:WebElement):
    if key == 'video':
        header = post_webelement.find_element(By.TAG_NAME,value='header')
        link = header.find_element(By.TAG_NAME,value='a').get_attribute('href')
        print(link)


def fetch_post_content(key:str, post_webelement:WebElement):
    text = ''
    if key == 'video':
        # iterate:
        # header following sibiling div ->
            # div->
                #<div> nested div 1 </div> ->
                    # <nested div 1> nested span </nested div 1> ->
                        # <nested span> all p tags <nested span>;

        header = post_webelement.find_element(By.TAG_NAME,value='header')
        parent_div = header.find_element(By.XPATH, value='//header/following-sibling::div')
        div_content_element = parent_div.find_element(By.XPATH, value="(//div)[1]/div")
        span_content_element = div_content_element.find_elements(By.XPATH,value="(//span//p)")
        for p in span_content_element:
            text+= p.text
        print(text)
        return text

def scrapper():
    driver = webdriver_set_up()
    driver.get("https://www.facebook.com/hashtag/childabuse")
    time.sleep(3)
    scroll()
    posts = fetch_all_links()
    for post in posts:
        link = post.replace('www','m')
        driver.get(link)
        if 'video' in link:
            element = fetch_video_post_web_element()
            if element:
               link =  fetch_post_link(key='video', post_webelement=element)
               content = fetch_post_content(key='video', post_webelement=element)
               yield content



