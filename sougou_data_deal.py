#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: sougou_data_deal.py
@description: 处理搜狗语料数据
"""
import re
import os
from collections import Counter


def create_data_set(file_dir: str):
    """
    提取语料中的文本及其标签
    :param file_dir: 处理的文件夹
    :return: contents_list, classes_list
    """
    # 定义提取数据的正则表达式
    # 获取所有文本对应url
    pattern_url = re.compile(r'<url>(.*?)</url>', re.S)
    # 提取文本内容
    pattern_content = re.compile(r'<content>(.*?)</content>', re.S)
    contents_list = []
    classes_list = []
    # 查看新闻的种类共有多少类以及各个类别有多少篇新闻
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file)
        with open(file_path, 'r', encoding='gb18030') as reader:
            text = reader.read()
            # 正则表达式匹配出url和content
            urls = pattern_url.findall(text)
            contents = pattern_content.findall(text)
            for i in range(len(urls)):
                # 提取文本类别
                pattern_class = re.compile(r'http://(.*?).sina.com', re.S)
                class_type_find = pattern_class.findall(urls[i])
                class_type = class_type_find[0] if class_type_find else ''
                content = contents[i]
                if class_type and content:
                    classes_list.append(class_type)
                    contents_list.append(content)
    return contents_list, classes_list

def create_data_set_by_file(file: str,limit:int=100000):
    """
    提取语料中的文本及其标签
    :param file_dir: 处理的文件夹
    :return: 
    """
    # 定义提取数据的正则表达式
    # 获取所有文本对应url
    pattern_url = re.compile(r'<url>(.*?)</url>', re.S)
    # 提取文本内容
    pattern_content = re.compile(r'<content>(.*?)</content>', re.S)
    pattern_contenttitle = re.compile(r'<contenttitle>(.*?)</contenttitle>', re.S)

    # 查看新闻的种类共有多少类以及各个类别有多少篇新闻
    
    file_path = file
    with open(file_path, 'r', encoding='gb18030') as reader:
        text = reader.read()
        # for line in reader:
            
        #     print(line)
        # 正则表达式匹配出url和content
        contenttitles = pattern_content.findall(text)

        # urls = pattern_url.findall(text)
        # contents = pattern_content.findall(text)
        # for i in range(len(urls)):
        #     # 提取文本类别
        #     pattern_class = re.compile(r'http://(.*?).sina.com', re.S)
        #     class_type_find = pattern_class.findall(urls[i])
        #     class_type = class_type_find[0] if class_type_find else ''
        #     content = contents[i]
        #     if class_type and content:
        #         classes_list.append(class_type)
        #         contents_list.append(content)

    if limit ==0:
        return contenttitles
    return contenttitles[:limit]


def simple_extract(contents: list, kinds: list, res_root: str = 'Data/SougouCA.reduced_Selected'):
    """
    根据一定规则提取数据，并存放到指定文件中。其中包含三个数据集train.txt, dev.txt,test.txt
    :param res_root:
    :param contents: 文本内容
    :param kinds: 文本对应标签
    :return: 并拆分成三个数据集
    """
    # 构建格式化数据
    X = []
    y = []
    counts = Counter(kinds)
    statistics = {}
    for kind, content in zip(kinds, contents):
        if kind == '2008':
            continue
        if counts.get(kind) >= 1000:
            if kind in statistics:
                if statistics[kind] > 1000:
                    continue
                else:
                    statistics[kind] += 1
            else:
                statistics[kind] = 1
            X.append(content)
            y.append(kind)
    # 开始将数据拆分为多个集
    X_train, X_dev_test, y_train, y_dev_test = train_test_split(X, y, test_size=0.4)
    X_dev, X_test, y_dev, y_test = train_test_split(X_dev_test, y_dev_test, test_size=0.5)
    # 保存数据为：类别\t内容
    with open(os.path.join(res_root, 'train.txt'), 'w', encoding='utf8') as writer:
        for content, kind in zip(X_train, y_train):
            writer.write("{}\t{}\n".format(kind, content))
    with open(os.path.join(res_root, 'dev.txt'), 'w', encoding='utf8') as writer:
        for content, kind in zip(X_dev, y_dev):
            writer.write("{}\t{}\n".format(kind, content))
    with open(os.path.join(res_root, 'test.txt'), 'w', encoding='utf8') as writer:
        for content, kind in zip(X_test, y_test):
            writer.write("{}\t{}\n".format(kind, content))
    # 保存数据为pkl格式


if __name__ == '__main__':
    dir_path = r'C:\Users\smock\Downloads\news_tensite_xml.full\news_tensite_xml.dat'
    res_root = r"C:\Users\smock\repo\BertMaskLM\train\sougou"
    contenttitles = create_data_set_by_file(dir_path,0)
    # simple_extract(content_lst, class_lst)
    with open(os.path.join(res_root, 'sougou_train_content.txt'), 'w', encoding='utf-8') as writer:
        for title in contenttitles:
            writer.write("{}\n".format(title))