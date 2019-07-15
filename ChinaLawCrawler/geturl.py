import sys
sys.path.append("..")
from easy_parallelize import *
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from config import *


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
                results = filter(None, soup.find_all('a'))
                for href in results:
                    if href.get('href').startswith('law'):
                        hrefs.append(href.get('href'))

        except Exception as e:
            print('Something wrong happened in url2url')
            print(e)

        return hrefs

    def base2result(self, strbase):

        if strbase is None:
            return None

        law_first_url = chinalaw_first_url_type1.get(strbase) if self.type == 1 else chinalaw_first_url_type2.get(strbase)
        url = chinalaw_base_url + law_first_url \
              + chinalaw_second_url + chinalaw_third_url \
              + str(self.keyword) + '&Type=' + str(self.type)
        result = []
        urls = []

        try:
            opener = request.Request(url, headers={'user-agent': ua.random})
            reponse = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if reponse:
                soup = BeautifulSoup(reponse, cr_parser)
                count_result = soup.find(id='pagecount')
                pagecount = 1 if count_result is None else int(count_result.get_text())

                for page in range(pagecount):
                    urls.append(chinalaw_base_url + law_first_url
                                + chinalaw_second_url + str(page + 1)
                                + chinalaw_third_url + self.keyword
                                + '&Type=' + str(self.type))
                # this stape can use parallelize
                result.extend(easy_parallelize(self.url2url, urls, pool_size=4))
                # print(result)

            return result

        except Exception as e:
            print('Something wrong happened in base2result')
            print(e)


if __name__ == '__main__':
    base = '全库'
    test = StringToUrl()
    test.base2result(base)
