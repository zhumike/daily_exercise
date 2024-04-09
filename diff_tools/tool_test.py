# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : tool_test.py
'''

import difflib
text1 = "Hello, World!"
text2 = "Hello, Python!"
differ = difflib.Differ()
diff = differ.compare(text1, text2)
print(' '.join(diff))