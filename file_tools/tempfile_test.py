# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : tempfile_test.py
'''


import tempfile
# 创建临时文件
with tempfile.NamedTemporaryFile() as temp_file:
    print(temp_file.name)
# 创建临时目录
with tempfile.TemporaryDirectory() as temp_dir:
    print(temp_dir)