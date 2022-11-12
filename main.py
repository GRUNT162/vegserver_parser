# -*- coding: cp1251 -*-
import os
os.system('pip install selenium')
os.system('pip install pandas')
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas
import itertools
import time


def login(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_class_name('ant-btn-primary').click()


def get_email(driver):
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="company-page"]/div/div/dl/dd/ul/li/a')))
        email = driver.find_elements_by_xpath('//*[@id="company-page"]/div/div/dl/dd/ul/li/a')
        for n, e in enumerate(email):
            email[n] = e.get_attribute('innerHTML')
        return ', '.join(email)
    except:
        return 'NO EMAIL'


def get_categories(driver):
    categories = []

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/main/div/div[1]/div[2]/section/ul/li/a')))
    categories_raw = driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/main/div/div[1]/div[2]/section/ul/li/a')
    for cat in categories_raw:
        categories.append(cat.get_attribute('href'))
    return categories

def get_categories2(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/main/div/div[1]/div[2]/div/div['
                                                  '2]/ul/li/a')))
    categories_raw = driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/main/div/div[1]/div[2]/div/div['
                                                   '2]/ul/li/a')
    categories = []
    for cat in categories_raw:
        categories.append(cat.get_attribute('href'))
    return categories


def get_links(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/div/div[2]/main/div/div/div/div/div/div/table/tbody/tr/td/div/a')))
    links = driver.find_elements_by_xpath('//*[@id="content"]/div/div['
                                          '2]/main/div/div/div/div/div/div/table/tbody/tr/td/div/a')
    arr = []
    for link in links:
        arr.append(link.get_attribute('href'))
    return arr


def get_pages(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/div/div[2]/main/div/div/div/ul[1]/li[9]')))
    pages1 = int(driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/main/div/div/div/ul[1]/li[9]').get_attribute('title'))
    try:
        pages2 = int(
            driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/main/div/div/div/ul[1]/li[11]').get_attribute(
                'title'))
        return pages2
    except:
        try:
            pages3 = int(
                driver.find_element_by_xpath(
                    '//*[@id="content"]/div/div[2]/main/div/div/div/ul[1]/li[10]').get_attribute(
                    'title'))
            return pages3
        except:
            return pages1


username = 'dfgsgthth'
password = '1'
driver = webdriver.Chrome()
driver.get('https://ru.foodmara.com/user/login')
login(driver)  # login

main_queue = ('https://ru.foodmara.com/companies', 'https://ru.foodmara.com/companies')
for pos in main_queue:
    main_arr = []
    driver.get(pos)
    data = []
    if pos != 'https://ru.foodmara.com/retail':
        categories = get_categories(driver)  # categories
    else:
        categories = get_categories2(driver)
        length = len(categories)
    df = pandas.DataFrame(columns=categories)
    print(categories)

    for category in categories:
        print(f'start of category = {category} | data = {data[-6:-1]}')
        data1 = []
        driver.get(category)
        pages = get_pages(driver)  # pages
        for page in range(1, pages + 1):
            print(f'  start of page = {page} of pages = {pages} | data = {data[-6:-1]} data1 = {data1[-6:-1]}')
            current_page = category + f'&page={page}'
            driver.get(current_page)
            links = get_links(driver)  # links
            for link in links:
                print(f'    start of link = {link} | data = {data[-6:-1]} data1 = {data1[-6:-1]}')
                driver.get(link)
                email = get_email(driver)  # email
                data1.append(email)
                time.sleep(1)
                print(f'    end of link = {link} | data = {data[-6:-1]} data1 = {data1[-6:-1]}, email = {email}')
            print(f'  end of page = {page} of pages = {pages} | data = {data[-6:-1]} data1 = {data1[-6:-1]}')
        data.append(data1)
        print(f'end of category = {category} | data = {data[-6:-1]}')
    df = pandas.DataFrame(columns=categories)
    for i in itertools.zip_longest(*data):
        new_df = pandas.DataFrame(columns=categories, data=[i])
        df = df.append(new_df, ignore_index=True)

    print(df)
    df.to_csv(pos.split('/')[-1])

