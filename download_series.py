import os
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from concurrent.futures import ThreadPoolExecutor,wait
import time
        
def one_book_url(url):#获取根目录所有本子信息
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.106'}
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'lxml')

    website = []
    the_begin = 'https://zh.nyahentai.site'                                   ##修改此处
    content = soup.find_all('div',class_ = 'gallery') ##大的div
    for i in content:
        nexturl = i.find('a')
        one_url = nexturl.get('href')
        all_url = the_begin + one_url
        website.append(all_url)
    return website

def geturl_pic(url,download_path):#获取单个本子所有链接并创建文件夹
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.106'}
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'lxml')

    book_title = soup.find('h1').get_text()
    download_path2 = download_path+"/"+book_title
    if not os.path.exists(download_path2):
        os.makedirs(download_path2)
    
    website = []
    the_begin = 'https://zh.nyahentai.site'
    content = soup.find_all('div',class_ = 'thumb-container') ##大的div
    for i in content:
        nexturl = i.find('a')
        one_url = nexturl.get('href')
        all_url = the_begin + one_url
        website.append(all_url)
    return website,download_path2

def download_pic(url,download_path2):#下载图片
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.106'}
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'lxml')

    link = soup.find(class_ = "fit-horizontal full-height").find('img').get('src')
    name = soup.find(class_ = "current").get_text()
    html = requests.get(link)
    with open(f'{download_path2}/{name}.jpg','wb') as f:
        f.write(html.content)
    print(f'{download_path2}图片{name}下载完成')



def main():
    authors = ['hal']               #输入作者名---------------------------------------------------
    page_num = [2]                  #输入作者中文界面页数-----------------------------------------

    first_urls = 'https://zh.nyahentai.site/artist/'                           ##修改此处源地址
    end_urls = '/chinese'
    for author,page in zip(authors,page_num):
        website2 = []
        root_url = first_urls + author +end_urls
        start_urls = [root_url]
        for i in range(2,page+1):
            start_urls.append(f'{root_url}/page/{i}')                         #设置该作者的所有网页

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.106'}
        r = requests.get(root_url,headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'lxml')#基础设置

        author_name_from = soup.find('div',id='content')
        author_name = author_name_from.find('span',class_=None).get_text()          #获取作者名且创建文件夹
        download_path = "./"+author_name
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        for url in start_urls:
            website = one_book_url(url)
            for url in website:
                website2.append(url)
            print(f"{author_name}'s page was completed!")                           #获取根目录本子链接至website2
        print("目前已下载几本?")
        x = int(input())
        if x == 0:
            website2 = website2
        else:
            for i in range(1,x+1):
                del website2[0]
            print(website2)


        for url in website2:
            website3,download_path2 = geturl_pic(url,download_path)
            print('文件夹已更新，休息3s')
            time.sleep(3)
            print('休息结束')
        
            with ThreadPoolExecutor(max_workers=20) as executor:                    #开启多线程
                for url in website3:
                    executor.submit(download_pic,url,download_path2)
                 

if __name__ == '__main__':
    main()
