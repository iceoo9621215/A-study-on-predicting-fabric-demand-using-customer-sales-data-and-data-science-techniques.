import requests
import json
import pandas as pd
import time
import random
import math
import hashlib


def get_xiapi_matche(itemid, shopid):
    data = f'itemid={itemid}&shopid={shopid}'
    str_request = f"55b03{hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()}55b03"
    if_none_match = f"55b03-{hashlib.md5(str_request.encode(encoding='UTF-8')).hexdigest()}"
    return if_none_match


timeout = 6
ecode = 'utf-8-sig'


# Comment Capture
def goods_comments(item_id, shop_id, offset):
    ifnomatch = get_xiapi_matche(item_id, shop_id)
    my_headers = {
        'if-none-match-': ifnomatch,
        'X-API-SOURCE': "pc",
        'X-Requested-With': "XMLHttpRequest",
        'X-Shopee-Language': "zh-Hant"
    }
    url = 'https://shopee.tw/api/v2/item/get_ratings?filter=0&flag=1&itemid=' + str(
        item_id) + '&limit=50&offset=' + str(offset) + '&shopid=' + str(shop_id) + '&type=0'
    try:
        r = requests.get(url, headers=my_headers, timeout=timeout)
    except:
        print('SSL ERROR')
        time.sleep(random.randint(10, 50))
        try:
            r = requests.get(url, headers=my_headers, timeout=timeout)
        except:
            print('SSL ERROR-2')
            time.sleep(random.randint(50, 100))
            try:
                r = requests.get(url, headers=my_headers, verify=False, timeout=timeout)
            except:
                print('SSL ERROR-3')
                time.sleep(100)
                r = requests.get(url, headers=my_headers, verify=False, timeout=timeout)
    st = r.text.replace("\\n", "^n")
    st = st.replace("\\t", "^t")
    st = st.replace("\\r", "^r")
    gj = json.loads(st)
    try:
        return gj['data']['ratings']
    except:
        print('Failed to retrieve data. Please try again.')
        time.sleep(11)
        url = 'https://shopee.tw/api/v2/item/get_ratings?filter=0&flag=1&itemid=' + str(
            item_id) + '&limit=50&offset=' + str(offset) + '&shopid=' + str(shop_id) + '&type=0'
        try:
            r = requests.get(url, headers=my_headers)
        except:
            print('SSL ERROR')
            time.sleep(10)
        st = r.text.replace("\\n", "^n")
        st = st.replace("\\t", "^t")
        st = st.replace("\\r", "^r")
        gj = json.loads(st)
        return gj['data']['ratings']


# Import and Organize Product Data
container_product1 = pd.read_csv("Crawler Data\JAN-03-2023\Perspiration clothing\2023-01-04排汗衣_商品資料.csv")
container_product2 = pd.read_csv("Crawler Data\JAN-03-2023\Cool Clothing\2023-01-03涼感衣_商品資料.csv")
container_product3 = pd.read_csv("Crawler Data\JAN-03-2023\Heating suit\2023-01-03發熱衣_商品資料.csv")
container_product4 = pd.read_csv(
    "Crawler Data\JAN-03-2023\Windproof and waterproof jacket\2023-01-03防風防水外套_商品資料.csv")
function = [container_product1, container_product2, container_product3, container_product4]
output = ['Perspiration clothing', 'Cool Clothing', 'Heating suit', 'Windproof and waterproof jacket']
tStart = time.time()  # Start timing and start processing data
for i in range(len(function)):
    container_product = function[i]
    print('-----Start crawling message data.-----')
    theitemid = container_product['商品ID']
    theshopidlen = len(theitemid)
    theshopid = container_product['賣家ID']
    getname = container_product['商品名稱']
    theprice = container_product['價格']
    ratecount = container_product['評價數量']
    material = container_product['材質（規格)']
    commodity = container_product['商品文案']
    container_comment = pd.DataFrame()
    sold = container_product['月銷售量']
    # Start crawling each product.
    for iii in range(theshopidlen):
        print('Start crawling: ' + getname[iii])
        if ratecount[iii] > 3000:
            rate = 3000
        else:
            rate = ratecount[iii]

        volume = rate / 50
        volume = math.ceil(volume)
        page = 0
        page2 = 1  # Crawl product quantity counting
        for iiii in range(int(volume)):
            iteComment = goods_comments(item_id=int(theitemid[iii]), shop_id=int(theshopid[iii]), offset=page)
            if iteComment == None:
                print('Failed to crawl this product page')
            else:
                userid = []  # User ID
                anonymous = []  # Is it anonymous?
                commentTime = []  # Message Time
                is_hidden = []  # Hide or not
                orderid = []  # Order number
                comment_rating_star = []  # Give star
                comment = []  # Message content
                product_SKU = []  # Product specifications
                for comm in iteComment:
                    try:
                        userid.append(comm['userid'])
                    except:
                        userid.append(None)
                    try:
                        anonymous.append(comm['anonymous'])
                    except:
                        anonymous.append(None)
                    try:
                        commentTime.append(comm['ctime'])
                    except:
                        commentTime.append(None)
                    try:
                        is_hidden.append(comm['is_hidden'])
                    except:
                        is_hidden.append(None)
                    try:
                        orderid.append(comm['orderid'])
                    except:
                        orderid.append(None)
                    try:
                        comment_rating_star.append(comm['rating_star'])
                    except:
                        comment_rating_star.append(None)
                    try:
                        comment.append(comm['comment'])
                    except:
                        comment.append(None)
                    p = []
                    for pro in comm['product_items']:
                        try:
                            p.append(pro['model_name'])
                        except:
                            p.append(None)
                    product_SKU.append(p)

                commDic = {
                    '商品ID': [theitemid[iii] for x in range(len(iteComment))],
                    '賣家ID': [theshopid[iii] for x in range(len(iteComment))],
                    '商品名稱': [getname[iii] for x in range(len(iteComment))],
                    '價格': [theprice[iii] for x in range(len(iteComment))],
                    '月銷售量': [sold[iii] for x in range(len(iteComment))],
                    '使用者ID': userid,
                    '是否匿名': anonymous,
                    '留言時間': commentTime,
                    '是否隱藏': is_hidden,
                    '訂單編號': orderid,
                    '給星': comment_rating_star,
                    '留言內容': comment,
                    '商品規格': product_SKU,
                    '規格': [material[iii] for x in range(len(iteComment))],
                    '商品文案': [commodity[iii] for x in range(len(iteComment))]
                }
                container_comment = pd.concat([container_comment, pd.DataFrame(commDic)], axis=0)
                sl = random.randint(0, 2)
                print('This product is the ' + str(page2) + ' Page completed. Already crawled the.' + str(iii + 1) +
                      'Goods' + ' Rast：' + str(sl) + ' Second')
                time.sleep(sl)
                page2 = page2 + 1
                page = page + 50
    currentytime = time.localtime()  # Get system time.
    currentytime = time.strftime("%Y-%m-%d", currentytime)
    container_comment.to_csv(str(currentytime) + output[i] + '_Message data.csv', encoding=ecode, index=False)
    print(output[i] + ' Message crawling completed.')

# Calculate execution time
tEnd = time.time()  # Time's up!
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('Data storage completed, time spent (approximately).： ' + str(minute) + ' Minute(s) ' + str(second) + ' Second')
