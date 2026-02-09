import time
from get_cookie import listProxyCookie
import json
import asyncio
import random
from playwright.async_api import async_playwright
from utils import URL_SEARCH, get_params, getHeaders, DEST, getUrlCard, getUrlImg
import aiohttp
from aiohttp_proxy import ProxyConnector, ProxyType
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





async def getCard(
        proxy:str,
        task:str,
        cookie:str,
        queue:asyncio.Queue,
        lock:asyncio.Lock,
        result:list,
        card,
        job,
):
    print(f'Create task {task} {proxy}')
    allCards = []
    username = proxy.split('@')[0].split(':')[0]
    password = proxy.split('@')[0].split(':')[1]
    host = proxy.split('@')[1].split(':')[0]
    port = int( proxy.split('@')[1].split(':')[1] )

    connector = ProxyConnector(
         proxy_type=ProxyType.HTTPS,
         host=host,
         port=port,
         username=username,
         password=password,
         rdns=True
     )
    try:
        detail:dict
        async with aiohttp.ClientSession(connector=connector) as session:
            while True:
                detail = await queue.get()
                #print(f'get detaul len {len(detail)}')
                await  asyncio.sleep(0.5)
                if detail == None:
                    break
                ids =str(  detail['id'] )

                print(f'Карточка {ids}')
                try:
                    url = getUrlCard(ids)
                    async with session.get(url=url,
                                            headers=getHeaders(cookie=cookie)
                    ) as res:

                        if res.status == 404:
                            print(f'404: {url}')
                            #нет такой страницы
                            ###Сделать ввывод ошибок
                            continue

                        responseText = await res.text()
                        responseCard = json.loads(responseText)


                        info = DataClass()
                        info.description =  responseCard['description']
                        info.imgs = getUrlImg(id = str(ids), count = int(responseCard['media']['photo_count']))
                        info.urlCard = f'https://www.wildberries.ru/catalog/{ids}/detail.aspx'
                        info.article = ids
                        info.name = responseCard['imt_name']
                        info.price = 'None'
                        info.supplierName = detail['supplier']
                        info.url_supplier = f'https://www.wildberries.ru/seller/{detail['supplierId']}'

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
                        sizesName = ','.join(sizes)
                       # info.qtySize = ''
                        info.qty = str(qty)
                        info.sizesName = sizesName
                        info.rating = str(detail['reviewRating'])
                        info.feedBack = str(detail['feedbacks'])

                        opts = []
                        for opt in responseCard['options']:
                            opts.append(f'{opt['name']} : {opt['value']} ')

                        info.opts = opts
                        allCards.append(info)


                    pass
                except Exception as err:
                    print(f'Ошибка')

            """
            async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            return await response.text()
            """

        #return result
    except:
        raise
    return {"card" : [allCards]}
    #return allCards


async def main(queue: asyncio.Queue, query:str):
    job = True
    if len(listProxyCookie) < 0:
        print('Нет доступных прокси. Для работы загрузите прокси ')
    else:
        print(f'К работе готово {len(listProxyCookie)} проксей')

    tasks_list = []
    card = []

    lock = asyncio.Lock()
    result = []
    for p, task in enumerate(listProxyCookie):
        task_obj = asyncio.create_task(getCard(
            proxy=task['proxy'],
            cookie=task['cookie'],
            task = str(p),
            queue=queue,
            lock=lock,
            result = result,
            card = card,
            job=job,
        ))
        tasks_list.append(task_obj)
    print('НАЧИНАМ СБОР ПО ПОИСКУ ')

    async with aiohttp.ClientSession() as session:
        startTime = time.time()
        count = 0
        maxCount = 0
        while count <= maxCount:
            try:
                page = count // 100 + 1
                try:
                    nm = ''
                    #запрос на поик 100 карточек
                    async with session.get(url=URL_SEARCH,
                                            params=get_params(query=query, page=page),
                                            ### костыль, нужно переписать нормально чтобы получать cookie для парса )
                                            headers=getHeaders(cookie=listProxyCookie[0]['cookie'])
                    ) as res:
                        responseText = await res.text()
                        response = json.loads(responseText)


                        if maxCount == 0:
                            maxCount = int(response['total'])
                            print(f"Карточек по запросу «{query}»: {maxCount}")
                        nm = ''
                        nms = []
                        for res in response['products']:
                            nms.append(str(res['id']))
                        nm = ';'.join(nms)
                        print('DETAIL')


                    async with session.get(
                        url= f'https://www.wildberries.ru/__internal/u-card/cards/v4/detail?appType=1&curr=rub&dest={DEST}&spp=30&hide_vflags=4294967296&hide_dtype=9&ab_testing=false&lang=ru&nm={nm}',
                            ### костыль, нужно переписать нормально чтобы получать cookie для парса )
                        headers=getHeaders(listProxyCookie[0]['cookie'])
                    ) as res:

                        responseText = await res.text()
                        response = json.loads(responseText)
                        #print(response)

                        for q in response['products']:
                            await queue.put(q)
                        #print(response)
                        print('--DETAIL---')

                    ###!!!Внимание break

                    #if count>300:
                    #    break
                    break
                except Exception as err:
                    print('ошибка выполнения запроса')
                    if count == 0:
                        print('Ошибка получения поиска: ', err)
                        break

            except Exception as err:
                print(f'ошибка цикла {err}')


            count = count + 100
                # Получаем максимальное кол-во карточек



    job = False
    for i in range(0, len(listProxyCookie)+1):
        await queue.put(None)
    print('job = False')
    results = await asyncio.gather(*tasks_list)

    pass

    ###Save openXlsx



    ###---Save openXlsx





query = "пальто из натуральной шерсти"

queue = asyncio.Queue()
asyncio.run(main(queue=queue, query=query))