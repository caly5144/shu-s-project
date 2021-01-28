'''
Author: Dong Xing
Date: 2021-01-28 13:36:17
LastEditors: Dong Xing
LastEditTime: 2021-01-28 17:44:37
Description: file content
'''
import jieba
import re
import os
import numpy as np

import codecs
import chardet


class SimilarTest(object):
    def __init__(self, a_path, b_path):
        s1_code = self.get_code(a_path)
        s2_code = self.get_code(b_path)
        chars_pattern = re.compile(
            r'[\s·’!"\#$%&\'\(\)＃！（）*\+,-./:;<=>\?\@，：?￥★＊、…．＞【】［］《》？“”‘’\[\]\^_`{|}~。—]+')
        s1 = open(a_path, 'r', encoding=s1_code, errors='ignore').read()
        s2 = open(b_path, 'r', encoding=s2_code, errors='ignore').read()
        # 去除标点符号
        self.s1 = chars_pattern.sub("", s1)
        self.s2 = chars_pattern.sub("", s2)

        # 设置停用词
        self.stopwords = open('./stopwords/baidu_stopwords.txt',
                              'r', encoding='utf-8-sig').read().splitlines()

    def test(self):
        s1_split = np.array(jieba.lcut(self.s1))
        s2_split = np.array(jieba.lcut(self.s2))
        s1_cut = s1_split[~np.isin(s1_split, self.stopwords)]
        s2_cut = s2_split[~np.isin(s2_split, self.stopwords)]
        word_set = np.union1d(s1_cut, s2_cut)
        # 用字典保存两篇文章中出现的所有词并编上号
        word_dict = dict()
        for i, word in enumerate(word_set):
            word_dict[word] = i

        # 根据词袋模型统计词在每篇文档中出现的次数，形成向量
        s1_cut_code = np.zeros(len(word_dict))
        s2_cut_code = np.zeros(len(word_dict))

        for word in s1_cut:
            s1_cut_code[word_dict[word]] += 1
        for word in s2_cut:
            s2_cut_code[word_dict[word]] += 1

        # 计算余弦相似度
        try:
            cos_arr = np.sum(s1_cut_code * s2_cut_code)
            sq1 = np.power(s1_cut_code, 2).sum()
            sq2 = np.power(s2_cut_code, 2).sum()
            result = np.around(cos_arr / (np.sqrt(sq1) * np.sqrt(sq2)), 3)
        except ZeroDivisionError:
            result = 0.0
        print("文本相似度为：{}".format(result))

    @staticmethod
    def get_code(path):
        with open(path, 'rb') as file:
            data = file.read(200)
            dicts = chardet.detect(data)
        return dicts["encoding"]


if __name__ == '__main__':
    a_path = 'atext.txt'
    b_path = 'btext.txt'
    textST = SimilarTest(a_path, b_path)
    textST.test()
