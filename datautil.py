# -*-coding:utf-8-*-

import sys
sys.path.append('../')
import shelve
import os
import codecs
from config import *


# empty persistent storage of download txt
def shelve_setup(filename):
    db = shelve.open(filename, writeback=True)
    assert isinstance(db, shelve.Shelf)

    try:
        for key in db:
            del db[key]
    finally:
        db.close()


# check current entry is exist or not
def check_db(entry, filename):
    db = shelve.open(filename, writeback=True)
    try:
        if entry in db:
            print('[] found'.format(entry))
            exist = True
        else:
            db[entry] = ''
            exist = False
    finally:
        db.close()

    return exist


def delete_db(entry, filename):
    db = shelve.open(filename, writeback=True)
    try:
        if entry in db:
            del db[entry]
    finally:
        db.close()


def sentence_extractor(data_dir, K=10):
    sentences = []
    path_list = os.listdir(data_dir)

    for i in range(len(path_list)):
        files = os.path.join(data_dir, path_list[i])
        with codecs.open(files, 'r+', encoding='utf-8', errors='ignore') as file:
            sen = ''

            for line in file.readlines():
                line = line.lstrip().rstrip()
                for word in line:
                    if word not in ['。', '！', '？']:
                        sen += word
                    else:
                        sen += word
                        if len(sen) > K:
                            sentences.append(sen.strip() + '\n')
                        sen = ''
                if sen != '' and sen[-1] in ['：', ';', '，', '、']:
                    continue
                else:
                    sen = ''
        # print('Current file ' + path_list[i] + ' has been counted!')

    print('current file is ' + data_dir)
    print('current file has ' + str(len(path_list)) + ' pages!')
    print('current file has ' + str(len(sentences)) + ' sentences!')

    sentences = list(set(sentences))
    print('there has ' + str(len(sentences)) + ' after cleaning')
    print('----------------------------------------------------')

    filename = data_dir + '/' + data_dir.split('/')[-1] + '.txt'
    with codecs.open(filename, 'w+', encoding='utf-8', errors='ignore') as file:
        file.writelines(sentences)


def total_sentences(data_dir):
    sentences = []
    path_list = os.listdir(data_dir)

    for i in range(len(path_list)):
        files = os.path.join(data_dir, path_list[i])
        with codecs.open(files, 'r+', encoding='utf-8', errors='ignore') as file:
            for sentence in file.readlines():
                sentences.append(sentence.strip() + '\n')

    sentences = list(set(sentences))
    print()
    print('Total number of sentences is ' + str(len(sentences)))

    with codecs.open('data/total_data/total_data.txt', 'w+', encoding='utf-8', errors='ignore') as file:
        file.writelines(sentences)


if __name__ == '__main__':
    # sentence_extractor('data/chinalaw', K=8)
    #
    # sentence_extractor('data/chinacourt', K=8)
    #
    # sentence_extractor('data/zhengce', K=8)
    #
    # sentence_extractor('data/globallaw', K=8)
    #
    # sentence_extractor('data/66law', K=8)
    #
    # sentence_extractor('data/findlaw', K=10)

    total_sentences('data/total_data')