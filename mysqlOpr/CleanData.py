import numpy as np
import pandas as pd
import re
from math import isnan


class 章节与一级指标(object):
    def __init__(self):  # 构造函数，创建类的实例调用
        self.章节与一级指标字典 = {}


# class 一级指标与二级指标(object):
#     def __init__(self, ):  # 构造函数，创建类的实例调用
#         self.一级与二级指标字典 = {}
#
#
# class 二级与三级指标(object):
#     def __init__(self, ):  # 构造函数，创建类的实例调用
#         self.二级与三级指标字典 = {}


class 三级与细则(object):
    def __init__(self):  # 构造函数，创建类的实例调用
        self.三级指标名称 = ''
        self.指标描述 = ''
        self.指标细则列表 = []
        self.医院等级要求列表 = []


def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]) + "\n")



class CleanData:
    def clean(self):
        #设置打印数据参数
        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)
        # 1：读取指定行

        df = pd.read_excel('2018全国医院信息化建设标准与规范(试行).xls', header=None)  # 这个会直接默认读取到这个Excel的第一个表单
        # 1.前三列填充数据
        df[[0, 1, 2]] = df[[0, 1, 2]].ffill()
        # 4.指标操作：获取到前三列中的指标数据；获取第四列的指标描述
        # print(df[[0,1,2]].values)
        date = 章节与一级指标()
        章节名称 = ''
        for index, row in df.iterrows():
            # 清除前三列中数字字符
            self.clearStartByChineseDigital(row, 0)
            self.clearStartByChineseDigital(row, 1)
            self.clearStartByChineseDigital(row, 2)
            章节判断 = self.is章节(row[0])
            if 章节判断:
                if not date.章节与一级指标字典.keys().__contains__(章节判断.group()):
                    # 添加章节名
                    date.章节与一级指标字典[章节判断.group()] = {}
                    章节名称 = 章节判断.group()
            #判断第四列这个单元格是否是空项
            if row.isna()[1] or row.isna()[2] or row.isna()[3]:
                continue
            # 添加一级指标
            if not date.章节与一级指标字典[章节名称].keys().__contains__(row[0]):
                date.章节与一级指标字典[章节名称][row[0]] = {}
            # 添加二级指标
            if not date.章节与一级指标字典[章节名称][row[0]].keys().__contains__(row[1]):
                date.章节与一级指标字典[章节名称][row[0]][row[1]] = {}
            # 添加三级指标，并新建三级指标对应对象
            三级 = 三级与细则()
            if not date.章节与一级指标字典[章节名称][row[0]][row[1]].keys().__contains__(row[2]):
                date.章节与一级指标字典[章节名称][row[0]][row[1]][row[2]] = 三级
            三级.三级指标名称 = row[2]
            if isinstance(row[3], str):
                rowCloumn3 = self.clearSpace(row[3])
                # 指标描述判断，默认取第一条
                desc = self.getIndicatorsDescription(rowCloumn3)
                三级.指标描述 = desc

                # 获取细则列表：list
                indicatorsList = self.getIndicatorsList(rowCloumn3)
                三级.指标细则列表 = indicatorsList

                # 获取医院级别要求：list
                leveHosReqList = self.getHospitalRequireList(rowCloumn3)
                三级.医院等级要求列表 = leveHosReqList


        #遍历输出自定义类对象
        self.printObj(date,0,True)
        # self.spliteReqireContent(date)
    #
    def clearSpace(self, s):
        '''去除空格、换行、制表符，然后去掉最后一个字符（“。”），再按“。”进行分割，获取到一个指标具体内容和要求的数组'''
        return re.split(r'。', re.sub('\s', '', s)[:-1])

    def clearStartByChineseDigital(self, row, index):
        '''删除开头序号标注：“23、为人民服务”变成“为人民服务”'''
        if len(row) <= index or not isinstance(row[index], str):
            return None
        b = re.compile(r'^[一二三四五六七八九十1234567890\n()（）、]*')  # 编译正则表达式
        row[index] = b.sub(r'', row[index])
        return row[index]

    def is章节(self, s):
        '''判断是否是章节名称'''
        result = re.match(r'第[一二三四五六七八九十1234567890].{1,4}.+', s)
        return result

    def getIndicatorsDescription(self, s):
        '''获取指标描述'''
        index = 0
        for clomunIndex in range(len(s)):
            # 指标描述判断，默认取第一条
            temp = self.isRequestDetails(s[clomunIndex])
            if temp:
                index = clomunIndex
                break
        descStr = ''
        for i in range(index):
            descStr = descStr + s[i] + "。"
        return descStr

    def getIndicatorsList(self, s):
        '''获取指标条目'''
        startIndex = 0
        for clomunIndex in range(len(s)):
            # 指标描述判断，默认取第一条
            temp = self.isRequestDetails(s[clomunIndex])
            if temp:
                startIndex = clomunIndex
                break
        endIndex = len(s)
        for clomunIndex in range(len(s)):
            # 指标描述判断，默认取第一条
            temp = self.getLevelRequire(s[clomunIndex])
            if temp:
                endIndex = clomunIndex
                break
        list = []
        for i in range(startIndex, endIndex):
            list.append(s[i])
        return list

    def getHospitalRequireList(self, s):
        '''获取指标条目'''
        startIndex = 0
        for clomunIndex in range(len(s)):
            # 指标描述判断，默认取第一条
            temp = self.getLevelRequire(s[clomunIndex])
            if temp:
                startIndex = clomunIndex
                break

        endIndex = len(s)
        for clomunIndex in range(len(s)):
            # 指标描述判断，默认取第一条
            temp = self.getLevelRequire(s[clomunIndex])
            if temp:
                endIndex = clomunIndex
        list = []
        for i in range(startIndex, endIndex):
            list.append(s[i])
        return list

    def isRequestDetails(self, s):
        '''文本是否是具体的条款'''
        if not isinstance(s, str):
            return None
        result = re.match(r'[①②③④⑤⑥⑦⑧⑨⑩)].+|.{0,3}具备.+|.{0,3}提供.+', s)
        return result

    def getLevelRequire(self, s):
        '''匹配是否是医院级别要求'''
        result = re.match(r'^[一二三四五六七八九十]级.+', s)
        return result
    def spliteReqireContent(self,date):
        keys1 = date.章节与一级指标字典.keys()
        for key1 in keys1:
            # print(key1)
            keys2 = date.章节与一级指标字典[key1].keys()
            for key2 in keys2:
                # print("\t"+key2)
                keys3 = date.章节与一级指标字典[key1][key2].keys()
                for key3 in keys3:
                    # print("\t"+"\t"+key3)
                    keys4 = date.章节与一级指标字典[key1][key2][key3].keys()
                    for key4 in keys4:
                        print("\t"+"\t"+"\t"+key4)
                        values = date.章节与一级指标字典[key1][key2][key3][key4].__dict__
                        for value in values:
                            print("\t"+"\t"+"\t"+"\t"+str(value)+":"+str(date.章节与一级指标字典[key1][key2][key3][key4].__dict__[value]))
    def statisticalFrequency(self,list):
        '''统计字符串列表中开头，结尾，或其他地方频率最高的词语'''

    def printObj(self, obj,countSpace=0,showFiledName=False):
        '''输出所有数据类型的字段值'''
        pd.set_option('display.max_columns', 4000)
        pd.set_option('display.width', 4000)
        pd.set_option('display.max_colwidth', 8000)
        if countSpace is None or countSpace<=0:
            countSpace=0
        space=''
        for i in range(countSpace):
            space=space+'\t'
        if isinstance(obj, (str,int)):
            print(space, end='')
            print(str(obj))
        elif isinstance(obj, (list,tuple,set)):
            for i in obj:
                self.printObj(i,countSpace)
        elif isinstance(obj,dict):
            keys = obj.keys()
            for key in keys:
                self.printObj(key, countSpace)
                self.printObj(obj[key], countSpace+1)
        # 如果是类对象
        elif isinstance(obj,object):
            # print(dir(obj))#所有字段、方法名等名称
            # print(obj.__dir__())#所有字段、方法名等名称
            # print(obj.__dict__.items())
            for key in dir(obj):
                isOK = re.match(r'__.+', key)
                if hasattr(obj, key) and not isOK:  # 检查实例是否有这个属性
                    if showFiledName:
                        print(space+str(key),end=':')
                    # self.printObj(str(key) ,countSpace)
                    self.printObj(getattr(obj, key), countSpace+1)

temp = CleanData()

temp.clean()

# test1()
print('\t'+'over')