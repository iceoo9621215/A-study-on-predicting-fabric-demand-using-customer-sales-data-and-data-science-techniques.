# 僅供學術上使用，請勿作為商業用途
# Egbert Hsu 2023.1
# import package or library
import pandas as pd
import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import re
import random
# define search page and merchandise
ecode = 'utf-8-sig'
keyword = '排汗衣'
page = 50
timeout = 6
# Import ChromeDriver
service = ChromeService('/Users/xuyuteng/PycharmProjects/Shopee Crawler/venv/bin/chromedriver')
# Turn Off Notification
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
# Open Chrome browser
driver = webdriver.Chrome(service=service, chrome_options=options)
time.sleep(random.randint(5, 10))
# Open site
driver.get('https://shopee.tw/search?keyword=' + keyword)
time.sleep(random.randint(10, 20))

print('---------- start crawling ----------')
tStart = time.time()  # Start timer
container_product = pd.DataFrame()
for i in range(int(page)):
    # Prepare an array for storing data
    link = []
    itemid = []  # Product ID
    shopid = []  # Store ID
    name = []  # product name
    price = []

    driver.get('https://shopee.tw/search?keyword=' + str(keyword) + '&ratingFilter=1&page=' + str(i))
    time.sleep(random.randint(5, 10))
    # scroll page
    for scroll in range(6):
        driver.execute_script('window.scrollBy(0,1000)')
        time.sleep(random.randint(3, 10))

    # Capture Product data
    for item, thename in zip(driver.find_elements(by=By.XPATH, value='//*[@data-sqe="link"]'),
                             driver.find_elements(by=By.XPATH, value='//*[@data-sqe="name"]')):
        # Product ID、Store ID、Product link
        getID = item.get_attribute('href')
        theitemid = int((getID[getID.rfind('.') + 1:getID.rfind('?')]))
        theshopid = int(getID[getID[:getID.rfind('.')].rfind('.') + 1:getID.rfind('.')])
        link.append(getID)
        itemid.append(theitemid)
        shopid.append(theshopid)

        # Product name String Process
        getname = thename.text.split('\n')[0]
        name.append(getname)

        # Price
        thecontent = item.text
        thecontent = thecontent[(thecontent.find(getname)) + len(getname):]
        thecontent = thecontent.replace('萬', '000')
        thecut = thecontent.split('\n')

        if bool(re.search('市|區|縣|鄉|海外|中國大陸', thecontent)):  # Sometimes there is no product location information
            if bool(re.search('已售出', thecontent)):  # Sometimes there is no sales information
                if '出售' in thecut[-3][1:]:
                    theprice = thecut[-4][1:]
                else:
                    theprice = thecut[-3][1:]

            else:
                theprice = thecut[-2][1:]
        else:
            if re.search('已售出', thecontent):  # Sometimes there is no sales information
                theprice = thecut[-2][1:]
            else:
                theprice = thecut[-1][1:]

        theprice = theprice.replace('$', '')
        theprice = theprice.replace(',', '')
        theprice = theprice.replace('售', '')
        theprice = theprice.replace('出', '')
        theprice = theprice.replace(' ', '')
        if ' - ' in theprice:
            theprice = (int(theprice.split(' - ')[0]) + int(theprice.split(' - ')[1])) / 2
        if '-' in theprice:
            theprice = (int(theprice.split('-')[0]) + int(theprice.split('-')[1])) / 2
        price.append(int(theprice))


    dic = {
        '商品ID': itemid,
        '賣家ID': shopid,
        '商品名稱': name,
        '商品連結': link,
        '價格': price,
    }

    # Data Integration
    container_product = pd.concat([container_product, pd.DataFrame(dic)], axis=0)
    print('Currently accumulating goods： ' + str(len(container_product)))
    time.sleep(random.randint(12, 35))

container_product.to_csv(keyword + '_商品資料.csv', encoding=ecode, index=False)
# Data Standardization
amount_before = len(container_product['商品ID'])
# exclude duplicates
container_product = container_product.drop_duplicates(subset='商品ID')
# exclude special keyw  ord merchandise
keyword_special = ['兒童', '嬰兒', '幼兒', '客製化', '客製化衣服']
for special in range(len(keyword_special)):
    container_product = container_product.drop(container_product[container_product['商品名稱'].str.contains
        (keyword_special[special])].index)
amount_after = len(container_product['商品ID'])
print('Drop amount:' + str(amount_before - amount_after))

# File Output output
currentytime = time.localtime()  # Get system time
currentytime = time.strftime("%Y-%m-%d", currentytime)
container_product.to_csv(str(currentytime) + keyword + '_product information.csv', encoding=ecode, index=False)
tEnd = time.time()  # end of time
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('Data storage is complete, time spent (approximately)： ' + str(minute) + ' min ' + str(second) + 'second')
driver.close()