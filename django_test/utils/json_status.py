# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :app01
# @File     :json_status
# @Date     :2025/5/29 14:28
# @Author   :zhuzhenzhong
# @Description :封装统一的接口响应码
-------------------------------------------------
"""

from django.http import JsonResponse

class Code:

    ok = 2
    params_error = 1
    un_auth_error = 403
    server_error = 500

