import sqlite3
import requests
from playwright.sync_api import sync_playwright, expect
from pytest_playwright.pytest_playwright import playwright
from utils import URL_SEARCH, getHeaders, get_params
conn = sqlite3.connect('db.db')
cursor = conn.cursor()
MAX_RETRY = 3
MAX_TIMEOUT = 5


with open('proxy.txt', 'r', encoding='utf-8') as file:
    lines = [line.rstrip('\n') for line in file.readlines()]

# Времено 1 прокси

#

getListCookie = []
# лист Валидных проксей и cookie
listProxyCookie = []
checkProxyCookie = []

def getNewCookie(proxy:str, check:bool):
    try:
        if check:
            username = proxy.split('@')[0].split(':')[0]
            password = proxy.split('@')[0].split(':')[1]
            host = proxy.split('@')[1].split(':')[0]
            port = int(proxy.split('@')[1].split(':')[1])
            proxyP = {"server": f"http://{host}:{str(port)}", "username": username, "password": password}
        else:
            proxyP = None
        with sync_playwright() as p:
            browser =  p.chromium.launch(
                headless=False,
                args=["--start-maximized",
                      '--disable-blink-features=AutomationControlled'],
                proxy=proxyP
            )
            context =  browser.new_context(
                storage_state=None,  # Без сохранённых cookies/storage
                locale="ru-RU",
                timezone_id="Europe/Moscow",
                permissions=[],
            )
            page =  context.new_page()
            #page.goto('https://www.2ip.ru/')
            page.goto('https://www.wildberries.ru/')
            loc = page.locator('a[href*="security/login"]')
            try:
                expect(loc).to_be_visible(visible=True,timeout=15000)
            except:
                print('exept loc')
                return
            print(context.cookies())

            mcookie = []
            for cok in context.cookies():
                mcookie.append(cok['name']+'='+cok['value'])

            cookieNew = ';'.join(mcookie)
            #получили новые куки
            if len(mcookie)>=1:
                try:
                    #proxyStr =
                    query = """
                               INSERT INTO cookies (proxy, cookie)
                               VALUES (?, ?)
                               ON CONFLICT(proxy)
                               DO UPDATE SET
                               cookie = excluded.cookie;
                               """
                    cursor.execute(query, (proxy, cookieNew))
                    conn.commit()
                except Exception as err:
                    print(f'Ошибка получения cookie для Proxy {proxy} : {err}')


    except Exception as err:

        print(f'Не получилось загрузить playwright через Proxy {proxy} : {err}')
    pass


"""
for i in range(0,1):
    getNewCookie('tmV4MbacaL:FGgpfV4ur9@5.8.16.245:31762')
exit(0)
"""


for i, proxy in enumerate(lines):
    try:
        cursor.execute('SELECT cookie FROM cookies WHERE proxy = ?', (proxy,))
        result = cursor.fetchone()
        if result== None:
            #нет записи cookie в бд. Нужно получить
            getListCookie.append(proxy)
        else:
            #есть записть cookie в бд, нужно проверить валидность cookie
            checkProxyCookie.append({'proxy':proxy, 'cookie':result[0]})
    except Exception as err:
        print(f'Ошибка базы данных Proxy: {proxy}')



for i, cookie in enumerate(checkProxyCookie):
    try:
        proxy = cookie['proxy']
        cookie = cookie['cookie']
        proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}', }


        for i in range(0,MAX_RETRY):
            try:
               # cookieTTT='x_wbaas_token=1.1000.7b88182a45834cda9c19d83a11475855.MHwxNzYuMTUuMTY0LjI1fE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDQuMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzcxNTkxODg1fHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3MDk4NzA4NXwx.MEUCIAfklxTyrKkvNX6hoUuTR76ETN+XljS1AVVOCxNrmQ0oAiEAit/4Nq2BDq58hjH4uGPjb1SQN5fWp/j4fErNB2n7eEY=; _wbauid=9255161901770382035; routeb=1770404947.732.60.384847|28979c6168ec4738f0fcb8539a6d5f12'
                response = requests.get(
                    timeout=MAX_TIMEOUT,
                        url = URL_SEARCH,
                       # 'http://icanhazip.com',
                        params=get_params(query="пальто из натуральной шерсти",page=0),
                        headers=getHeaders(cookie),
                        proxies=proxies
                    ).json()

                #Успешно загрузили cookie)
                print(f'--->Рабочий прокси и cookie {proxy} ')
                listProxyCookie.append({'cookie': cookie, 'proxy': proxy})
                break
            except Exception as err:
                print(f'Ошибка запроса на проверку cookie. Proxy: {proxy}')

    except Exception as err:

        print(f'Ошибка получения запроса прокси {proxy}', err)

def startProxy():
    #Если у нас ещё небыло записи cookie для Proxy или же cookie устарели
    for i, proxy in enumerate(getListCookie):
        getNewCookie(proxy, True)


