# -*- coding: utf-8 -*-
# @Time : 2022/7/11 4:53 下午
# @Author : zhuzhenzhong
import json
import json

# JSON string:
# Multi-line string
# x = """{
#     "Name":"Jennifer Smith",
#     "Contact Number":7867567898,
#     "Email":"jen123@gmail.com",
#     "Hobbies":["Reading", "Sketching", "Horse Riding"]
#     }"""
#
# # parse x:
# y = json.loads(x)
#
# # the result is a Python dictionary:
# print(y)
#
#
#
#
#
# # JSON string
# employee = '{"id":"09", "name":"Nitin", "department":"Finance"}'
#
# # Convert string to Python dict
# employee_dict = json.loads(employee)
# print(employee_dict)
#
# print(employee_dict['name'])

str = {"total_count":2,
"total_download_psm":4,
"waiting_time":120,
"total_task":3,
"strong_dependency":3,
"week_dependency":2,
"detail":[
{"cluster":"default",
 "method":"test1",
 "case":"demo1",
 "result_list":[
 {"id":1,
  "psm":"ad.search.t1",
  "method":"qat1",
  "dep_type":1,
  "is_destructive":"false",
   "report_list_history":[
   {"id":121,"status":1,'url':'http://bytedpe.bytedance.net/'},
   {"id":122,"status":1,'url':'http://bytedpe.bytedance.net/'}
]

},
 {"id":2,
  "psm":"ad.search.t2",
  "method":"qat2",
  "dep_type":1,
  "is_destructive":"false",
   "report_list_history":[
   {"id":123,"status":1,'url':'http://bytedpe.bytedance.net/'},
   {"id":124,"status":2,'url':'http://bytedpe.bytedance.net/'},
   {"id":125,"status":1,'url':'http://bytedpe.bytedance.net/'}
]

}
]
},
{"cluster":"default2",
 "method":"test21",
 "case":"demo21",
 "result_list":[
 {"id":3,
  "psm":"ad.search.t21",
  "method":"qat21",
  "dep_type":1,
  "is_destructive":"false",
   "report_list_history":[
   {"id":1221,"status":1,'url':'http://bytedpe.bytedance.net/'},
   {"id":1222,"status":1,'url':'http://bytedpe.bytedance.net/'}
]

},
 {"id":4,
  "psm":"ad.search.t22",
  "method":"qat22",
  "dep_type":1,
  "is_destructive":"false",
   "report_list_history":[
   {"id":1223,"status":1,'url':'http://bytedpe.bytedance.net/'},
   {"id":1224,"status":2,'url':'http://bytedpe.bytedance.net/'},
   {"id":1225,"status":1,'url':'http://bytedpe.bytedance.net/'}
]

}
]
}

]
}
print (json.loads('"%s"' %str))
