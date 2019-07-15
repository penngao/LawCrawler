# -*-coding:utf-8-*-

import sys
sys.path.append('../')
from easy_parallelize import *
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from config import *
from datautil import shelve_setup, check_db
import os
import re


class StringToUrl():

    def __init__(self, string=''):
        self.keyword = parse.quote(string)

    def url2url(self, url):
        hrefs = []

        try:
            opener = request.Request(url, headers={'user-agent': ua.random})
            response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                result = filter(None, soup.find_all('a'))
                result = list(result)
                for line in result:
                    href = line.get('href')
                    if href and href.startswith(globallaw_startswith):
                        hrefs.append(href)
        except Exception as e:
            print('Something wrong happened in url2url')
            print(url)
            print(e)

        return hrefs

    def url2more(self, url):
        more_hrefs = []

        try:
            opener = request.Request(url, headers={'user-agent': ua.random})
            response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                result = filter(None, soup.find_all('a', class_='more posa'))
                result = list(result)
                pattern = r'\(\S+(\,|\，)\S+(\,|\，)\S+\)'
                maxpage = 1
                for line in result:
                    href = line.get('href')
                    search_result = re.search(pattern, href).group()
                    result_split = search_result.split('\'')
                    sortId = result_split[1]
                    sortName = result_split[3]
                    fg = result_split[5]

                    # crawl the page information
                    if search_result:
                        temp_url = globallaw_claw_base_url \
                                   + 'keyword=' + self.keyword \
                                   + '&sortId=' + sortId \
                                   + '&sortName=' + parse.quote(sortName) \
                                   + '&fg=' + fg
                        page_opener = request.Request(temp_url, headers={'user-agent': ua.random})
                        page_response = request.urlopen(page_opener, timeout=FETCHTIME_OUT)
                        if page_response:
                            page_soup = BeautifulSoup(page_response, cr_parser)
                            page_all_urls = page_soup.find_all('a', class_='next')

                            for url in page_all_urls:
                                if url.get_text() == '尾页':
                                    page_href = url.get('href')
                            page_pattern = r'\(\'\w\'\)'
                            page_result = re.search(page_pattern, page_href).group()
                            maxpage = int(page_result.split('\'')[1]) if page_result is not None else 1

                            for page in range(maxpage):
                                curr_url = globallaw_claw_base_url \
                                           + 'pageNum=' + str(page + 1) \
                                           + '&maxNum=' + str(maxpage) \
                                           + '&keyword=' + self.keyword \
                                           + '&sortId=' + sortId \
                                           + '&sortName=' + parse.quote(sortName) \
                                           + '&fg=' + fg
                                more_hrefs.append(curr_url)

        except Exception as e:
            print('Something happenes wrong in url2more')
            print(url)
            print(e)

        return more_hrefs

    def base2result(self):
        hrefs = []

        for first_url in globallaw_first_url:
            complete_url = first_url + self.keyword

            hrefs.append(self.url2url(complete_url))
            more_result = self.url2more(complete_url)
            if more_result is not None:
                hrefs.extend(self.url2url(url) for url in more_result)

        return hrefs


def href2txt(link):
    content_id = link.split('=')[-1]
    if not check_db('content_' + content_id, globallaw_shelve_dir):
        total_text = ''
        try:
            link = globallaw_search_url + link
            opener = request.Request(link, headers={'user-agent': ua.random})
            response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                xml = soup.find('div', class_='article')
                if xml is None:
                    print('content_id = ' + content_id + ' is none')
                    return
                content_text = xml.get_text().strip()

                for sentence in content_text.split('\n'):
                    sentence = sentence.strip()
                    if sentence != '':
                        sentence = sentence.split(' ')
                        sentence = ''.join(sentence)
                        total_text += sentence + '\n'

                filename = globallaw_save_dir + content_id + '.txt'
                file = open(filename, 'a+', encoding='utf-8')
                file.write(total_text)
                file.close()
                print('content_id = ' + content_id + ' has been crawled.')
        except Exception as e:
            print('Something wrong happened in href2txt method!')
            print(link)
            print(e)


def globallawcrawler(keyword):
    """
    crawl data from http://policy.mofcom.gov.cn/law/index.shtml
    :param keyword: search keyword like '道路' or '交通'
    :return:
    """
    test = StringToUrl(string=keyword)
    urls = test.base2result()

    for url in urls:
        crawl_ThreadSubmit(href2txt, url, workers=1)


if __name__ == '__main__':
    keyword_1 = '道路'
    keyword_2 = '交通'
    shelve_setup(globallaw_shelve_dir)
    globallawcrawler(keyword_1)
    globallawcrawler(keyword_2)

    if os.path.exists(globallaw_save_dir):
        files = os.listdir(globallaw_save_dir)
        print('Total counts of laws in globallaw file is ' + str(len(files)))
