import requests
import json
import ConfigParser
import sys
from bs4 import BeautifulSoup
from aes import enc_data
from datetime import datetime

#init setting
section = 'default'
config = ConfigParser.ConfigParser()
config.read('data/conf.ini')
print("Start Initialization.")

#auth setting
if len(sys.argv) == 3:
    user_id = sys.argv[1]
    user_pin = sys.argv[2]
elif len(sys.argv) == 1:
    user_id = str(config.get(section,'user_id'))
    user_pin = str(config.get(section,'user_pin'))
else:
    #wrong param
    print("Wrong Param!!")
    exit()

contents_num_init= int(config.get(section,'contents_num_init'))
init_date = datetime(int(config.get(section,'init_date_year')),\
    int(config.get(section,'init_date_month')),\
    int(config.get(section,'init_date_day')))
limit_page = int(config.get(section,'limit_page'))

print("User ID  : "+user_id)
print("User PIN : "+user_pin)
print("==================================================")
print("Start Processing")

#URL setting
with open('data/url.json') as data_file:    
    data = json.load(data_file)

URL_home = str(data['URL_home'])
URL_login = str(data['URL_login'])
URL_login_proc = str(data['URL_login_proc'])
URL_pages = str(data['URL_pages'])
URL_like = str(data['URL_like'])
URL_share = str(data['URL_share'])
request_headers = data['request_headers']

#login page for finding encoding key
response = requests.get(URL_login)
plain_text = response.text
soup = BeautifulSoup(plain_text, 'lxml')
sub_soup = [s for s in soup.findAll('script') if "function enc_data(secret)" in str(s)]
keys = str(sub_soup[0]).split('\n')

login_data = {'member_no':enc_data(user_id,keys[3].split('"')[1],keys[4].split('"')[1]),\
             'epin':enc_data(user_pin,keys[3].split('"')[1],keys[4].split('"')[1])}
request_headers['cookie'] = 'PHPSESSID=' + response.cookies['PHPSESSID']

print("Login Cookie : " + str(request_headers['cookie']))

#login proc request
request_headers['referer'] = URL_login
response = requests.request("POST", URL_login_proc, data=login_data, headers=request_headers)
if response.json().get('flag') == 'ok':
    print("Login Processing complete...")

    #crowling pages set
    pages_num = (datetime.now()-init_date).days*4+contents_num_init
    pages = (pages_num, pages_num+1)

    #web crowling
    like_cnt = 0
    share_cnt = 0
    page_idx = (datetime.now()-init_date).days*4+contents_num_init

    for i in range(100):
        #loop condition check
        request_headers['referer'] = URL_home
        response = requests.request("GET", URL_home, headers=request_headers)
        plain_text = response.text
        soup = BeautifulSoup(plain_text, 'lxml')

        like_cnt = int(soup.find(id='like-count').string)
        share_cnt = int(soup.find(id='share-count').string)
        info_point = str(soup.find(id='info_point').string)

        if (like_cnt >= limit_page and share_cnt >= limit_page) :
            break
        else :
            print("URL : "+request_headers['referer'])

            request_headers['referer'] = URL_pages + str(page_idx)
            like_data = {'idx':str(page_idx)}
            requests.request("POST", URL_like, data=like_data, headers=request_headers)
            #response = requests.request("POST", URL_like, data=like_data, headers=request_headers)
            #print(request_headers)
            #print(response.text)

            share_data = {'idx':str(page_idx), 'sns':'twitter'}
            requests.request("POST", URL_share, data=share_data, headers=request_headers)
            #response = requests.request("POST", URL_share, data=share_data, headers=request_headers)
            #print(request_headers)
            #print(response.text)


            page_idx += 1

    print("==================== Complete ====================")
    print("Today Like count : "+str(like_cnt))
    print("Today Share count : "+str(share_cnt))
    print("Point : "+info_point)
    print("==================================================")
else:
    print("Login Fail!")
