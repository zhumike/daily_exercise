# -*- coding: utf-8 -*-
# @Time : 2022/11/1 8:06 下午
# @Author : zhuzhenzhong
#coding=utf8
import xlrd
import numpy as np
from pyecharts.charts import Bar
from pyecharts.charts import Pie, Grid
from pyecharts import options as opts
import pandas as pd

# #导入Excel 文件
# data =  xlrd.open_workbook("测试数据1.xls")
# print(data)
# #载入第一个表格
# table = data.sheets()[0]
# print(table)


IO  = '测试数据1.xls'#'/Users/admin/zhuzhenzhong/python/tools/可视化/测试数据1.xsl'
raw_data = pd.read_excel(io=IO)
print(raw_data)
print(raw_data.values) #只提取有效数据

# import pandas as pd
# import numpy as np
#
# df = pd.DataFrame(np.random.randn(10,4),index=pd.date_range('2018/12/18',
#    periods=10), columns=list('ABCD'))
#
# df.plot()

