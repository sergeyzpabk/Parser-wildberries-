import time
import requests
import aiohttp
from getserver import getUrlCard, getUrlImg
import asyncio

query = "пальто из натуральной шерсти"
#query = "пальто натуральной шерсти"

cookie = "x_wbaas_token=1.1000.7b88182a45834cda9c19d83a11475855.MHwxNzYuMTUuMTY0LjI1fE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDQuMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzcxNTkxODg1fHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3MDk4NzA4NXwx.MEUCIAfklxTyrKkvNX6hoUuTR76ETN+XljS1AVVOCxNrmQ0oAiEAit/4Nq2BDq58hjH4uGPjb1SQN5fWp/j4fErNB2n7eEY=; _wbauid=9255161901770382035; routeb=1770404947.732.60.384847|28979c6168ec4738f0fcb8539a6d5f12"

#региональность
dest = "123586213"

URL_SEARCH = "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search"

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


async def detCard_(
    self,
    sid:str,
    proxy:str,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore
):
    pass



def get_params(query:str, page:int):
    params = {
        "appType": "1",
        "curr": "rub",
        "dest": dest,
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


def parse_card(detail : dict ):
    try:
        id = str(detail['id'])
        responseCard = requests.get(
            getUrlCard(id),
            headers=headers,
        ).json()
        print('CARD')
        print(responseCard)
        print('---CARD---')
        #получаем описание

        description = responseCard['description']
        imgs = getUrlImg(id = str(id), count = int(responseCard['media']['photo_count']))
        ###card

        urlCard = f'https://www.wildberries.ru/catalog/{id}/detail.aspx'
        print(f'Успешно получили данные для {urlCard}')
        article = id
        name = responseCard['imt_name']

        ### Может быть что размеры разные и цены тоже
        price = None
        ###

        #Имя селлера
        supplierName = detail['supplier']

        #url селлера
        url_supplier = f'https://www.wildberries.ru/seller/{detail['supplierId']}'

        ###Получаем размеры + Остатки)
        # остатки товаров по всем размерам
        qty = 0
        # все размеры по name
        sizes = []
        # размеры, через запятую
        sizesName = ''

        for q in detail['sizes']:
            sizes.append(q['name'])
            if 'stocks' in q:
                if q['stocks'] != []:
                    if 'qty' in q['stocks'][0]:
                        qty = qty + int(q['stocks'][0]['qty'])
        sizesName =','.join(sizes)

        ###

        ###
        # все размеры по origname
        """
        sizes_origName = ''
        sizesOrig = []
        for q in resDetail['products'][0]['sizes']:
            sizesOrig.append(q['origName'])
        sizes_origName = ','.join(sizes)
        """
        ###

        rating = str(detail['reviewRating'])
        feedBack = str(detail['feedbacks'])


        ###Характеристики
        for opt in responseCard['options']:
            print(f'{opt['name']} : {opt['value']} ')
        ###


        print('------------card-------------')
        print(urlCard)
        print(article)
        print(name)
        print(price)
        print(supplierName)
        print(url_supplier)
        print(qty)
        print(sizesName)
        #print(sizes_origName)
        print(rating)
        print(feedBack)
        print(description)
        print(imgs)
        print()
        print()
        print('------------card-------------')


        pass
    except Exception as err:
        raise err
        #print(f'Ошибка, id:{id} не получилось обработать: {err}')



"""
url = f'https://www.wildberries.ru/__internal/u-card/cards/v4/detail?appType=1&curr=rub&dest={dest}&spp=30&hide_vflags=4294967296&hide_dtype=9&ab_testing=false&lang=ru&nm={nm}'
        resDetail = requests.get(
            url,
            headers=headers,
        ).json()

        print(resDetail)
        """
def start_search():
    startTime = time.time()
    count = 0
    maxCount = 0
    while count <= maxCount:
        try:
            page = count // 100 + 1
            response = requests.get(
                URL_SEARCH,
                params=get_params(query=query,page=page),
                headers=headers,
            ).json()
            #Получаем максимальное кол-во карточек
            if maxCount == 0:
                maxCount = int(response['total'])
                print(f"Карточек по запросу «{query}»: {maxCount}")
            nm = ''
            nms=[]
            for res in response['products']:
                nms.append(str(res['id']))
            nm = ';'.join(nms)
            print('SEARCH')
            print(response['products'][0]['id'])
            print('--SEARCH---')

            ###Получаем detail по 100 id(артикулам) карточек

            resDetail = requests.get(
                url=f'https://www.wildberries.ru/__internal/u-card/cards/v4/detail?appType=1&curr=rub&dest={dest}&spp=30&hide_vflags=4294967296&hide_dtype=9&ab_testing=false&lang=ru&nm={response['products'][0]['id']}',
                headers=headers,
            ).json()
            print('DETAIL')

            for detail in resDetail['products']:
                parse_card(detail)

            print(resDetail)
            print('---DETAIL---')
            print(f"Запрос {page} из {maxCount // 100 + 1}: Карточек: {len(nms)}")

            ###

            #parse_card(nm)
        except Exception as err:
            raise
            if count == 0:
                print('Ошибка выполнения первого запроса: ', err)
                break
            print(f'Ошибка выполнения поискового запроса №{count//100+1} : ', err)
        count = count+100
    print(f'Время сбора карточек из поиска: {(time.time()-startTime):.4f} секунд')
#parse_card(str(response['products'][0]['id']))

start_search()
#parse_card('489377490')


#start_search()