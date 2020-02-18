import numpy as np
import pandas as pd
import re
from math import isnan


class 章节与一级指标(object):
    def __init__(self):  # 构造函数，创建类的实例调用
        self.章节与一级指标字典 = {}


class 一级指标与二级指标(object):
    def __init__(self, ):  # 构造函数，创建类的实例调用
        self.一级与二级指标字典 = {}


class 二级与三级指标(object):
    def __init__(self, ):  # 构造函数，创建类的实例调用
        self.二级与三级指标字典 = {}


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
        # 1：读取指定行
        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)
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
            if row.isna()[3]:
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
            # print(str(date.章节与一级指标字典[章节名称][row[0]][row[1]]))
            # print('\t\t\t'+str(date.章节与一级指标字典[章节名称][row[0]][row[1]][row[2]].三级指标名称))
            # print('\t\t\t\t' + str(date.章节与一级指标字典[章节名称][row[0]][row[1]][row[2]].指标描述))
            # print('\t\t\t\t' + str(date.章节与一级指标字典[章节名称][row[0]][row[1]][row[2]].指标细则列表))
            # print('\t\t\t\t' + str(date.章节与一级指标字典[章节名称][row[0]][row[1]][row[2]].医院等级要求列表))
            # print('\n')
        a = date.__dict__.keys()
        for b in a:
            # print("1"+b)
            c =date.__dict__[b].keys()
            for d in c:
                # print('\t2.'+d)
                e = date.__dict__[b][d].keys()
                for f in e:
                    # print('\t\t3.'+f)
                    g = date.__dict__[b][d][f].keys()
                    for h in g:
                        print('\t\t\t4.' + h)
                        i = date.__dict__[b][d][f][h]
                        print(i)


        # self.printObj(date)
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

    def 测试数据(self):
        aaa = np.random.uniform(1, 1000, 3000)
        bbb = np.random.uniform(1, 1000, 3000)
        ccc = np.random.uniform(1, 1000, 3000)
        ddd = np.random.uniform(1, 1000, 3000)
        return pd.DataFrame({'aaa': aaa, 'bbb': bbb, 'ccc': ccc, 'ddd': ddd, 'eee': None})

    def printObj(self, obj,*countSpaceList):
        if isinstance(obj, int):
            for i in obj:
                print(i + "\t" + self.printObj(obj[i]))
        if isinstance(obj, list):
            for i in obj:
                print(i + "\t" + self.printObj(obj[i]))
        if isinstance(obj, tuple):
            for i in obj:
                print(i + "\t" + self.printObj(obj[i]))
        if isinstance(obj, dict):
            for i in obj:
                print(i+"\t"+self.printObj(obj[i]))
        if isinstance(obj, str):
            print(obj)
        else:
            ls = obj.__dir__()
            for i in ls:
                if isinstance(i, str):
                    b = re.match(r'__.+', i)
                    if not b:
                        print(i,end='')
                else:
                    if countSpaceList:
                        lenth=0
                    else:
                        lenth = countSpaceList[0]
                    for ll in lenth:
                        print('\t',end='')
                    prn_obj(i,lenth+1)
        print('')




temp = CleanData()

temp.clean()
