# -*-coding:utf-8-*-

import sys
sys.path.append('../')
from easy_parallelize import *
from urllib import request
from bs4 import BeautifulSoup
from config import findlaw_base_url, FETCHTIME_OUT, cr_parser, \
                   findlaw_save_dir, findlaw_shelve_dir, findlaw_search_urls, MAX_TIME, \
                   findlaw_jiaotongfaguiku_url
from datautil import shelve_setup, check_db, delete_db
import os
import urllib
from dynamic_proxy import *

test = GetProxy('../proxy.txt', proxy_pickle_dir)
test.update_available_ip(findlaw_base_url)


def url2url(url):
    hrefs = []
    count = 0

    while count < MAX_TIME:
        try:
            print('current parse href is ' + url)
            proxy = urllib.request.ProxyHandler(test.get_random_ip())
            opener = request.build_opener(proxy, request.HTTPHandler)
            opener.addheaders = [('User-Agent', ua.random)]
            request.install_opener(opener)
            response = request.urlopen(url, timeout=FETCHTIME_OUT)
            # opener = request.Request(url, headers={'User-Agent': ua.random})
            # response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                href_result = soup.find_all('a')
                if href_result is None:
                    # print('Current url ' + url + ' has no href!')
                    count += 1
                else:

                    for href in href_result:
                        href = href.get('href')
                        if href.startswith(findlaw_base_url) and href.endswith('.html'):
                            hrefs.append(href)
                    break
        except Exception as e:
            # print('Something wrong happened in url2url')
            # print(url)
            print(e)
            count += 1
    if count >= MAX_TIME:
        print('current url is unavailable ' + url)

    return list(set(hrefs))


def url2page(url):
    page_hrefs = []
    count = 0

    while count < MAX_TIME:
        try:
            proxy = urllib.request.ProxyHandler(test.get_random_ip())
            opener = request.build_opener(proxy, request.HTTPHandler)
            opener.addheaders = [('User-Agent', ua.random)]
            request.install_opener(opener)
            response = request.urlopen(url, timeout=FETCHTIME_OUT)
            # opener = request.Request(url, headers={'User-Agent': ua.random})
            # response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                href_result = soup.find_all('a', class_='pagination-item')
                if href_result is None:
                    # print('Something wrong happened in url2page')
                    # print(url)
                    count += 1
                else:

                    page_prefix = ''
                    page_number = 0
                    for href in href_result:
                        href_str = href.get_text()
                        if href_str == '尾页' and href.get('href') != '':
                            page_prefix = href.get('href').split('_')[0]
                            page_number = href.get('href').split('_')[1].split('.')[0]
                            page_number = int(page_number)
                            page_suffix = href.get('href').split('_')[1].split('.')[1]
                            print('page_prefix is ' + page_prefix)
                            print('page_number is ' + str(page_number))
                            break
                        elif href_str == '尾页':
                            print('current url has one page ' + url)
                            page_number = 1
                    if page_number == 0 and url.startswith(findlaw_jiaotongfaguiku_url):
                        page_hrefs.append(url)
                    elif page_number == 0:
                        print('Can not parse page prefix in this url ' + url)
                        return []
                    elif page_number > 1:
                        for page in range(page_number):
                            page_hrefs.append(page_prefix + '_' + str(page+1) + '.' + page_suffix)
                    else:
                        page_hrefs.append(url)
                    break
        except Exception as e:
            # print('Something wrong happened in url2page!')
            # print(url)
            print(e)
            count += 1
    if count >= MAX_TIME:
        print('current url is unavailable ' + url)

    return page_hrefs


def base2result():
    hrefs = []

    for current_url in findlaw_search_urls:
        count = 0
        more_hrefs = []

        while count < MAX_TIME:
            try:
                proxy = urllib.request.ProxyHandler(test.get_random_ip())
                opener = request.build_opener(proxy, request.HTTPHandler)
                opener.addheaders = [('User-Agent', ua.random)]
                request.install_opener(opener)
                response = request.urlopen(current_url, timeout=FETCHTIME_OUT)
                # opener = request.Request(current_url, headers={'User-Agent': ua.random})
                # response = request.urlopen(opener, timeout=FETCHTIME_OUT)
                if response:
                    soup = BeautifulSoup(response, cr_parser)
                    more_result = filter(None, soup.find_all('a', class_='common-load-more'))
                    if more_result is None:
                        # print('Something wrong happened in base2result!')
                        # print(current_url)
                        count += 1
                    else:

                        for result in more_result:
                            result = result.get('href')
                            if result.startswith(findlaw_base_url):
                                more_hrefs.append(result)
                        temp_hrefs = list(easy_parallelize(url2page, more_hrefs, pool_size=4))
                        hrefs.extend(list(easy_parallelize(url2url, href, pool_size=4)) for href in temp_hrefs)
                        break
                else:
                    count += 1
            except Exception as e:
                # print('Something wrong happened in base2result!')
                # print(current_url)
                print(e)
                count += 1
        if count >= MAX_TIME:
            print('current url is unavailable ' + current_url)

    return hrefs


def href2txt(link):
    content_id = link.split('/')[-1].split('.')[0]
    if not isNumber(content_id):
        print('current url is wrong ' + link)
        return

    count = 0

    while count < MAX_TIME:
        try:
            if not check_db('content_id = ' + content_id, findlaw_shelve_dir):
                total_text = ''
                proxy = urllib.request.ProxyHandler(test.get_random_ip())
                opener = request.build_opener(proxy, request.HTTPHandler)
                opener.addheaders = [('User-Agent', ua.random)]
                request.install_opener(opener)
                response = request.urlopen(link, timeout=FETCHTIME_OUT)
                # opener = request.Request(link, headers={'User-Agent': ua.random})
                # response = request.urlopen(opener, timeout=FETCHTIME_OUT)
                if response:
                    soup = BeautifulSoup(response, cr_parser)
                    xml = soup.find_all('p')
                    if xml is None:
                        # print('current link has none txt: ' + link)
                        count += 1
                    else:

                        for sentence in xml:
                            sentence = sentence.get_text().strip()
                            if sentence != '':
                                sentence = sentence.split(' ')
                                sentence = ''.join(sentence)
                                total_text += sentence + '\n'

                    filename = findlaw_save_dir + content_id + '.txt'
                    file = open(filename, 'a+', encoding='utf-8')
                    file.write(total_text)
                    file.close()
                    print('current id = ' + content_id + ' has been crawled!')
                    break
                else:
                    # print('Something wrong happened in href2txt!')
                    # print(link)
                    count += 1
        except Exception as e:
            # print('Something wrong happened in href2txt!')
            # print(link)
            print(e)
            count += 1
        if count < MAX_TIME:
            delete_db('content_id = ' + content_id, findlaw_shelve_dir)

    if count >= MAX_TIME:
        print('current url is unavailable ' + link)


def isNumber(string):
    for i in range(len(string)):
        if '9' >= string[i] >= '0':
            continue
        else:
            return False
    return True


def findlawcrawler():
    """
    crawl data from http://china.findlaw.cn/jiaotongshigu/
    :return:


    """
    urls_group = base2result()

    for urls in urls_group:
        for url in urls:
            crawl_ThreadSubmit(href2txt, url, workers=1)


if __name__ == '__main__':
    findlawcrawler()

    if os.path.exists(findlaw_save_dir):
        files = os.listdir(findlaw_save_dir)
        print('Total counts of laws in findlaw file is ' + str(len(files)))

