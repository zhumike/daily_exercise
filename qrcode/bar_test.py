# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : bar_test.py
'''
import barcode
from barcode.writer import ImageWriter
# 设置要生成的字符串
data = '123456789'
# 创建EAN13条形码对象
ean = barcode.get('ean13', data, writer=ImageWriter())
# 保存条形码图片
filename = ean.save('barcode')