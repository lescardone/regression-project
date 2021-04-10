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
driver.get(url)

# clicking on round shape
# button = driver.find_element_by_xpath('//*[@id="Round-filter-button-med-lrg"]')
# button.click()

# adjust price
min_price = driver.find_element_by_name(name='price-min-input')
min_price.clear()
min_price.send_keys('500')

for i in range (8):
    try:
        #text = driver.find_element_by_name(name='price-max-input').get_attribute('value')
        max_price = driver.find_element_by_name(name='price-max-input')
        max_price.clear()
        max_price.send_keys('600')
        max_price.send_keys(Keys.ENTER)
        print('OUTTER LOOP...Max price input success:',i)
        break
    except StaleElementReferenceException:
        time.sleep(10)
        print('OUTTER LOOP...MAX Stale Element:',i)
    except NoSuchElementException:
        time.sleep(10)
        print('OUTTER LOOP...MAX No Such Element:',i)


# adjust carot min
time.sleep(2)
min_carot = driver.find_element_by_name(name='carat-min-input')
min_carot.clear()
min_carot.send_keys('.25')
min_carot.send_keys(Keys.ENTER)

# show more variables in table
time.sleep(2)
show_more = driver.find_element_by_xpath('//*[@id="react-app"]/div/div/section/div/div[2]/div[3]/button[2]')
show_more.click()

#croll down a little
driver.execute_script('window.scrollTo(0,400)') 

# add other variables to table
time.sleep(5)
polish_toggle = driver.find_element_by_id('polish-toggle-button')
polish_toggle.click()

time.sleep(2)
symmetry_toggle = driver.find_element_by_id('symmetry-toggle-button')
symmetry_toggle.click()

time.sleep(5)
for i in range (3):
    try:
        fluo_toggle = driver.find_element_by_id('fluorescence-toggle-button')
        fluo_toggle.click()
        print('Toggle success:',i)
        break
    except ElementClickInterceptedException:
        time.sleep(10)
        print('TOGGLE Element Click Intercepted:',i)
    break

time.sleep(2)
depth_toggle = driver.find_element_by_id('depth %-toggle-button')
depth_toggle.click()

time.sleep(2)
table_toggle = driver.find_element_by_id('table %-toggle-button')
table_toggle.click()

# sort by delivery date
time.sleep(2)
for i in range (5):
    try:
        date_sort = driver.find_element_by_xpath('//*[@id="diamond-result"]/div[2]/div/div[1]/div/div[18]/button')
        date_sort.click()
        print('OUTTER LOOP Sort success:',i)
        break
    except ElementClickInterceptedException:
        time.sleep(10)
        print('OUTTER LOOP Element Click Intercepted:',i-1)
    break


# scroll all the way down
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(10)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height



# make the soup
soup = BeautifulSoup(driver.page_source, 'lxml')

# create columns
column_header = soup.find('div', class_='row').find_all('span')
columns = [i.text for i in column_header][::2]
#columns

# create dataframe ROUND
df = pd.DataFrame(columns=columns)
df.drop(columns=['Compare','Cut'],axis=1,inplace=True)
df['Cut']=None

# create dataframe PRINCESS (and other)
df2 = pd.DataFrame(columns=columns)
df2.drop(columns=['Compare','Cut'],axis=1,inplace=True)
df2['Cut']=None


#ROUND DF
# isolate table, isolate rows
# first pass
table = soup.find('div', style='display:table')
rows = table.find_all('div',class_='grid-row row')


for row_block in rows:
    row_data = row_block.find_all('span',class_='single-cell')
    row = [j.text for j in row_data]

    cut_data = row_block.find('span',class_='label')
    cut = cut_data.text  
    row.append(cut)
    #print(cut)
    
    length = len(df)
    if len(row) == 16:
        df.loc[length] = row
    else:
        pass
        
# automate the process
min_val = 500
max_val = 600

for i in range (50):
    #scroll to top
    driver.execute_script('window.scrollTo(0,200)') 
    
    #max is now min, max increase by 10
    min_val = max_val
    max_val += 100
    
    # adjust price
    min_price = driver.find_element_by_name(name='price-min-input')
    min_price.clear()
    min_price.send_keys(min_val)
    min_price.send_keys(Keys.ENTER)

    time.sleep(10)
    for ii in range (5):
        try:
            #text = driver.find_element_by_name(name='price-max-input').get_attribute('value')
            max_price = driver.find_element_by_name(name='price-max-input')
            max_price.clear()
            max_price.send_keys(max_val)
            max_price.send_keys(Keys.ENTER)
            print('Max price input success:',i,':',ii)
            break
        except StaleElementReferenceException:
            time.sleep(10)
            print('MAX Stale Element:',i,':',ii)
        except NoSuchElementException:
            time.sleep(10)
            print('MAX No Such Element:',i,':',ii)
  
    #sort by delivery date to randomize
    for iii in range (5):
        try:
            driver.execute_script('window.scrollTo(0,500)') 
            date_sort = driver.find_element_by_xpath('//*[@id="diamond-result"]/div[2]/div/div[1]/div/div[18]/button')
            date_sort.click()
            print('Date Sort Success:',i,':',iii)
            break
        except ElementClickInterceptedException:
            time.sleep(10)
            print('DATE Element Click Intercepted:',i,':',iii)


    #scroll to bottom to load all rows
    time.sleep(5)
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(10)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    print('Scroll to bottom:', i)
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('div', style='display:table')
    rows = table.find_all('div',class_='grid-row row')


    for row_block in rows:
        row_data = row_block.find_all('span',class_='single-cell')
        row = [j.text for j in row_data]
    
        cut_data = row_block.find('span',class_='label')
        cut = cut_data.text  
        row.append(cut)
        #print(cut)
        
        length = len(df)
        if len(row) == 16:
            df.loc[length] = row
        else:
            pass
    
    print('INNER LOOP COMPLETE:',i)
    
df.to_csv('bluenile_round_13k.csv')




# CUSHION PRINCESS RADIANCE DF2
min_val = 400
max_val = 500

for i in range (150):
    #scroll to top
    driver.execute_script('window.scrollTo(0,200)') 
    
    #max is now min, max increase by 100
    min_val = max_val
    max_val += 100
    
    # adjust price
    min_price = driver.find_element_by_name(name='price-min-input')
    min_price.clear()
    min_price.send_keys(min_val)
    min_price.send_keys(Keys.ENTER)

    time.sleep(10)
    for ii in range (5):
        try:
            #text = driver.find_element_by_name(name='price-max-input').get_attribute('value')
            max_price = driver.find_element_by_name(name='price-max-input')
            max_price.clear()
            max_price.send_keys(max_val)
            max_price.send_keys(Keys.ENTER)
            print('Max price input success:',i,':',ii)
            break
        except StaleElementReferenceException:
            time.sleep(10)
            print('MAX Stale Element:',i,':',ii)
        except NoSuchElementException:
            time.sleep(10)
            print('MAX No Such Element:',i,':',ii)
  
    #sort by delivery date to randomize
    for iii in range (5):
        try:
            driver.execute_script('window.scrollTo(0,500)') 
            date_sort = driver.find_element_by_xpath('//*[@id="diamond-result"]/div[2]/div/div[1]/div/div[18]/button')
            date_sort.click()
            print('Date Sort Success:',i,':',iii)
            break
        except ElementClickInterceptedException:
            time.sleep(10)
            print('DATE Element Click Intercepted:',i,':',iii)


    #scroll to bottom to load all rows
    time.sleep(5)
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(10)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    print('Scroll to bottom:', i)
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('div', style='display:table')
    rows = table.find_all('div',class_='grid-row row')


    for row_block in rows:
        row_data = row_block.find_all('span',class_='single-cell')
        row = [j.text for j in row_data]
    
        cut_data = row_block.find('span',class_='label')
        cut = cut_data.text  
        row.append(cut)
        #print(cut)
        
        length = len(df2)
        if len(row) == 16:
            df2.loc[length] = row
        else:
            pass
    
    print('INNER LOOP COMPLETE:',i)
  
df2.to_csv('bluenile_princess_13k.csv')
