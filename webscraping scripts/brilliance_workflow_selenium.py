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

max_price = driver.find_element_by_id('priceMax')
max_price.clear()
max_price.send_keys('600')
max_price.send_keys(Keys.ENTER)

# adjust carot min
time.sleep(2)
min_carot = driver.find_element_by_id('caratMin')
min_carot.click()
min_carot.send_keys('.23')
min_carot.send_keys(Keys.ENTER)

# MANUALLY ADJUST ADVANCED FEATURES
# color: k
# clarity: si2
# table: 49-89
# depth:45-86
# polish: g, vg, ex
# symmetry: g, vg, ex
# GIA certification
    
soup = BeautifulSoup(driver.page_source, 'lxml')




# SET UP -- columns and first row of df
first_row = soup.find('div',id='brl-diamond-search-table').find('div',class_='ds__item search-repeat')

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

# scroll all the way down
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(4)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

# grab entire page
page_soup = BeautifulSoup(driver.page_source,'lxml')
page_soup

# grab all rows
row_blocks = page_soup.find_all('div',class_='ds__item search-repeat')
len(row_blocks)

# go through each row
for idx, row in enumerate(row_blocks):
    
    if idx % 3 == 0:
        
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
        print(stock_number, ':',idx)  

        # price
        price = table.find('div',class_='product__tab-price product__title-item product__title-price pull-right no-margin-top').find('span').text
        print(price,':', idx)
        
        # grab all the cells in the table
        cells = table.find_all('div',class_='product-specs__listing-item')
        cell_list = [cell.text for cell in cells]

        # grab only the features
        cell_data = [string.strip().split(':')[1] for string in cell_list]
        cell_data.append(stock_number)
        cell_data.append(price)
        cell_data    
        
        # append to df
        length = len(df)
        if len(cell_data) == 18:
            df.loc[length] = cell_data
        else:
            pass
        
        # close tab and switch back
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    df.to_csv('brilliance.csv')
  
# 500 - 600: 1,909

# ----------------

# two loops, idx % 10
# 600 - 700: 5,367
# 700 - 800: 5,046

# five loops: idx % 5
# 800 - 900: 2,484
# 900 - 1000: 2,705
# 1000 - 1100: 2,432
# 1100 - 1200: 1,748
# 1200 - 1300: 1,230

# once, all
# 1300 - 1400: 817
    
# initialize another df
df2 = pd.DataFrame(columns=columns)
df2
  
min_val = 500
max_val = 600

for j in range (2):
    # scroll to top
    driver.execute_script('window.scrollTo(0,200)')
    
    # set new prices
    min_val = max_val
    max_val += 100
    print(max_val)
        
    # adjust price
    min_price = driver.find_element_by_id('priceMin')
    min_price.clear()
    min_price.send_keys(min_val)
  
    max_price = driver.find_element_by_id('priceMax')
    max_price.clear()
    max_price.send_keys(max_val)
    max_price.send_keys(Keys.ENTER)
    print('Price Range set',j)
    
    time.sleep(5)

    # scroll all the way down
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    
    # grab entire page
    page_soup = BeautifulSoup(driver.page_source,'lxml')
    page_soup
        
    # grab all rows
    row_blocks = page_soup.find_all('div',class_='ds__item search-repeat')
    len(row_blocks)
    
    for idx, row in enumerate(row_blocks):
    
        if idx % 10 == 0:
        
            # got to 'details' and get link
            link = row.find('a')['href']
            tab = 'https://www.brilliance.com/' + link
                    
            # open new tab and switch driver
            driver.execute_script(f'''window.open('{tab}','_blank');''')
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)
            driver.refresh()
                
            # pull html from new tab
            diamond_soup = BeautifulSoup(driver.page_source,'lxml')
                    
            # isolate table
            table = diamond_soup.find('div',class_='tab-content col-sm-12')
                
            # stock number
            stock_number = table.find('div',class_='product__tab-price product__title-item pull-left').find('small').text
            print(stock_number, ':',idx)  
            
            # price
            price = table.find('div',class_='product__tab-price product__title-item product__title-price pull-right no-margin-top').find('span').text
            print(price,':', idx)
                    
            # grab all the cells in the table
            cells = table.find_all('div',class_='product-specs__listing-item')
            cell_list = [cell.text for cell in cells]
            
            # grab only the features
            cell_data = [string.strip().split(':')[1] for string in cell_list]
            cell_data.append(stock_number)
            cell_data.append(price)
            cell_data    
                    
            # append to df
            length = len(df2)
            if len(cell_data) == 18:
                df2.loc[length] = cell_data
            else:
                pass
                    
            # close tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
                
        else:
            pass   
    
    print('PAGE GATHERED:',j)    
    

# two loops, idx % 3
# 1400 - 1600: 2,992
# 1600 - 1800: 3,059

min_val = 1300
max_val = 1400

for j in range (2):
    # scroll to top
    driver.execute_script('window.scrollTo(0,200)')
    
    # set new prices
    min_val = max_val
    max_val += 200
    print(max_val)
        
    # adjust price
    min_price = driver.find_element_by_id('priceMin')
    min_price.clear()
    min_price.send_keys(min_val)
  
    max_price = driver.find_element_by_id('priceMax')
    max_price.clear()
    max_price.send_keys(max_val)
    max_price.send_keys(Keys.ENTER)
    print('Price Range set',j)
    
    time.sleep(5)

    # scroll all the way down
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    
    # grab entire page
    page_soup = BeautifulSoup(driver.page_source,'lxml')
    page_soup
        
    # grab all rows
    row_blocks = page_soup.find_all('div',class_='ds__item search-repeat')
    len(row_blocks)
    
           
    for idx, row in enumerate(row_blocks):
            
        if idx % 3 == 0:
                
            # got to 'details' and get link
            link = row.find('a')['href']
            tab = 'https://www.brilliance.com/' + link
                        
            # open new tab and switch driver
            driver.execute_script(f'''window.open('{tab}','_blank');''')
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)
            driver.refresh()
                
            # pull html from new tab
            diamond_soup = BeautifulSoup(driver.page_source,'lxml')
                        
            # isolate table
            table = diamond_soup.find('div',class_='tab-content col-sm-12')
                    
            # stock number
            stock_number = table.find('div',class_='product__tab-price product__title-item pull-left').find('small').text
            print(stock_number, ':',idx)  
                
            # price
            price = table.find('div',class_='product__tab-price product__title-item product__title-price pull-right no-margin-top').find('span').text
            print(price,':', idx)
                        
            # grab all the cells in the table
            cells = table.find_all('div',class_='product-specs__listing-item')
            cell_list = [cell.text for cell in cells]
                
            # grab only the features
            cell_data = [string.strip().split(':')[1] for string in cell_list]
            cell_data.append(stock_number)
            cell_data.append(price)
            cell_data    
                        
            # append to df
            length = len(df2)
            if len(cell_data) == 18:
                df2.loc[length] = cell_data
            else:
                pass
            
            # close tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
                    
        else:
            pass   
        
    print('PAGE GATHERED:',j)

df2.to_csv('brilliance_2.csv')


# three loops, idx % 3
# 1600 - 1800: 3,059
# 1800 - 2000: 2,146
# 2000 - 2300: 2,126

# three loops, all
# 2300 - 2600: 1,302
# 2600 - 2900: 1,297
# 2900 - 3200: 1,130

# once, all
# 3200 - 3800

min_val = 1400
max_val = 1600

for j in range (3):
    # scroll to top
    driver.execute_script('window.scrollTo(0,200)')
    
    # set new prices
    min_val = max_val
    max_val += 200
    print(max_val)
        
    # adjust price
    min_price = driver.find_element_by_id('priceMin')
    min_price.clear()
    min_price.send_keys(min_val)
  
    max_price = driver.find_element_by_id('priceMax')
    max_price.clear()
    max_price.send_keys(max_val)
    max_price.send_keys(Keys.ENTER)
    print('Price Range set',j)
    
    time.sleep(5)

    # scroll all the way down
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    
    # grab entire page
    page_soup = BeautifulSoup(driver.page_source,'lxml')
    page_soup
        
    # grab all rows
    row_blocks = page_soup.find_all('div',class_='ds__item search-repeat')
    len(row_blocks)
    
           
    for idx, row in enumerate(row_blocks):
            
        # got to 'details' and get link
        link = row.find('a')['href']
        tab = 'https://www.brilliance.com/' + link
                        
        # open new tab and switch driver
        driver.execute_script(f'''window.open('{tab}','_blank');''')
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.refresh()
                
        # pull html from new tab
        diamond_soup = BeautifulSoup(driver.page_source,'lxml')
                        
        # isolate table
        table = diamond_soup.find('div',class_='tab-content col-sm-12')
                    
        # stock number
        stock_number = table.find('div',class_='product__tab-price product__title-item pull-left').find('small').text
        print(stock_number, ':',idx)  
        
        # price
        price = table.find('div',class_='product__tab-price product__title-item product__title-price pull-right no-margin-top').find('span').text
        print(price,':', idx)
                        
        # grab all the cells in the table
        cells = table.find_all('div',class_='product-specs__listing-item')
        cell_list = [cell.text for cell in cells]
                
        # grab only the features
        cell_data = [string.strip().split(':')[1] for string in cell_list]
        cell_data.append(stock_number)
        cell_data.append(price)
        cell_data    
                        
        # append to df
        length = len(df2)
        if len(cell_data) == 18:
            df2.loc[length] = cell_data
        else:
            pass
            
        # close tab and switch back
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
                    
    print('PAGE GATHERED:',j)
    df2.to_csv('brilliance_2.csv')

# five loops, all
# 3800 - 4800
# 4800 - 5800
# 5800 - 6800
# 6800 - 7800
# 7800 - 8800

min_val = 3200
max_val = 3800

for j in range (5):
    # scroll to top
    driver.execute_script('window.scrollTo(0,200)')
    
    # set new prices
    min_val = max_val
    max_val += 1000
    print(max_val)
        
    # adjust price
    min_price = driver.find_element_by_id('priceMin')
    min_price.clear()
    min_price.send_keys(min_val)
  
    max_price = driver.find_element_by_id('priceMax')
    max_price.clear()
    max_price.send_keys(max_val)
    max_price.send_keys(Keys.ENTER)
    print('Price Range set',j)
    
    time.sleep(5)

    # scroll all the way down
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    
    # grab entire page
    page_soup = BeautifulSoup(driver.page_source,'lxml')
    page_soup
        
    # grab all rows
    row_blocks = page_soup.find_all('div',class_='ds__item search-repeat')
    len(row_blocks)
    
           
    for idx, row in enumerate(row_blocks):
            
        # got to 'details' and get link
        link = row.find('a')['href']
        tab = 'https://www.brilliance.com/' + link
                        
        # open new tab and switch driver
        driver.execute_script(f'''window.open('{tab}','_blank');''')
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.refresh()
                
        # pull html from new tab
        diamond_soup = BeautifulSoup(driver.page_source,'lxml')
                        
        # isolate table
        table = diamond_soup.find('div',class_='tab-content col-sm-12')
                    
        # stock number
        stock_number = table.find('div',class_='product__tab-price product__title-item pull-left').find('small').text
        print(stock_number, ':',idx)  
        
        # price
        price = table.find('div',class_='product__tab-price product__title-item product__title-price pull-right no-margin-top').find('span').text
        print(price,':', idx)
                        
        # grab all the cells in the table
        cells = table.find_all('div',class_='product-specs__listing-item')
        cell_list = [cell.text for cell in cells]
                
        # grab only the features
        cell_data = [string.strip().split(':')[1] for string in cell_list]
        cell_data.append(stock_number)
        cell_data.append(price)
        cell_data    
                        
        # append to df
        length = len(df2)
        if len(cell_data) == 18:
            df2.loc[length] = cell_data
        else:
            pass
            
        # close tab and switch back
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
                    
    print('PAGE GATHERED:',j)

df2.to_csv('brilliance_2.csv')

# once, all
# 8800 - 15000

min_val = 7800
max_val = 8800

for j in range (1):
    # scroll to top
    driver.execute_script('window.scrollTo(0,200)')
    
    # set new prices
    min_val = max_val
    max_val += 5200
    print(max_val)
        
    # adjust price
    min_price = driver.find_element_by_id('priceMin')
    min_price.clear()
    min_price.send_keys(min_val)
  
    max_price = driver.find_element_by_id('priceMax')
    max_price.clear()
    max_price.send_keys(max_val)
    max_price.send_keys(Keys.ENTER)
    print('Price Range set',j)
    
    time.sleep(5)

    # scroll all the way down
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    
    # grab entire page
    page_soup = BeautifulSoup(driver.page_source,'lxml')
    page_soup
        
    # grab all rows
    row_blocks = page_soup.find_all('div',class_='ds__item search-repeat')
    len(row_blocks)
    
           
    for idx, row in enumerate(row_blocks):
            
        # got to 'details' and get link
        link = row.find('a')['href']
        tab = 'https://www.brilliance.com/' + link
                        
        # open new tab and switch driver
        driver.execute_script(f'''window.open('{tab}','_blank');''')
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.refresh()
                
        # pull html from new tab
        diamond_soup = BeautifulSoup(driver.page_source,'lxml')
                        
        # isolate table
        table = diamond_soup.find('div',class_='tab-content col-sm-12')
                    
        # stock number
        stock_number = table.find('div',class_='product__tab-price product__title-item pull-left').find('small').text
        print(stock_number, ':',idx)  
        
        # price
        price = table.find('div',class_='product__tab-price product__title-item product__title-price pull-right no-margin-top').find('span').text
        print(price,':', idx)
                        
        # grab all the cells in the table
        cells = table.find_all('div',class_='product-specs__listing-item')
        cell_list = [cell.text for cell in cells]
                
        # grab only the features
        cell_data = [string.strip().split(':')[1] for string in cell_list]
        cell_data.append(stock_number)
        cell_data.append(price)
        cell_data    
                        
        # append to df
        length = len(df2)
        if len(cell_data) == 18:
            df2.loc[length] = cell_data
        else:
            pass
            
        # close tab and switch back
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
                    
    print('PAGE GATHERED:',j)

driver.close()

df2.to_csv('brilliance_2.csv')