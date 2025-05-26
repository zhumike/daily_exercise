# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :replace_test
# @Date     :2025/5/25 08:46
# @Author   :zhuzhenzhong
# @Description :字符替换工具类
-------------------------------------------------
"""
import logging
import re
import pandas as pd
from bs4 import BeautifulSoup
import logging

import demo.demo_test

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Demo:
    def __init__(self,text=None,dataframe=None):
        self.text = text
        self.dataframe = dataframe

    """字符串替换功能函数"""
    def replace_string(self,old,new,count):
        return self.text.replace(old,new,count)


    def replace_regex(self,pattern,repl,flags=0):
        """
        正则替换效果
        :param pattern:
        :param repl:
        :param falgs:
        :return:
        """
        return re.sub(pattern,repl,self.text,flags=flags)

    def replace_dict(self,mapping):
        """
        多个关键词替换效果
        :param mapping:
        :return:
        """
        for old,new in mapping.items():
            if isinstance(old,str):
                self.text=self.text.replace(old,new)
            else:
                self.text=re.sub(old,new,self.text)
        return self.text

    def replace_dataframe(self,column,mapping):
        if self.dataframe is not None:
            self.dataframe[column] = self.dataframe[column].replace(mapping)
            return self.dataframe
        else:
            raise  ValueError("DataFrame 未提供")

    def replace_words_case_insensitive(self,mapping):

        words=self.text.split(",")
        logger.info(words)
        # print(words)
        replaced = []
        for word in words:
            lower_word = word.lower()
            if lower_word in mapping:
                replaced.append(mapping[lower_word])
            else:
                replaced.append(word)
        return ' '.join(replaced)


    def filter_sensitive_words(self,sensitive_words,replacement="*"):
        pattern = '|'.join([re.escape(word) for word in sensitive_words])
        return re.sub(pattern,lambda match:replacement * len(match.group()),self.text)

    def clean_html_tags(self):
        soup = BeautifulSoup(self.text,"html.parser")
        return soup.get_text()

if __name__=="__main__":
    demo_text = "HELLO ,hello,nihao,this is qa test,hello,hello,hello,World  world"
    replacer = Demo(text=demo_text)
    # print("单字符替换：",replacer.replace_string("Hello","Hi",5))
    # print("正则替换：",replacer.replace_regex(r"(hello|world)",r"***",flags=re.IGNORECASE))
    # mapping = {"test":"test_new","Hello":"Greeting"}
    # print("多关键词替换效果：{}".format(replacer.replace_dict(mapping)))
    # case_mapping={"hello":"glad","world":"city"}
    # print("不区分大小写替换：{}".format(replacer.replace_words_case_insensitive(case_mapping)))
    sensitive = ["hello","---"]
    print("敏感词过滤：",replacer.filter_sensitive_words(sensitive))

    #HTML标签清理
    html_text = "<h2> Hello"

    replacer.text = html_text
    print("标签清理结果：",replacer.clean_html_tags())



