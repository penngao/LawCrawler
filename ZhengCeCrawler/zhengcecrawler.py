# -*-coding:utf-8-*-

import sys
sys.path.append('../')
from easy_parallelize import *
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from config import *
from datautil import *
import re
import os


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
                results = filter(None, soup.find_all('a'))
                # results = list(results)
                for href in results:
                    href_str = href.get('href')
                    if href_str and href_str.startswith(zhengce_stratswith):
                        hrefs.append(href_str)

        except Exception as e:
            print('Someting wrong happened in url2url')
            print(e)

        return hrefs

    def base2result(self):

        result = []
        urls = []

        try:
            for page in range(zhengce_max_page):
                urls.append(zhengce_first_url + self.keyword
                            + zhengce_second_url + str(page)
                            + zhengce_third_url)

            result.extend(easy_parallelize(self.url2url, urls, pool_size=1))

            return result

        except Exception as e:
            print('Someting wrong happened in base2result')
            print(e)


def href2txt(link):
    content_id = link.split('.')[-2].split('_')[-1]
    if not check_db('content_' + content_id, zhengce_shelve_dir):
        total_text = ''
        try:
            opener = request.Request(link, headers={'user-agent': ua.random})
            reponse = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if reponse:
                soup = BeautifulSoup(reponse, cr_parser)
                titleresult = soup.find('div', class_='pages-title')
                if titleresult is not None and titleresult.get_text().strip() != '':
                    total_text += titleresult.get_text().strip() + '\n'   # title of the news
                xml = soup.find_all(re.compile('^p'))
                if xml is None:
                    print('content_id = ' + content_id + ' is none')
                    return

                for sentence in xml:
                    sentence = sentence.get_text().strip()
                    if sentence != '' and len(sentence) > 10:
                        total_text += sentence + '\n'

                if len(total_text.split('\n')) < 4:
                    print('sentence of the content is too short and has to be removed!')
                    return
                # for sentence in total_text.split('\n'):
                #     if sentence is not None:
                #         sentences.append(sentence.strip() + '\n')

                filename = zhengce_save_dir + content_id + '.txt'
                file = open(filename, 'a+', encoding='utf-8')
                file.write(total_text)
                file.close()
                print('content_id = ' + content_id + ' has been crawled.')

        except Exception as e:
            print('Something happened in href2txt method! current content id = ' + content_id)
            print(e)


def zhengcecrawler(keyword):
    """
    the search domain limits in xinwen
    :param keyword: search keyword like '道路交通'
    :return:
    """
    test = StringToUrl(string=keyword)
    urls = test.base2result()

    for url in urls:
        crawl_ThreadSubmit(href2txt, url, workers=1)


if __name__ == '__main__':

    keyword = '道路交通'
    shelve_setup(zhengce_shelve_dir)
    zhengcecrawler(keyword)

    if os.path.exists(zhengce_save_dir):
        files = os.listdir(zhengce_save_dir)
        print('Total counts of laws in zhengce file is ' + str(len(files)))
