from bs4 import BeautifulSoup as BS
import telebot
import time as TIME
import requests
import pickle
import random
import cfscrape
with open('log.txt','rb') as inp:
    log = pickle.load(inp)
def TimeNow(base_url,headers,LOG=None,ParsProxyDate=None):
    session = requests.Session()
    request = session.get(base_url, headers=headers,verify=False)
    if request.status_code == 200:
        soup = BS(request.content, 'html.parser')
        tables = soup.find('table')
        rows = tables.find_all('tr')[1:]
        TIMENOW = []
        for row in rows:
            TIMENOW.append(row.find_all('td'))
        TIMENOWM = (TIMENOW[0][1].text)
        DATE=TIMENOWM.split('T')[0]
        TIMENOWM = TIMENOWM.split('T')[1]

        if LOG!=None:
            time_log=('UTC: '+TIMENOWM[0:10]+' '+TIMENOWM[11:19]+' Date: '+str(DATE))
            return time_log
        elif ParsProxyDate!=None:
            return DATE
        else:
            time_sec=(int(TIMENOWM[0:2])+3)*3600+int(TIMENOWM[3:5])*60+int(TIMENOWM[6:8])
            return time_sec
headers={'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
base_url='https://www.utctime.net'
def proxy_day():
    DATE_NOW = TimeNow(base_url, headers, None, True)
    DATE_LAST_file = open("DATE_LAST.txt", "r")
    LAST_DATE = DATE_LAST_file.read()
    if int(LAST_DATE[0:4]) < int(DATE_NOW[0:4]) or int(LAST_DATE[5:7]) < int(DATE_NOW[5:7]) or int(
            LAST_DATE[8:10]) < int(DATE_NOW[8:10]):

        DATE_LAST_file.close()
        DATE_LAST_file = open("DATE_LAST.txt", "w")
        DATE_LAST_file.write(str(DATE_NOW))
        DATE_LAST_file.close()
        RESULT_PARS_PROXY = 100
        counter = 0
        while RESULT_PARS_PROXY != 200 and counter!=5:
            RESULT_PARS_PROXY = pars_proxy()
            counter += 1
        print("proxy_day after while")
    else:
        DATE_LAST_file.close()
from python3_anticaptcha import NoCaptchaTaskProxyless
def capcha(base_url_proxy):
    # Введите ключ от сервиса AntiCaptcha, из своего аккаунта. Anticaptcha service key.
    ANTICAPTCHA_KEY = "ANTICAPTCHA_KEY"
    # G-ReCaptcha ключ сайта. Website google key.
    SITE_KEY = 'SITE_KEY'
    # Ссылка на страницу с капчёй. Page url.
    PAGE_URL = base_url_proxy
    # Возвращается строка-расшифровка капчи. Get string for solve captcha, and other info.
    # session = requests.Session()
    user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(websiteURL=PAGE_URL, websiteKey=SITE_KEY)
    # print(user_answer)
    return user_answer
def pars_proxy():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import TimeoutException
    base_url_proxy = 'https://awmproxy.com/freeproxy.php'
    result_capcha = False
    i=0
    while result_capcha != True:
        i += 1
        user_answer = capcha(base_url_proxy)
        if user_answer['errorId'] != 0:
            # print('Wait...')
            TIME.sleep(60)
        else:
            # https://awmproxy.com/freeproxy.php?g-recaptcha-response=&op=getlink
            url = base_url_proxy + '?g-recaptcha-response={}&op=getlink'.format(user_answer['solution']['gRecaptchaResponse'])
            TIME.sleep(5)
            try:
                driver = webdriver.Chrome(executable_path=r'C:\Users\user\PycharmProjects\PROX_bot\chromedriver.exe') # chromedriver.exe должен находиться в той же папке, что и этот скрипт!
                act = ActionChains(driver)
                wait = WebDriverWait(driver, 500)
                driver.get(url)  # Перейти по ссылк
                wait.until(EC.element_to_be_clickable((By.ID, "wait-div")))
                # driver.find_element_by_xpath('/html/body/div/div[4]/div/div[2]/div[2]/table')  # проверка прохождения капчи
                TIME.sleep(5)
                url2 = driver.find_element_by_xpath('//*[@id="info3-inp"]/input').get_attribute('value')
                # driver.find_element_by_xpath('//*[@id="wait-div-button"]/div/form/input').click() #нажатие кнопки с ссылкой
                driver.close()
                # print(url2)
                TIME.sleep(5)
                driver = webdriver.Chrome('chromedriver.exe')
                driver.get(url2)
                TIME.sleep(5)
                PROXY_LEAST = driver.find_element_by_xpath('/html/body/pre').text
                proxy_file=open('PROXY.txt','w')
                proxy_file.write(str(PROXY_LEAST))
                proxy_file.close()
                # f = f.split()
                '''''''''
                act = ActionChains(driver)
                act.send_keys(Keys.CONTROL).send_keys("a").perform()
                time.sleep(5)
                act.send_keys(Keys.CONTROL).send_keys("c").perform()
                time.sleep(5)
                driver.close()  # закрываем браузер
                c = pyperclip.paste()
                c = c.split()
                print(len(c), c)
                '''
                driver.close()
                result_capcha = True
            except NoSuchElementException:
                print("NoSuchElementException")
                driver.close()
                result_capcha = False
            except TimeoutException:
                print("TimeoutException")
                driver.close()
                result_capcha = False
            except Exception as err:
                print(err)
                driver.close()
                result_capcha = False
    RES_PARS_PROXY=200
    return RES_PARS_PROXY

proxy_day()
token="my_token"
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['10proxy'])
def handle_start(message):
    PROXY_TEN=''
    PROXY_file=open('PROXY.txt','r')
    prox = PROXY_file.read()
    prox = prox.split()
    log.append([["10proxy"], [str(message.from_user)], [str(message.chat)], [str(TimeNow(base_url, headers, LOG=True))]])
    with open('log.txt', 'wb') as out:
        pickle.dump(log, out)
    if len(prox)>10:
        for i in range(10):
            r = random.randint(0, len(prox) - 1)
            PROXY_TEN+=(str(prox[r])+'\n')
            del prox[r]
        bot.send_message(message.chat.id, PROXY_TEN)
    elif len(prox)<10:
        bot.send_message(message.chat.id,'Какие-то проблемы с моими прокси\nнапиши позже')
    PROXY_file.close()
    proxy_day()

bot.polling(none_stop=True)