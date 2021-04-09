#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 22:20:11 2021

@author: lescardone
"""


from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
import time


url = 'https://www.bluenile.com/diamond-search'
driver = webdriver.Chrome()
# driver.implicitly_wait(60)
driver.get(url)

# clicking on round shape
# button = driver.find_element_by_xpath('//*[@id="Round-filter-button-med-lrg"]')
# button.click()

# adjust price
min_price = driver.find_element_by_name(name='price-min-input')
min_price.clear()
min_price.send_keys('500')

time.sleep(30)
for i in range (3):
    text = driver.find_element_by_name(name='price-max-input').get_attribute('value')
    try:
        max_price = driver.find_element_by_name(name='price-max-input')
        max_price.clear()
        max_price.send_keys('505')
        max_price.send_keys(Keys.ENTER)
    except StaleElementReferenceException:
        time.sleep(10)
        print('Stale Element:',i)
    except NoSuchElementException:
        time.sleep(10)
        print('No Such Element:',i)
    if text == '505':    
        print('Success:',i)
        break


# adjust carot min
time.sleep(2)
min_carot = driver.find_element_by_name(name='carat-min-input')
min_carot.clear()
min_carot.send_keys('.30')
min_carot.send_keys(Keys.ENTER)

# show more variables in table
time.sleep(2)
show_more = driver.find_element_by_xpath('//*[@id="react-app"]/div/div/section/div/div[2]/div[3]/button[2]')
show_more.click()

# add other variables to table
time.sleep(5)
polish_toggle = driver.find_element_by_id('polish-toggle-button')
polish_toggle.click()

time.sleep(2)
symmetry_toggle = driver.find_element_by_id('symmetry-toggle-button')
symmetry_toggle.click()

time.sleep(5)
fluo_toggle = driver.find_element_by_id('fluorescence-toggle-button')
fluo_toggle.click()

time.sleep(2)
depth_toggle = driver.find_element_by_id('depth %-toggle-button')
depth_toggle.click()

time.sleep(2)
table_toggle = driver.find_element_by_id('table %-toggle-button')
table_toggle.click()

# sort by delivery date
time.sleep(2)
for i in range (3):
    try:
        date_sort = driver.find_element_by_xpath('//*[@id="diamond-result"]/div[2]/div/div[1]/div/div[18]/button')
        date_sort.click()
        print('Success:',i)
    except ElementClickInterceptedException:
        time.sleep(10)
        print('Element Click Intercepted:',i)
    break

driver.quit()

# scroll all the way down
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(10)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(driver.page_source, 'lxml')
soup

table = soup.find('div', style='display:table')
table

column_header = soup.find('div', class_='row').find_all('span')
columns = [i.text for i in column_header][::2]
columns


df = pd.DataFrame(columns=columns)
df.drop(columns=['Compare','Cut'],axis=1,inplace=True)
df

rows = table.find_all('div',class_='grid-row row')
test = rows

for row_block in test:
    row_data = row_block.find_all('span',class_='single-cell')
    row = [j.text for j in row_data]
    length = len(df)
    if len(row) == 15:
        df.loc[length] = row
    else:
        pass
    
min_val = 500
max_val = 505

for i in range (3):
    driver.execute_script('window.scrollTo(0,200)') 
    min_val = max_val
    max_val += 5
    
    # adjust price
    min_price = driver.find_element_by_name(name='price-min-input')
    min_price.clear()
    min_price.send_keys(min_val)
    min_price.send_keys(Keys.ENTER)

    time.sleep(5)
    max_price = driver.find_element_by_name(name='price-max-input')
    max_price.clear()
    max_price.send_keys(max_val)
    max_price.send_keys(Keys.ENTER)
    
    for i in range (3):
        try:
            date_sort = driver.find_element_by_xpath('//*[@id="diamond-result"]/div[2]/div/div[1]/div/div[18]/button')
            date_sort.click()
            print('Success:',i)
        except ElementClickInterceptedException:
            time.sleep(10)
            print('Element Click Intercepted:',i)
        break
    
    time.sleep(5)
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(10)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    print('Interation:', i)

driver.quit()