from bs4 import BeautifulSoupfrom lxml import htmlimport xmlimport requestsimport csvimport timeheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 'Host': 'movie.douban.com'}link_lists = [] # url 队列class Spyder():    def __init__(self):        self.header = headers    def get_url(self):        queue_url = []        for i in range(0, 10):            link = 'https://movie.douban.com/top250?start=' + str(i * 25)            r = requests.get(link, headers=self.header, timeout=100)            soup = BeautifulSoup(r.text, 'lxml')  # 使用bs清洗数据 得到soup类            url_list = soup.find_all('div', class_='info')            for each in url_list:                movie_url = each.a['href']                queue_url.append(movie_url)        if len(queue_url) == 250:            # 将得到的url读取到txt文本内            with open('url.txt', 'w', encoding='utf-8', newline='') as file:                while len(queue_url):                    file.writelines(queue_url.pop(0))                    file.write('\n')    def read_url(self):        with open('url.txt', 'r') as file:            for i in range(0, 150):                temp_link = file.readline()                link_lists.append(temp_link)    def get_movie_message(self): # 从子页面爬取到的信息        movie_message_list = []        for i in range(0, 1):            link = link_lists[i][:-1]            while True:  # 一直循环，知道访问站点成功                try:                    # 以下except都是用来捕获当requests请求出现异常时，                    # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行                    r = requests.get(link, headers=self.header, timeout=5)                    break                except requests.exceptions.ConnectionError:                    print('ConnectionError -- please wait 3 seconds')                    time.sleep(3)                except requests.exceptions.ChunkedEncodingError:                    print('ChunkedEncodingError -- please wait 3 seconds')                    time.sleep(3)                except:                    print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')                    time.sleep(3)            soup = BeautifulSoup(r.text, 'lxml')  # 使用bs清洗数据 得到soup类            div_list = soup.find_all(type="application/ld+json")            print(div_list)    def get_movies(self):        movie_message_list = []        for i in range(0, 10):            link = 'https://movie.douban.com/top250?start=' + str(i * 25)            while True:                try:                    r = requests.get(link, headers=self.header, timeout=5)                    break                except requests.exceptions.ConnectionError:                    print('ConnectionError -- please wait 3 seconds')                    time.sleep(3)                except requests.exceptions.ChunkedEncodingError:                    print('ChunkedEncodingError -- please wait 3 seconds')                    time.sleep(3)                except:                    print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')                    time.sleep(3)            soup = BeautifulSoup(r.text, 'lxml')  # 使用bs清洗数据 得到soup类            div_list = soup.find_all('div', class_='info')  # 提取电影名            for each in div_list:                movie_message = []                movie_name = each.span.text                movie_message.append(movie_name)  # 添加电影名                pre_data = each.p.text.strip().split(' ')                movie_message.append(pre_data[1])  # 添加导演序列                i = len(pre_data) - 1  # 添加年份和概述                while True:                    if pre_data[i] != '':                        i -= 1                    else:                        break                for j in range(i, len(pre_data) - 1):                    movie_message.append(pre_data[j])                if each.find('span', class_='inq'):                    movie_motto = each.find('span', class_='inq').text                movie_message.append(movie_motto)  # 添加一句话电影                # 进行最后处理                movie_message.remove('') # 删除空格                movie_message_copy = []# 处理掉乱码字符                for each in movie_message:                    movie_message_copy.append(''.join(each.split()))                movie_message_list.append(movie_message_copy)        return movie_message_list    def write_to_csv_file(self, filename, rows):        with open(filename, 'w', encoding='utf-8', newline='') as file:            writer = csv.writer(file)            writer.writerows(rows)if __name__ == '__main__':    spyder = Spyder()    #spyder.get_url()    #spyder.read_url()    #spyder.get_movie_message()    movie_message_list = spyder.get_movies()    print(movie_message_list)    print(len(movie_message_list))    # # 写入txt    filename = 'data.csv'    spyder.write_to_csv_file(filename, movie_message_list)