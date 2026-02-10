
cookie = "x_wbaas_token=1.1000.7b88182a45834cda9c19d83a11475855.MHwxNzYuMTUuMTY0LjI1fE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDQuMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzcxNTkxODg1fHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3MDk4NzA4NXwx.MEUCIAfklxTyrKkvNX6hoUuTR76ETN+XljS1AVVOCxNrmQ0oAiEAit/4Nq2BDq58hjH4uGPjb1SQN5fWp/j4fErNB2n7eEY=; _wbauid=9255161901770382035; routeb=1770404947.732.60.384847|28979c6168ec4738f0fcb8539a6d5f12"

from dataclasses import dataclass
@dataclass
class DataClass:
    description: str = None
    imgs: str = None
    urlCard: str = None
    article: str = None
    name: str = None
    price: str = None
    supplierName: str = None
    url_supplier: str = None
    qty: str = None
    sizes: str = None
    rating: str = None
    feedBack: str = None
    opts: str = None
    sizesName: str = None
    imgs: str = None


def getHeaders(cookie:str):
    return {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "deviceid": "site_ad042367acf04931ad4a5c4aefe6ccfe",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-queryid": "qid925516190177038203520260206124715",
    "x-requested-with": "XMLHttpRequest",
    "x-spa-version": "13.22.3",
    "x-userid": "0",
    "cookie": cookie
}


def get_params(query:str, page:int):
    params = {
        "appType": "1",
        "curr": "rub",
        "dest": DEST,
        "hide_dtype": "9",
        "hide_vflags": "4294967296",
        "lang": "ru",
        "page": str(page),
        "query": query,
        "resultset": "catalog",
        "sort": "popular",
        "spp": "30",
    }
    return params


headers = {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "deviceid": "site_ad042367acf04931ad4a5c4aefe6ccfe",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-queryid": "qid925516190177038203520260206124715",
    "x-requested-with": "XMLHttpRequest",
    "x-spa-version": "13.22.3",
    "x-userid": "0",
    "cookie": cookie
}
#региональность
DEST = "123586213"
URL_SEARCH = "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search"

def getBasket(id:str):
    # Определяем сервер. Если длина id 8 то по 3 первым цифрам, если 9 то по 4 цифрам
    vol = ''
    if len(id) == 8:
        vol = id[:3]
    elif len(id)==9:
        vol = id[:4]
    elif len(id)==7:
        vol=id[:2]
    else:
        print('Другие сервера')

    #Тут жесткий костыль, когда я инициализированную переменную типа String, а после переназначаю в Int 😂
    vol = int(vol)
    basket = ''
    if vol>=0 and vol<=143:basket='01'
    if vol>143 and vol<=287:basket='02'
    if vol>287 and vol<=431:basket='03'
    if vol>431 and vol<=719:basket='04'
    if vol>719 and vol<=1007:basket='05'
    if vol>1007 and vol<=1061:basket='06'
    if vol>1061 and vol<=1115:basket='07'
    if vol>1115 and vol<=1169:basket='08'
    if vol>1169 and vol<=1313:basket='09'
    if vol>1313 and vol<=1601:basket='10'
    if vol>1601 and vol<=1655:basket='11'
    if vol>1655 and vol<=1919:basket='12'
    if vol>1919 and vol<=2045:basket='13'
    if vol>2045 and vol<=2189:basket='14'
    if vol>2189 and vol<=2405:basket='15'
    if vol>2405 and vol<=2621:basket='16'
    if vol>2621 and vol<=2837:basket='17'
    if vol>2837 and vol<=3053:basket='18'
    if vol>3053 and vol<=3269:basket='19'
    if vol>3269 and vol<=3485:basket='20'
    if vol>3485 and vol<=3701:basket='21'
    if vol>3701 and vol<=3917:basket='22'
    if vol>3917 and vol<=4133:basket='23'
    if vol>4133 and vol<=4349:basket='24'
    if vol>4349 and vol<=4565:basket='25'
    if vol>4565 and vol<=4877:basket='26'
    if vol>4877 and vol<=5189:basket='27'
    if vol>5189 and vol<=5501:basket='28'
    if vol>5501 and vol<=5813:basket='29'
    if vol>5813 and vol<=6125:basket='30'
    if vol>6125 and vol<=6437:basket='31'
    if vol>6437 and vol<=6749:basket='32'
    if vol>6749 and vol<=7061:basket='33'
    if vol>7061 and vol<=7373:basket='34'
    if vol>7373 and vol<=7685:basket='35'
    if vol>7685 and vol<=7997:basket='36'
    if vol>7997 and vol<=8309:basket='37'
    if vol>8309: basket='38'
    return basket

def getServer(id:str):
    vol = ''
    if len(id) == 8:
        vol = id[:3]
        part = id[:5]
    elif len(id) == 9:
        vol=id[:4]
        part = id[:6]
    elif len(id)==7:
        part = id[:4]
        vol = id[0:2]
    return f'https://basket-{getBasket(id)}.wbbasket.ru/vol{vol}/part{part}/{id}'

def getUrlCard(id:str):
    return getServer(id) + '/info/ru/card.json'

def getUrlImg(id:str, count:int):
    urls = []
    for i in range(1,count+1):
        urls.append(getServer(id) + f'/images/big/{i}.webp')
    return ', '.join(urls)

