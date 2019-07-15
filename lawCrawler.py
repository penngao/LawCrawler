from ChinaLawCrawler.geturl import *
from ChinaLawCrawler.retriever import *
from ChinaLawCrawler.chinalawcrawler import *
import easy_parallelize
import os

if __name__ == '__main__':
    base = '全库'
    keyword = '交通'
    type = 1
    chinalawcrawler(base, keyword, search_type=type)

    if os.path.exists(chinalaw_save_dir):
        files = os.listdir(chinalaw_save_dir)
        print('Total counts of laws in chinalaw file is ' + str(len(files)))

