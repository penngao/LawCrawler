# -*-coding:utf-8-*-

import sys
sys.path.append('../')
from easy_parallelize import *
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from config import *
from datautil import *
import os


class StringToUrl():

    def __init__(self, string='', search_type=1):
        self.keyword = parse.quote(string)
        self.type = search_type

    def url2url(self, url):
        hrefs = []

        try:
            opener = request.Request(url, headers={'user-agent': ua.random})
            response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                result = filter(None, soup.find_all('dd', class_='links'))
                result = list(result)
                for href in result:
                    href_str = href.get_text()
                    if href_str and href_str.startswith('http://www.chinacourt.org/law/detail/'):
                        hrefs.append(href_str)

        except Exception as e:
            print('Someting wrong happened in url2url')
            print(e)

        return hrefs

    def base2result(self):

        first_url = chinacourt_first_url + self.keyword + chinacourt_second_url + \
                    '1' + chinacourt_third_url
        result = []
        urls = []
        pagecount = 1

        try:
            opener = request.Request(first_url, headers={'user-agent': ua.random})
            reponse = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if reponse:
                soup = BeautifulSoup(reponse, cr_parser)
                temp_result = filter(None, soup.find_all('a'))
                for curr in temp_result:
                    curr_str = curr.get_text().strip()
                    if curr_str and curr_str == '尾页':
                        pagecount = int(curr.get('href').split('/')[-1].split('.')[0])
                        break

                for page in range(pagecount):
                    urls.append(chinacourt_first_url + self.keyword +
                                chinacourt_second_url + str(page + 1) +
                                chinacourt_third_url)

                result.extend(easy_parallelize(self.url2url, urls, pool_size=4))

            return result

        except Exception as e:
            print('Something wrong happened in base2result')
            print(e)


def href2txt(link):
    content_id = link.split('/')[-1].split('.')[0]
    if not check_db('content_id_' + content_id, chinacourt_shelve_dir):
        total_text = ''
        try:
            opener = request.Request(link, headers={'user-agent': ua.random})
            reponse = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if reponse:
                soup = BeautifulSoup(reponse, cr_parser)
                result = soup.find('div', class_='law_content')
                law_content = soup.find('div', class_='content_text') if result is None else result
                law_content_text = law_content.get_text().strip()

                for sentence in law_content_text.split('\n'):
                    sentence = sentence.strip()
                    if sentence != '':
                        total_text += sentence + '\n'

                filename = chinacourt_save_dir + content_id + '.txt'
                file = open(filename, 'a+', encoding='utf-8')
                file.write(total_text)
                file.close()
                print('content_id = ' + content_id + ' has been crawled.')

        except Exception as e:
            print('Something wrong happened in href2txt method! current content id = '
                  + content_id)
            print(link)
            print(e)


def chinacourtcrawler(keyword):
    """
    main data source
    :param keyword: search keyword like '道路' or '交通'
    :return:
    """
    test = StringToUrl(string=keyword)
    urls = test.base2result()

    for url in urls:
        crawl_ThreadSubmit(href2txt, url, workers=1)


if __name__ == '__main__':

    # keyword_1 = '道路'
    keyword_2 = '交通'
    # shelve_setup(chinacourt_shelve_dir)
    # chinacourtcrawler(keyword_1)
    chinacourtcrawler(keyword_2)

    if os.path.exists(chinacourt_save_dir):
        files = os.listdir(chinacourt_save_dir)
        print('Total counts of laws in chinacourt file is ' + str(len(files)))
