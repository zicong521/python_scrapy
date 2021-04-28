from redis import Redis
from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import csv
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 'Host': 'movie.douban.com'}


class Redis_server():
    def get_url_list(self):
        r = Redis(host='10.11.1.42', port=6379)
        print(r.keys('*'))
        r.delete('url')
        with open('url.txt', 'r') as file:
            for i in range(0, 150):
                temp_link = file.readline()
                r.lpush('url', temp_link)
            print('待爬取链接个数', r.llen('url'))


    def get_html(self):
        re = Redis(host='10.11.1.42', port=6379)

        while True:  # 一直循环，直到访问站点成功
            try:
                link = re.lpop('url')
                link = link.decode('ascii')
                link = link[:-1]
                print(link)
                # 以下except都是用来捕获当requests请求出现异常时，
                # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
                r = requests.get(link, headers=headers, timeout=5)
                soup = BeautifulSoup(r.text, 'lxml')  # 使用bs清洗数据 得到soup类
                div_list = soup.find_all(type="application/ld+json")
                print(div_list)
                print('爬取第 %d 个链接'  % re.llen('url'))

            except requests.exceptions.ConnectionError:
                print('ConnectionError -- please wait 3 seconds')
                time.sleep(3)
            except requests.exceptions.ChunkedEncodingError:
                print('ChunkedEncodingError -- please wait 3 seconds')
                time.sleep(3)
            except:
                print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(3)

if __name__ == '__main__':
    this_machine = 'master'
    if this_machine == 'master':
        redis_handle = Redis_server()
        #redis_handle.get_url_list()
        redis_handle.get_html()
    if this_machine == 'slave':
        redis_handle = Redis_server()
        redis_handle.get_html()
