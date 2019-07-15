from urllib import request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from config import *
from datautil import *
import re


class ChinaLawUrlToTxt():

    def __init__(self):
        self.sentencebase = []
        self.lawid = ''

    def href2txt(self, link, page):

        if not check_db(self.lawid + '_' + str(page), chinalaw_shelve_dir):
            total_txt = ''

            try:
                opener = request.Request(link, headers={'user-agent': ua.random})
                reponse = request.urlopen(opener, timeout=FETCHTIME_OUT)
                filename = chinalaw_save_dir + self.lawid + '.txt'
                file = open(filename, 'a+', encoding='utf-8')
                if reponse:
                    soup = BeautifulSoup(reponse, cr_parser)
                    title = ''
                    if page == 1:
                        titleresult = soup.find('div', class_='conTit')
                        if titleresult is None:
                            return
                        title = titleresult.get_text() + '\n'
                    total_txt += title
                    xml = soup.find_all(re.compile('^p'))

                    if xml is None:
                        return

                    for sentence in xml:
                        if sentence.get_text() != '':
                            total_txt += sentence.get_text() + '\n'

                    for sentence in total_txt.split('\n'):
                        if sentence not in self.sentencebase:
                            self.sentencebase.append(sentence)
                            file.write(sentence + '\n')
                    file.close()
                    print('Lawid = ' + str(self.lawid) + '\' page ' + str(page) + ' has been crawled.')
                    self.sentencebase.clear()

            except Exception as e:
                print('Something happened in href2txt method! current lawid = ' + str(self.lawid))
                print(e)

    # link represent the href of super stage
    def result2hrefs(self, link):

        self.lawid = link.split('&')[0].split('=')[-1]

        try:
            link = urljoin(chinalaw_base_url, link) + '&PageIndex='
            opener = request.Request(link, headers={'user-agent': ua.random})
            response = request.urlopen(opener, timeout=FETCHTIME_OUT)
            if response:
                soup = BeautifulSoup(response, cr_parser)
                pageresult = soup.find(id='pagecount')
                pagecount = 1 if pageresult is None else int(pageresult.get_text())
                for i in range(pagecount):
                    curr_link = link + str(i+1)
                    self.href2txt(curr_link, i+1)
                print('Lawid = ' + str(self.lawid) + ' has been crawled completely!')

        except Exception as e:
            print('Something wrong happened in result2hrefs method! current lawid = ' + str(self.lawid))
            print(e)


if __name__ == '__main__':

    url = 'law/searchTitleDetail' \
          '?LawID=406380&Query=%E4%BA%A4%E9%80%9A&IsExact='
    test = ChinaLawUrlToTxt()
    test.result2hrefs(url)
