# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : test.py
'''


from faker import Faker


class Generate_File():
    def __init__(self):
        # self.fake = Faker(locale="zh-CN")
        self.fake = Faker()

    def generate_text(self, file_format, file_size):
        """
        生成txt、doc、docx、xls、xlsx等格式指定大小文件
        :param file_format: 要生成的文件格式，如txt、doc、docx、xls、xlsx
        :param file_size: 生成文件的大小，单位M
        :return:
        """
        text = self.fake.text()     # 生成要重复的文本
        text_size_bytes = len(text.encode('utf-8'))     # 每个重复的文本的大小（以字节为单位）
        file_size_bytes = 1024 * 1024 * file_size
        repetitions = int(file_size_bytes) // text_size_bytes    # 需要重复的次数
        remainder = int(file_size_bytes) % text_size_bytes
        file_path = "testfile.{}".format(file_format)
        with open(file_path, 'w') as file:
            for _ in range(repetitions):
                file.write(text)
            if remainder > 0:
                file.write(text[:remainder])
        print("生成完成,生成的文件在当前exe所在的文件夹下，文件名为testfile")


if __name__ == "__main__":
    file_format = str(input("请输入要生成的文件格式如txt、doc、docx、xls、xlsx: "))
    file_size = float(input("请输入要生成的文件大小如10M请输入10： "))
    # print(file_size,type(file_size))
    if file_format in ('txt','doc','docx','xls','xlsx'):
        GF = Generate_File()
        GF.generate_text(file_format, file_size)
    else:
        print("输入的文件格式不对，请检查后重新输入，只支持txt、doc、docx、xls、xlsx")
    input("按下任意键退出程序。")