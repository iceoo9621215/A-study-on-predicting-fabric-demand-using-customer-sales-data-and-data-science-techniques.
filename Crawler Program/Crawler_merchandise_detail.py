# 僅供學術上使用，請勿作為商業用途
# Egbert Hsu 2023.1
# Import Library
import json
import pandas as pd
import time
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire.utils import decode
import random
from selenium.common.exceptions import TimeoutException

# File Import and Defined Encoding
container_product1 = pd.read_csv("Crawler Data\JAN-03-2023\Perspiration clothing\2023-01-04排汗衣_商品資料.csv")
container_product2 = pd.read_csv("Crawler Data\JAN-03-2023\Cool Clothing\2023-01-03涼感衣_商品資料.csv")
container_product3 = pd.read_csv("Crawler Data\JAN-03-2023\Heating suit\2023-01-03發熱衣_商品資料.csv")
container_product4 = pd.read_csv("Crawler Data\JAN-03-2023\Windproof and waterproof jacket\2023-01-03防風防水外套_商品資料.csv")
File = [container_product4]
Type = ['Perspiration clothing', 'Cool Clothing', 'Heating suit', 'Windproof and waterproof jacket']
ecode = 'utf-8-sig'
timeout = 6
tStart = time.time()


# proxy
def get_proxy_ip():
    r = None
    while not r:
        try:
            r = requests.get('http://proxy.husan.cc')
        except:
            time.sleep(1)
    return r.text


# Define Crawler Merchandise Function
def selenium(url, item_id, shop_id):
    global driver, product
    getPacket = ''
    situation = False
    while situation == False:
        try:
            driver.get(url)
            situation = True
        except TimeoutException as e:
            print("Page load Timeout Occurred. Quitting !!!")
            driver.quit()
            # proxy
            ip = get_proxy_ip()
            options.add_argument('--proxy-server=%s' % ip)
            # login and open chrome
            if __name__ == '__main__':
                with open(r'C:\Users\Tester\AppData\Roaming\JetBrains\PyCharmCE2022.3\scratches\scratch.json') as f:
                    cookies = json.load(f)
                driver = webdriver.Chrome(service=service, chrome_options=options)
                driver.get('https://shopee.tw/')
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()
            driver.set_page_load_timeout(50)
            time.sleep(random.randint(5, 10))
    time.sleep(random.randint(4, 9))
    for scroll in range(random.randint(1, 3)):
        driver.execute_script('window.scrollBy(0,250)')
        time.sleep(random.randint(0, 2))
        try:
            product = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div/div/div/div')
            product = product.text
        except:
            try:
                bad = driver.find_element(By.XPATH, '/html/body/center[1]/h1')
                print(bad)
                product = '此商品不存在'
            except:
                try:
                    error404 = driver.find_element(By.XPATH, '/html/body/main/div[2]/p[1]')
                    print(error404)
                    product = '此商品不存在'
                except:
                    product = '此商品不存在'
                    print('Not find error, but the page can be not found!!, now system sleep 30 second')
                    time.sleep(30)
        for request in driver.requests:
            if product == '此商品不存在':
                break
            if request.response:
                # 挑出商品詳細資料的json封包
                if 'https://shopee.tw/api/v4/item/get?itemid=' + str(item_id) + '&shopid=' + str(shop_id) in request.url:
                    # decode body
                    response = request.response
                    body = decode(response.body, response.headers.get('Content-Encoding'))
                    decoded_body = body.decode('utf8')
                    getPacket = decoded_body.replace("\\n", "^n")
                    getPacket = getPacket.replace("\\t", "^t")
                    getPacket = getPacket.replace("\\r", "^r")
        if getPacket != '':
            gj = json.loads(getPacket)
            print('Information obtained successfully')
            try:
                return gj['data']
            except:
                print(gj)
                time.sleep(5)
                getPacket = ''
                return None
        else:
            return getPacket


def Merchandise_detail(url, item_id, shop_id):
    global good
    error = 1
    while error > 0:
        if error > 3:
            print('Failed to get this item, will skip')
            good = ''
            break
        good = selenium(url, item_id, shop_id)
        if good == '' or good == None:
            print('Failed to get product information, Reacquire:' + str(error))
            error = error + 1
        elif good == '此商品不存在':
            good = ''
            break
        else:
            break
    return good


# Automatic Download ChromeDriver
service = ChromeService(executable_path=ChromeDriverManager().install())

# Turn off notification reminders
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("disable-infobars")
options.add_argument('--ignore-ssl-error')

# Do not load pictures, improve crawler speed
options.add_argument('blink-settings=imagesEnabled=false')

# proxy
ip = get_proxy_ip()
options.add_argument('--proxy-server=%s' % ip)
options.add_argument("start-maximized")

# login and open chrome
if __name__ == '__main__':
    with open(r'C:\Users\Tester\AppData\Roaming\JetBrains\PyCharmCE2022.3\scratches\scratch.json') as f:
        cookies = json.load(f)
    driver = webdriver.Chrome(service=service, chrome_options=options)
    driver.get('https://shopee.tw/')
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
driver.set_page_load_timeout(20)
time.sleep(random.randint(5, 10))

# Start crawler
for i in range(len(File)):
    # Prepare tables for storing data
    container_product = pd.DataFrame()

    # Prepare an array for storing data
    sold = []  # monthly sales
    itemid = []  # Product ID
    shopid = []  # Store ID
    name = []  # product name
    brand = []
    stock = []
    price = []
    ctime = []
    description = []
    can_use_bundle_deal = []
    can_use_wholesale = []
    historical_sold = []
    is_cc_installment_payment_eligible = []
    is_official_shop = []
    liked_count = []
    shop_location = []
    SKU = []
    cmt_count = []
    five_star = []
    four_star = []
    three_star = []
    two_star = []
    one_star = []
    rating_star = []
    attributes = []
    error = []
    good_count = 90
    for ii in range(len(File[i]['商品ID'])):
        good = ii
        url = File[i]['商品連結'][ii]
        item_id = File[i]['商品ID'][ii]
        shop_id = File[i]['賣家ID'][ii]
        print('開始爬取：' + File[i]['商品名稱'][ii] + ' 順位： ' + str(ii + 1))
        itemDetail = Merchandise_detail(url, item_id, shop_id)
        if itemDetail == '':
            error.append(File[i]['商品名稱'][ii])
            print('-----This item is no longer available.Maybe Crawler Error or Not Find Merchandise-------')
            continue
        print('Data Capture Successful')

        price.append(itemDetail['price'] / 100000)  # Price
        itemid.append(itemDetail['itemid'])  # Product ID
        shopid.append(itemDetail['shopid'])  # Store ID
        name.append(itemDetail['name'])  # Product name
        sold.append(itemDetail['sold'])  # monthly sales
        brand.append(itemDetail['brand'])  # brand
        stock.append(itemDetail['stock'])  # inventory quantity
        ctime.append(itemDetail['ctime'])  # Added time
        description.append(itemDetail['description'])  # Product copywriting
        can_use_bundle_deal.append(itemDetail['can_use_bundle_deal'])  # Can it be purchased together
        can_use_wholesale.append(itemDetail['can_use_wholesale'])  # Is it possible to buy in bulk
        historical_sold.append(itemDetail['historical_sold'])  # historical sales
        # Can I pay in installments?
        is_cc_installment_payment_eligible.append(itemDetail['is_cc_installment_payment_eligible'])
        is_official_shop.append(itemDetail['is_official_shop'])  # Whether it is an official seller account
        liked_count.append(itemDetail['liked_count'])  # Number of likes

        # SKU
        all_sku = []
        for sk in itemDetail['models']:
            all_sku.append(sk['name'])
        SKU.append(all_sku)  # SKU

        shop_location.append(itemDetail['shop_location'])  # Store Location
        cmt_count.append(itemDetail['cmt_count'])  # number of comments
        five_star.append(itemDetail['item_rating']['rating_count'][5])  # Five star
        four_star.append(itemDetail['item_rating']['rating_count'][4])  # Four star
        three_star.append(itemDetail['item_rating']['rating_count'][3])  # Three Star
        two_star.append(itemDetail['item_rating']['rating_count'][2])  # Two star
        one_star.append(itemDetail['item_rating']['rating_count'][1])  # One Star
        rating_star.append(itemDetail['item_rating']['rating_star'])  # Rate

        # Product specifications
        all_attributes = []
        if itemDetail['attributes'] == None:
            attributes.append(['None'])
        else:
            for at in itemDetail['attributes']:
                if at['name'] == '材質':
                    all_attributes.append(at['value'])
            attributes.append(all_attributes)  # SKU

        # Store data regularly to prevent data loss
        while ii == good_count:
            good_count = good_count + random.randint(80, 120)
            print('Next Restart item Number:' + str(good_count + 1))
            driver.quit()
            dic = {
                '商品ID': itemid,
                '賣家ID': shopid,
                '商品名稱': name,
                '品牌': brand,
                '價格': price,
                '月銷售量': sold,
                '歷史銷售量': historical_sold,
                '存貨數量': stock,
                '評價數量': cmt_count,
                '五星': five_star,
                '四星': four_star,
                '三星': three_star,
                '二星': two_star,
                '一星': one_star,
                '評分': rating_star,
                '商品文案': description,
                '可否搭配購買': can_use_bundle_deal,
                '可否大量批貨購買': can_use_wholesale,
                '可否分期付款': is_cc_installment_payment_eligible,
                '是否官方賣家帳號': is_official_shop,
                '喜愛數量': liked_count,
                '商家地點': shop_location,
                'SKU': SKU,
                '材質（規格)': attributes,
            }
            # Data Integrated
            container_product = pd.concat([container_product, pd.DataFrame(dic)], axis=0)
            print('Current Merchandise Count： ' + str(len(container_product)))
            container_product.to_csv('shopeeAPIData' + str(ii + 1) + '_Product.csv', encoding=ecode)
            # Reset an array for storing data
            sold = []  # monthly sales
            itemid = []  # Product ID
            shopid = []  # Store ID
            name = []  # product name
            brand = []
            stock = []
            price = []
            ctime = []
            description = []
            can_use_bundle_deal = []
            can_use_wholesale = []
            historical_sold = []
            is_cc_installment_payment_eligible = []
            is_official_shop = []
            liked_count = []
            shop_location = []
            SKU = []
            cmt_count = []
            five_star = []
            four_star = []
            three_star = []
            two_star = []
            one_star = []
            rating_star = []
            attributes = []
            # proxy
            ip = get_proxy_ip()
            options.add_argument('--proxy-server=%s' % ip)
            options.add_argument("start-maximized")
            # login and open chrome
            if __name__ == '__main__':
                with open(r'C:\Users\Tester\AppData\Roaming\JetBrains\PyCharmCE2022.3\scratches\scratch.json') as f:
                    cookies = json.load(f)
                driver = webdriver.Chrome(service=service, chrome_options=options)
                driver.get('https://shopee.tw/')
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()
            driver.set_page_load_timeout(15)
            time.sleep(random.randint(20, 35))

        # Rast（prevent anti-reptiles）
        sleep = random.randint(1, 5)
        print('Successful Capture，Item Code： ' + str(ii + 1) + ' ,Rest' + str(sleep) + 'Second')
        time.sleep(sleep)

    dic = {
        '商品ID': itemid,
        '賣家ID': shopid,
        '商品名稱': name,
        '品牌': brand,
        '價格': price,
        '月銷售量': sold,
        '歷史銷售量': historical_sold,
        '存貨數量': stock,
        '評價數量': cmt_count,
        '五星': five_star,
        '四星': four_star,
        '三星': three_star,
        '二星': two_star,
        '一星': one_star,
        '評分': rating_star,
        '商品文案': description,
        '可否搭配購買': can_use_bundle_deal,
        '可否大量批貨購買': can_use_wholesale,
        '可否分期付款': is_cc_installment_payment_eligible,
        '是否官方賣家帳號': is_official_shop,
        '喜愛數量': liked_count,
        '商家地點': shop_location,
        'SKU': SKU,
        '材質（規格)': attributes,
    }

    # Data integration and output
    currentytime = time.localtime()  # Get system time
    currentytime = time.strftime("%Y-%m-%d", currentytime)
    log = pd.DataFrame(error)
    log.to_csv('error.csv')
    container_product = pd.concat([container_product, pd.DataFrame(dic)], axis=0)
    container_product.to_csv(str(currentytime) + Type[i] + '_商品資料.csv', encoding=ecode, index=False)
    print(Type[i] + ' Product information crawling completed---------')
    time.sleep(180)

# Calculate execution time
driver.quit()
tEnd = time.time()  # end of time
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('Data storage is complete, time spent (approximately)： ' + str(minute) + ' Minute ' + str(second) + 'Second')
