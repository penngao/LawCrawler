# -*-coding:utf-8-*-

import sys
sys.path.append('../')
from easy_parallelize import *
from urllib import request
from bs4 import BeautifulSoup
from config import *
from datautil import shelve_setup, check_db
import os


def url2url(url):
    hrefs = []
    next_href = url
    try:
        while next_href is not None:
            print('current parse href is ' + next_href)
            opener = request.Request(next_href, headers={'user-agent': ua.random})
            response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                href_result = soup.find_all('a', attrs={'target': '_blank'})
                if href_result is None:
                    print('Current url ' + url + ' has no href!')
                    return
                else:

                    for href in href_result:
                        href = href.get('href')
                        if href.startswith('/laws/'):
                            hrefs.append(hualv_base_url + href)
                        elif href.startswith(('http://lawyers.66law.cn/', 'https://lawyers.66law.cn/')) \
                                and href.endswith('.aspx'):
                            hrefs.append(href)
                    hrefs = list(set(hrefs))
                # search for next href
                next_href_result = soup.find('a', class_='m-page-next')
                if next_href_result is None:
                    break
                else:
                    next_href = next_href_result.get('href')
                    if next_href.startswith('/laws/'):
                        next_href = hualv_base_url + next_href
    except Exception as e:
        print('Something wrong happened in url2url')
        print(url)
        print(e)

    return hrefs


def another2url(url):
    hrefs = []

    try:
        opener = request.Request(url, headers={'user-agent': ua.random})
        response = request.urlopen(opener, timeout=FETCHTIME_OUT)
        if response:
            soup = BeautifulSoup(response, cr_parser)
            href_result = soup.find_all('a', attrs={'target': '_blank'})
            if href_result is None:
                print('Something wrong happened in another2url')
                print(url)
            else:

                for href in href_result:
                    href = href.get('href')
                    if href.startswith(('https://www.66law.cn/laws/', 'http://www.66law.cn/laws')):
                        hrefs.append(href)
                        print('add ' + href + ' to another2url results')
        else:
            print('Something wrong happened in another2url')
            print(url)
    except Exception as e:
        print('Something wrong happened in another2url')
        print(url)
        print(e)

    return list(set(hrefs))


def base2result():
    hrefs = []
    hrefs_result = []
    try:
        for first_url in hualv_first_search_urls:
            first_url = hualv_base_url + first_url
            opener = request.Request(first_url, headers={'user-agent': ua.random})
            response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                more_result = filter(None, soup.find_all('a', class_='fr f16 s-c358'))
                if more_result is None:
                    print('Something wrong happened in base2result!')
                    print(first_url)
                    return
                else:

                    for result in more_result:
                        result = result.get('href')
                        if result.startswith('/laws/jiaotongshigu/'):
                            hrefs.append(hualv_base_url + result)
                            print('add ' + hualv_base_url + result + ' to base2result results')

        # hrefs.append(hualv_base_url + '/laws/jiaotongshigu/anli/')
        hrefs = list(set(hrefs))
        for href in hrefs:
            temp_href = url2url(href)
            temp_href = list(set(temp_href))
            if temp_href:
                hrefs_result.append(temp_href)
    except Exception as e:
        print('Something wrong happened in base2result')
        print(e)

    return hrefs_result


def another2result():
    hrefs = []
    hrefs_result = []

    try:
        for url in hualv_second_search_urls:
            url = hualv_base_url + url
            next_url = url

            while next_url is not None:
                print(next_url + ' in another2result')
                opener = request.Request(next_url, headers={'user-agent': ua.random})
                response = request.urlopen(opener, timeout=FETCHTIME_OUT)
                if response:
                    soup = BeautifulSoup(response, cr_parser)
                    more_result = filter(None, soup.find_all('a', attrs={'target': '_blank'}))
                    if more_result is None:
                        print('Something wrong happened in another2result!')
                        print(next_url)
                    else:

                        for result in more_result:
                            result = result.get('href')
                            if result.startswith(hualv_another_startswith):
                                hrefs.append(hualv_base_url + result)
                                print('add ' + hualv_base_url + result + ' to another2result results')

                next_url_result = soup.find('a', class_='m-page-next')
                if next_url_result is None:
                    break
                else:
                    next_url = next_url_result.get('href')
                    if next_url.startswith('/laws/'):
                        next_url = hualv_base_url + next_url

        hrefs = list(set(hrefs))
        for href in hrefs:
            temp_hrefs = another2url(href)
            temp_hrefs = list(set(temp_hrefs))
            if temp_hrefs:
                hrefs_result.append(temp_hrefs)
    except Exception as e:
        print('Something wrong happened in another2result')
        print(e)

    return hrefs_result


def href2result(link):
    content_id = link.split('/')[-1].split('.')[0]

    try:
        if not check_db('content_id = ' + content_id, hualv_shelve_dir):
            total_text = ''
            opener = request.Request(link, headers={'user-agent': ua.random})
            response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                xml = soup.find_all('p')
                if xml is None:
                    print('content_id = ' + content_id + ' is none')
                    print(link)
                    return
                else:
                    for sentence in xml:
                        sentence = sentence.get_text().strip()
                        if sentence != '':
                            sentence = sentence.split(' ')
                            sentence = ''.join(sentence)
                            total_text += sentence + '\n'

                filename = hualv_save_dir + content_id + '.txt'
                file = open(filename, 'a+', encoding='utf-8')
                file.write(total_text)
                file.close()
                print('current id = ' + content_id + ' has been crawled')
            else:
                print('Something wrong happened is href2result!')
                print(link)
    except Exception as e:
        print('Something wrong happened in href2result')
        print(link)
        print(e)


def hualvcrawler():
    """
    crawl data from https://www.66law.cn
    :return:
    """
    urls = []
    urls.extend(base2result())
    # urls.extend(another2result())

    for url in urls:
        crawl_ThreadSubmit(href2result, url, workers=1)


if __name__ == '__main__':
    # shelve_setup(hualv_shelve_dir)
    hualvcrawler()

    if os.path.exists(hualv_save_dir):
        files = os.listdir(hualv_save_dir)
        print('Total counts of laws in hualv file is ' + str(len(files)))
