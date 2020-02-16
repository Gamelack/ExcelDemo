import numpy as np
import pandas as pd
import re
import time


class 章节:
    "这是Student类的说明"  # __doc__

    objCount = 0  # 类的静态变量

    def __init__(self, 章节id, 章节名称, 起始行索引, 结束列索引, 录入时间):  # 构造函数，创建类的实例调用
        self.章节id = 章节id
        self.章节名称 = 章节名称
        self.起始行索引 = 起始行索引
        self.结束列索引 = 结束列索引
        self.录入时间 = 录入时间

    def __init__(self):  # 构造函数，创建类的实例调用
        self.章节id = None
        self.章节名称 = None
        self.起始行索引 = None
        self.结束列索引 = None
        self.录入时间 = None


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
        # 2.获取章节的信息
        # 章信息 = df[df[0].str.contains('第.{1,4}章', case=False, flags=0, na=np.nan, regex=True)]
        # for i in 章信息.index.tolist():
        #     zj = 章节()
        #     zj.起始行索引 = i
        #     zj.录入时间 = time.localtime(time.time())
        #     zj.章节名称 = df.iloc[i, 0]
            # prn_obj(zj)

        # 3.去除第三列为空的行(章节名也被去掉)
        # df = df.dropna(subset=[3])
        # print(df[0:20])

        # 4.指标操作：获取到前三列中的指标数据；获取第四列的指标描述
        # print(df[[0,1,2]].values)
        for index, row in df.iterrows():
            # 清除前三列中数字字符
            self.clearStartByChineseDigital(row, 0)
            self.clearStartByChineseDigital(row, 1)
            self.clearStartByChineseDigital(row, 2)
            if  self.is章节(row[0]):
                print(self.is章节(row[0]).group())
                continue
            # # 获取指标的描述
            # print(str(row[0])+"-"+str(row[1])+"-"+str(row[2])+"-" + '\n\n')
            if isinstance(row[3],str):
                rowCloumn3 = self.clearSpace(row[3])
                # 获取指标描述
                desc = self.getIndicatorsDescription(rowCloumn3[0])
                print("指标描述："+desc)
                for subRow3 in rowCloumn3:
                    temp = self.isRequestDetails(subRow3)
                    if temp:
                        print("具体实现条款：" + temp.group())
                    temp = self.getLevelRequir(subRow3)
                    if temp:
                        print("各级医院要求："+temp.group())

        # else:
        #     print(row[0] + "\t" + row[1] + "\t" + row[2] + "\t" + row[3])

    def clearSpace(self, s):
        '''去除空格、换行、制表符，然后去掉最后一个字符（“。”），再按“。”进行分割，获取到一个指标具体内容和要求的数组'''
        print(s)
        return re.split(r'。', re.sub('\s', '', s)[:-1])
    def clearStartByChineseDigital(self, row, index):
        '''删除开头序号标注：“23、为人民服务”变成“为人民服务”'''
        if len(row)<=index or not isinstance(row[index],str) :
            return '';
        b = re.compile(r'^[一二三四五六七八九十1234567890\n()（）、]*')  # 编译正则表达式
        row[index] = b.sub(r'', row[index])
        return row[index]

    def is章节(self,s):
        result = re.match(r'第[一二三四五六七八九十1234567890].{1,4}.+', s)
        return result
    def getIndicatorsDescription(self, s):
        '''获取指标描述'''
        if self.isRequestDetails(s) is None:
            return s
        else:
            return ''
    def isRequestDetails(self, s):
        '''要求的具体条款'''
        if isinstance(s,str):
            return ''
        result = re.match(r'[①②③④⑤⑥⑦⑧⑨⑩)].+|.{0,3}具备.+|.{0,3}支持.+|.{0,3}提供.+|.{0,3}支持.+', s)
        return result
    def getLevelRequir(self,s):
        '''匹配是否是医院级别要求'''
        result = re.match(r'^[一二三四五六七]级.+', s)
        return result

    def 测试数据(self):
        aaa = np.random.uniform(1, 1000, 3000)
        bbb = np.random.uniform(1, 1000, 3000)
        ccc = np.random.uniform(1, 1000, 3000)
        ddd = np.random.uniform(1, 1000, 3000)
        return pd.DataFrame({'aaa': aaa, 'bbb': bbb, 'ccc': ccc, 'ddd': ddd, 'eee': None})


temp = CleanData()

temp.clean()
