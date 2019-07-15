from ChinaLawCrawler.geturl import *
from ChinaLawCrawler.retriever import *
from datautil import *
import os


def chinalawcrawler(base, keyword, search_type=1):
    """
    :param base: choose from "全库", "法律", "行政法规", "国务院部门规章",
                             "地方性法规", "地方政府规章", "司法解释"
    :param keyword: search keyword like "交通", "道路"
    :param search_type: 1 represent "按标题检索"
                        2 represent "按正文检索"
    :return:
    """
    urls = StringToUrl(string=keyword, search_type=search_type)
    result = urls.base2result(base)
    for barch in result:
        crawl_ThreadSubmit(ChinaLawUrlToTxt().result2hrefs, barch)


if __name__ == '__main__':
    base = '全库'
    keyword_1 = '交通'
    keyword_2 = '道路'
    shelve_setup(chinalaw_shelve_dir)
    chinalawcrawler(base, keyword_1, search_type=1)
    chinalawcrawler(base, keyword_2, search_type=1)
    chinalawcrawler(base, keyword_1, search_type=2)
    chinalawcrawler(base, keyword_2, search_type=2)

    if os.path.exists(chinalaw_save_dir):
        files = os.listdir(chinalaw_save_dir)
        print('Total counts of laws in chinalaw file is ' + str(len(files)))
