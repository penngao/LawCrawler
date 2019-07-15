from multiprocessing.dummy import Pool
from concurrent.futures import ThreadPoolExecutor
import concurrent


def easy_parallelize(func, data, pool_size=None):

    if pool_size is None or pool_size < 1:
        pool = Pool(processes=len(data))
    else:
        pool = Pool(processes=pool_size)

    results = pool.map(func, data)
    cleaned = filter(None, results)

    pool.close()
    pool.join()

    return cleaned


def crawl_ThreadSubmit(func, urls, workers=1):
    process_pool = ThreadPoolExecutor(max_workers=workers)
    futures = {process_pool.submit(func, url): url for url in urls}

    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            print(result)
        except Exception as e:
            print('Someting wrong happened in crawl_ThreadSubmit!')
            print(e)