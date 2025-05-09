# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : tool_test.py
参考链接：https://blog.51cto.com/u_16213346/12307506
比较文本差异部分
'''

import difflib
text1 = "Hello, World!"
text2 = "Hello, Python!"
differ = difflib.Differ()
diff = differ.compare(text1, text2)
print(' '.join(diff))

#test