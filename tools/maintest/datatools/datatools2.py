# -*- coding: utf-8 -*-
# @Time : 2021/9/26 10:34 上午
# @Author : zhuzhenzhong
#生成个人信息测试数据
import random
FirstNameList = "王李张刘陈杨赵黄周吴徐孙胡朱高林何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史"
SecondNameList = "大学之道在明明德在亲民在止于至善知止而后有定定而后能静静而后能安安而后能虑虑而后能得物有本末事有终始知所先后则近道矣古之欲明明德于天下者先治其国欲治其国者先齐其家欲齐其家者先修其身欲修其身者先正其心欲正其心者先诚其意欲诚其意者先致其知致知在格物物格而后知至知至而后意诚意诚而后心正心正而后身修身修而后家齐家齐而后国治国治而后天下平"
textList = "归去来兮田园将芜胡不归既自以心为形役奚惆怅而独悲悟已往之不谏知来者之可追实迷途其未远觉今是而昨非舟遥遥以轻飏风飘飘而吹衣问征夫以前路恨晨光之熹微乃瞻衡宇载欣载奔僮仆欢迎稚子候门三径就荒松菊犹存携幼入室有酒盈樽引壶觞以自酌眄庭柯以怡颜倚南窗以寄傲审容膝之易安园日涉以成趣门虽设而常关策扶老以流憩时矫首而遐观云无心以出岫鸟倦飞而知还景翳翳以将入抚孤松而盘桓归去来兮请息交以绝游世与我而相违复驾言兮焉求悦亲戚之情话乐琴书以消忧农人告余以春及将有事于西畴或命巾车或棹孤舟既窈窕以寻壑亦崎岖而经丘木欣欣以向荣泉涓涓而始流善万物之得时感吾生之行休已矣乎寓形宇内复几时曷不委心任去留胡为乎遑遑欲何之富贵非吾愿帝乡不可期怀良辰以孤往或植杖而耘耔登东皋以舒啸临清流而赋诗聊乘化以归尽乐夫天命复奚疑"
AddrDict = set()

def randName():
    FirstName = random.choice(FirstNameList)
    SecondName = "".join(random.choice(SecondNameList)
                         for i in range(random.randint(1, 2)))
    return FirstName + SecondName


def randAddr():
    AddrList = list(AddrDict)
    Addr = random.choice(AddrList)
    Addr = Addr.split("---")
    CityName = Addr[0]
    CountryList = Addr[1].split("|")
    Country = random.choice(CountryList)
    StreetName = "".join(random.choice(SecondNameList)
                         for i in range(random.randint(2, 3)))+"路"
    CommunityName = "".join(random.choice(textList)
                            for i in range(random.randint(2, 4))) + "社区"
    No = random.randint(1, 99)
    return "河南省" + CityName + Country + StreetName + CommunityName + str(No) + "号"


def randBirthday():
    year = random.randint(1997, 2001)
    month = random.randint(1, 12)
    day = random.randint(1, 27)
    birthday = "{}{:0>2d}{:0>2d}".format(year, month, day)
    return birthday


def randID():
    birth = randBirthday()
    prefixID = random.randint(400000, 411999)
    subfixID = random.randint(0000, 9999)
    IDCard = "{}{}{}".format(prefixID, birth, subfixID)
    return IDCard


def randPhone():
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    suffix = random.randint(9999999, 100000000)

    return "1{}{}{}".format(second, third, suffix)


def randPerson():
    name = randName()
    birth = randBirthday()
    personid = randID()
    phone = randPhone()
    addr = randAddr()
    info = "{},{},{},{},{}".format(name, birth, personid, phone, addr)
    return info

if __name__ == '__main__':
    with open("area.txt", encoding="utf-8") as fo:
        for line in fo.readlines():
            AddrDict.add(line.strip())
            pass
    for i in range(10):
        print(randPerson())