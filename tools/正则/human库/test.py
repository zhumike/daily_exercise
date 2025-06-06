# -*- coding: utf-8 -*-
# @Time : 2022/9/26 5:20 下午
# @Author : zhuzhenzhong
from humre import *
"""简化正则表达式"""



text = 'Call 415-555-1234 today!'
regexStr = exactly(3, DIGIT) + '-' + exactly(3, DIGIT) + '-' + exactly(4, DIGIT)
result = compile(regexStr).search(text)
print(result.group())


compile(
    either(
        noncap_group(noncap_group(either('0x', '0X')), one_or_more(chars('0-9a-f'))),
        noncap_group(noncap_group(either('0x', '0X')), one_or_more(chars('0-9A-F'))),
        noncap_group(one_or_more(chars('0-9a-f'))),
        noncap_group(one_or_more(chars('0-9A-F')))
    )
)