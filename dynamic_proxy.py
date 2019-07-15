# -*-coding:utf-8-*-
from typing import List, Any, Generator
from urllib import request
from config import ua, proxy_pickle_dir, findlaw_base_url
import random
import codecs
import pickle
import os


class GetProxy():
    def __init__(self, filename, pickle_dir=None):
        """
        :param filename of ip proxies
        :param pickle filename of pickle file
        """
        self.proxies = []  # will contain proxies [ip, port, available]
        self.available_proxies = {}
        self.pickle_dir = pickle_dir
        with codecs.open(filename, 'r+', encoding='utf-8', errors='ignore') as file:
            sentences = file.read()
            for sentence in sentences.split(' '):
                ip = sentence.split(':')[0]
                port = sentence.split(':')[1]
                self.proxies.append([ip, port, 1])
            file.close()

    def update_available_ip(self, url):
        """
        :param url: the target url of crawler
        :return:
        """
        if not os.path.exists(self.pickle_dir):

            for i in range(len(self.proxies)):
                if self.proxies[i][2] == 1:
                    proxy_url = self.proxies[i][0] + ':' + self.proxies[i][1]
                    print('proxy_url ' + proxy_url)
                    try:
                        proxy_agent = {'http': proxy_url}
                        proxy = request.ProxyHandler(proxy_agent)
                        opener = request.build_opener(proxy, request.HTTPHandler)
                        opener.addheaders = [('User-Agent', ua.random)]
                        request.install_opener(opener)
                        response = request.urlopen(url, timeout=1)
                        if response:
                            print('current ip is available ' + self.proxies[i][0])
                            self.proxies[i][2] = 1
                    except Exception as e:
                        print(e)
                        print('current ip is not available ' + self.proxies[i][0])
                        self.proxies[i][2] = 0

            for line in self.proxies:
                if line[2] == 1:
                    self.available_proxies.update({line[0]: line[1]})
            with open(proxy_pickle_dir, 'wb') as p:
                pickle.dump(self.available_proxies, p)
        else:
            with open(proxy_pickle_dir, 'rb') as r:
                self.available_proxies = pickle.load(r)
                for key, value in self.available_proxies.items():
                    proxy_url = key + ':' + value
                    print('proxy_url ' + proxy_url)
                    try:
                        proxy_agent = {'http': proxy_url}
                        proxy = request.ProxyHandler(proxy_agent)
                        opener = request.build_opener(proxy, request.HTTPHandler)
                        opener.addheaders = [('User-Agent', ua.random)]
                        request.install_opener(opener)
                        response = request.urlopen(url, timeout=1)
                        if response:
                            print('current ip is available ' + key)
                    except Exception as e:
                        print(e)
                        print('current ip is not available ' + key)
                        del self.available_proxies[key]

        print('The number of available ip is ' + str(len(self.available_proxies)))

    def get_random_ip(self):
        selected_ip = random.choice(list(self.available_proxies.keys()))
        proxy_url = selected_ip + ':' + self.available_proxies.get(selected_ip)
        print('selected proxy is ' + proxy_url)
        proxy_agent = {'http': proxy_url}

        return proxy_agent


if __name__ == '__main__':
    test = GetProxy('proxy.txt', proxy_pickle_dir)
    test.update_available_ip(findlaw_base_url)
    test.get_random_ip()


