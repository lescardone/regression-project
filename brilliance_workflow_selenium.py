#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 08:35:08 2021

@author: lescardone
"""

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.alert import Alert
import time

url = 'https://www.brilliance.com/diamond-search'
driver = webdriver.Chrome()
driver.get(url)


# clicking on round shape
button = driver.find_element_by_xpath('//*[@id="ds-shapes"]/ul/li[1]/div')
button.click()

# adjust price
min_price = driver.find_element_by_id('priceMin')
min_price.clear()
min_price.send_keys('500')

for i in range (8):
    try:
        #text = driver.find_element_by_name(name='price-max-input').get_attribute('value')
        max_price = driver.find_element_by_id('priceMax')
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
min_carot = driver.find_element_by_id('caratMin')
min_carot.click()
min_carot.send_keys('.23')
min_carot.send_keys(Keys.ENTER)

soup = BeautifulSoup(driver.page_source, 'lxml')
soup

# SET UP
first_row = soup.find('div',id='brl-diamond-search-table').find('div',class_='ds__item search-repeat')
first_row

link = first_row.find('a')['href']
tab = 'https://www.brilliance.com/' + link
        
# open new tab
driver.execute_script(f'''window.open('{tab}','_blank');''')
driver.switch_to.window(driver.window_handles[1])
driver.refresh()
    
# pull html
diamond_soup = BeautifulSoup(driver.page_source,'lxml')
        
# isolate table
table = diamond_soup.find('div',class_='tab-content col-sm-12')
        
# get stock number column
stock_column = table.find('div',class_='product__tab-price product__title-item pull-left').find('strong').text
stock_column = stock_column.replace(':','')
stock_column
    
# stock number
stock_number = table.find('div',class_='product__tab-price product__title-item pull-left').find('small').text
stock_number  
    
# price
price = table.find('div',class_='product__tab-price product__title-item product__title-price pull-right no-margin-top').find('span').text
price 
        
cells = table.find_all('div',class_='product-specs__listing-item')
cell_list = [cell.text for cell in cells]
    
columns = [string.strip().split(':')[0] for string in cell_list]
columns.append(stock_column)
columns.append('Price')
columns

df = pd.DataFrame(columns=columns)
df     
   
cell_data = [string.strip().split(':')[1] for string in cell_list]
cell_data.append(stock_number)
cell_data.append(price)
cell_data    

df.loc[0] = cell_data
df

driver.close()
driver.switch_to.window(driver.window_handles[0])

# FIRST PASS

last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(5)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

page_soup = BeautifulSoup(driver.page_source,'lxml')
row_blocks = soup.find('div',class_='search-table-wrapper-outter').find_all('div',class_='ds__item search-repeat')
len(row_blocks)

for idx, row in enumerate(row_blocks):
    
    if idx % :
        
        # got to 'details' and get link
        link = row.find('a')['href']
        tab = 'https://www.brilliance.com/' + link
        
        # open new tab
        driver.execute_script(f'''window.open('{tab}','_blank');''')
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.refresh()
    
        # pull html
        diamond_soup = BeautifulSoup(driver.page_source,'lxml')
        
        # isolate table
        table = diamond_soup.find('div',class_='tab-content col-sm-12')
    
        # stock number
        stock_number = table.find('div',class_='product__tab-price product__title-item pull-left').find('small').text
        stock_number  

        # price
        price = table.find('div',class_='product__tab-price product__title-item product__title-price pull-right no-margin-top').find('span').text
        price 
        
        cells = table.find_all('div',class_='product-specs__listing-item')
        cell_list = [cell.text for cell in cells]

        
        cell_data = [string.strip().split(':')[1] for string in cell_list]
        cell_data.append(stock_number)
        cell_data.append(price)
        cell_data    
    
        length = len(df)
        if len(cell_data) == 18:
            df.loc[length] = cell_data
        else:
            pass
      
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    








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