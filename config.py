from fake_useragent import UserAgent

# most common user agent according to: https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
ua = UserAgent(use_cache_server=False)
VERSION = '0.2'

proxy_addr = ''
FETCHTIME_OUT = 10
cr_parser = 'html5lib'

# max crawl time for each time
MAX_TIME = 3

# crawl data from search.chinalaw.gov.cn
# save file
chinalaw_save_dir = '../data/chinalaw/'
chinalaw_shelve_dir = '../ChinaLawCrawler/download_db.db'

# the url information
chinalaw_base_url = 'http://search.chinalaw.gov.cn/'
chinalaw_first_url_type1 = {'全库': 'SearchLawTitle?effectLevel=',
                       '法律': 'SearchLawTitle?effectLevel=2',
                       '行政法规': 'SearchLawTitle?effectLevel=3',
                       '国务院部门规章': 'SearchLawTitle?effectLevel=4',
                       '地方性法规': 'SearchLawTitle?effectLevel=5',
                       '地方政府规章': 'SearchLawTitle?effectLevel=6',
                       '司法解释': 'SearchLawTitle?effectLevel=7'}
chinalaw_first_url_type2 = {'全库': 'SearchLaw?effectLevel=',
                       '法律': 'SearchLaw?effectLevel=2',
                       '行政法规': 'SearchLaw?effectLevel=3',
                       '国务院部门规章': 'SearchLaw?effectLevel=4',
                       '地方性法规': 'SearchLaw?effectLevel=5',
                       '地方政府规章': 'SearchLaw?effectLevel=6',
                       '司法解释': 'SearchLaw?effectLevel=7'}
chinalaw_second_url = '&SiteID=124&PageIndex='
chinalaw_third_url = '&Sort=PublishTime&Query='

# crawl data from http://www.gov.cn/zhengce/zc_flfg.htm
# save file
zhengce_save_dir = '../data/zhengce/'
zhengce_shelve_dir = '../ZhengCeCrawler/download_db.db'

# the url information
zhengce_base_url = ''
zhengce_first_url = 'http://sousuo.gov.cn/s.htm?q='
zhengce_second_url = '&n=10&p='
zhengce_third_url = '&t=govall&timetype=timeqb&mintime=&maxtime=&sort=&sortType=1&nocorrect='

# second section of the url
zhengce_stratswith = ('http://www.gov.cn/xinwen',)
# 'http://www.gov.cn/jrzg',
# 'http://www.gov.cn/wenzheng',
# 'http://www.gov.cn/gzdt',
# 'http://www.gov.cn/zwgk',
# 'http://www.gov.cn/fwxx',
# 'http://www.gov.cn/zhengce',
# 'http://www.gov.cn/fwxx'

# max page
zhengce_max_page = 540

# crawl data from https://www.chinacourt.org/law.shtml
# save file
chinacourt_save_dir = '../data/chinacourt/'
chinacourt_shelve_dir = '../ChinaCourtCrawler/download_db.db'

# url information
chinacourt_base_url = 'https://www.chinacourt.org'
chinacourt_first_url = 'https://www.chinacourt.org/law/searchproc/keyword/'
chinacourt_second_url = '/t/1/law_type_id//page/'
chinacourt_third_url = '.shtml'

# crawl data from http://policy.mofcom.gov.cn/law/index.shtml
# save file
globallaw_save_dir = '../data/globallaw/'
globallaw_shelve_dir = '../GlobalLawCrawler/download_db.db'

# url information
globallaw_base_url = 'http://policy.mofcom.gov.cn/law/index.shtml'
globallaw_startswith = ('/claw/clawContent.shtml?id=', '/pact/pactContent.shtml?id=')
globallaw_claw_base_url = 'http://policy.mofcom.gov.cn/claw/keySearchMore.shtml?'
globallaw_first_url = ['http://policy.mofcom.gov.cn/claw/keySearchList.shtml?keyword=',
                       'http://policy.mofcom.gov.cn/pact/index.shtml?keyword=']
globallaw_search_url = 'http://policy.mofcom.gov.cn'

# crawl data from https://www.66law.cn/laws/jiaotongshigu/
# save file
hualv_save_dir = '../data/66law/'
hualv_shelve_dir = '../HuaLvCrawler/download_db.db'

# url information
hualv_base_url = 'https://www.66law.cn'
hualv_first_search_urls = ['/laws/jiaotongshigu/jtsgjd/',
                           '/laws/jiaotongshigu/jtsgrd/',
                           '/laws/jiaotongshigu/jtsgcl/',
                           '/laws/jiaotongshigu/sgpc/']
hualv_second_search_urls = ['/laws/jiaotongshigu/topic2012/',
                            '/laws/jiaotongshigu/special/']
hualv_another_startswith = ('/special/', '/topic2012/')

# crawl data from http://china.findlaw.cn/jiaotongshigu/jiaotongfa/
# save file
findlaw_save_dir = '../data/findlaw/'
findlaw_shelve_dir = '../FindLawCrawler/download_db.db'

# url information
findlaw_base_url = 'http://china.findlaw.cn/jiaotongshigu/'
findlaw_jiaotongfaguiku_url = 'http://china.findlaw.cn/jiaotongshigu/jiaotongfa/jiaotongfaguiku/'
findlaw_search_urls = ['http://china.findlaw.cn/jiaotongshigu/baoxianlipei/',
                       'http://china.findlaw.cn/jiaotongshigu/jtsgql/',
                       'http://china.findlaw.cn/jiaotongshigu/jtsgld/',
                       'http://china.findlaw.cn/jiaotongshigu/jtsgjd/',
                       'http://china.findlaw.cn/jiaotongshigu/jtsgpc/',
                       'http://china.findlaw.cn/jiaotongshigu/jiaotongfa/']


# proxy pickle file
proxy_pickle_dir = '../proxy.pickle'