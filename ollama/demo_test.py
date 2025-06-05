# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :demo_test
# @Date     :2025/5/28 20:22
# @Author   :zhuzhenzhong
# @Description :ollama模型调试大模型
-------------------------------------------------
"""
import sys
from ollama import chat
from ollama import ChatResponse

def ollama_chat(role:str,content:str):
    response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=[
        {
            'role': role,
            'content': content,
        },
    ])
    print(response.message.content)
    return response.message.content


if __name__=="__main__":
    # role=sys.argv[1]
    # content= sys.argv[2]

    a=input("请输入你的使用角色，比如user,admin等等：")
    b=input("请输入提示词：")

    print("以下是AI自动生成的文案，请参考 \n")
    # print(ollama_chat(role=role,content=content))
    print(ollama_chat(role=a, content=b))
