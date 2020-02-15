import numpy as np
import pandas as pd
import re
import time


class 章节:
    "这是Student类的说明"  # __doc__

    objCount = 0  # 类的静态变量

    def __init__(self, 章节id, 章节名称,起始行索引,结束列索引,录入时间):  # 构造函数，创建类的实例调用
        self.章节id = 章节id
        self.章节名称 = 章节名称
        self.起始行索引 = 起始行索引
        self.结束列索引 =结束列索引
        self.录入时间 = 录入时间

    def __init__(self):  # 构造函数，创建类的实例调用
        self.章节id = None
        self.章节名称 = None
        self.起始行索引 = None
        self.结束列索引 = None
        self.录入时间 = None
def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()])+"\n")
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
        章信息 = df[df[0].str.contains('第.{1,4}章', case=False, flags=0, na=np.nan, regex=True)]
        for i in 章信息.index.tolist():
            zj = 章节()
            zj.起始行索引 = i
            zj.录入时间 = time.localtime(time.time())
            zj.章节名称 = df.iloc[i,0]
            # prn_obj(zj)

        # 3.去除第三列为空的行(章节名也被去掉)
        df = df.dropna(subset=[3])
        # print(df[0:20])
        # 4.获取到前三列：指标数据
        # print(df[[0,1,2]].values)
        for index, row in df.iterrows():
            b = re.compile(r'[一二三四五六七八九十\n()（）、]*')

            if index>3:
                row0=b.sub(r'', row[0])
                row1=b.sub(r'', row[1])
                row2=b.sub(r'', row[2])
                print(row1 + '\n\n')
            else:
                print(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3])

    def 测试数据(self):
        aaa = np.random.uniform(1, 1000, 3000)
        bbb = np.random.uniform(1, 1000, 3000)
        ccc = np.random.uniform(1, 1000, 3000)
        ddd = np.random.uniform(1, 1000, 3000)
        return pd.DataFrame({'aaa': aaa, 'bbb': bbb, 'ccc': ccc, 'ddd': ddd, 'eee': None})

temp = CleanData()

temp.clean()
