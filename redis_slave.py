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
        r = Redis(host='10.10.70.83', port=6379)
        print(r.keys('*'))
        r.delete('url')
        with open('url.txt', 'r') as file:
            for i in range(0, 150):
                temp_link = file.readline()
                r.lpush('url', temp_link)
            print('待爬取链接个数', r.llen('url'))

if __name__ == '__main__':
    this_machine = 'slave'
    if this_machine == 'master':

        redis_handle = Redis_server()
        redis_handle.get_html()
    if this_machine == 'slave':
        redis_handle = Redis_server()
        redis_handle.get_url_list()
        #redis_handle.get_html()

