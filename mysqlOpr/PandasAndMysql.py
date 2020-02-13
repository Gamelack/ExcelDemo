import numpy as np
import pandas as pd


class Test1():
    def test1(self):
        '''一维数据组'''
        s = pd.Series([1, 2, 5, np.nan, 6, 8])
        print(s)

    def test2(self):
        '''创建一个 DateFrame(二位数据表)'''
        # 创建日期索引序列
        dates = pd.date_range('20130101', periods=6)
        print(type(dates))
        print(dates)
        print('--------------------------------------------------------------------')
        # 创建Dataframe，其中 index 决定索引序列，columns 决定列名
        df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
        print(df)

    def test3(self):
        '''字典创建 DataFrame'''
        df2 = pd.DataFrame({'A': 1.,
                            'B': pd.Timestamp('20130102231214'),
                            'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                            'D': np.array([3] * 4, dtype='int32'),
                            'E': pd.Categorical(["test", "train", "test", "train"]),
                            'F': 'foo'})
        print(df2)


class Test2():
    def test1(self):
        df = pd.read_excel('2018全国医院信息化建设标准与规范(试行).xls')  # 这个会直接默认读取到这个Excel的第一个表单
        data = df.head()  # 默认读取前5行的数据
        print("获取到所有的值:\n{0}".format(data))  # 格式化输出

    def test2(self):
        # 方法二：通过指定表单名的方式来读取
        df = pd.read_excel('2018全国医院信息化建设标准与规范(试行).xls',
                           sheet_name='Sheet1')  # 可以通过sheet_name来指定读取的表单
        data = df.head()  # 默认读取前5行的数据
        print("获取到所有的值:\n{0}".format(data))  # 格式化输出
    def test3(self):
        # 方法三：通过表单索引来指定要访问的表单，0表示第一个表单
        # 也可以采用表单名和索引的双重方式来定位表单
        # 也可以同时定位多个表单，方式都罗列如下所示
        df = pd.read_excel('2018全国医院信息化建设标准与规范(试行).xls', sheet_name=['Sheet1', 'Sheet2'])  # 可以通过表单名同时指定多个
        # df=pd.read_excel('lemon.xlsx',sheet_name=0)#可以通过表单索引来指定读取的表单
        # df=pd.read_excel('lemon.xlsx',sheet_name=['python',1])#可以混合的方式来指定
        # df=pd.read_excel('lemon.xlsx',sheet_name=[1,2])#可以通过索引 同时指定多个
        data = df.values()  # 获取所有的数据，注意这里不能用head()方法哦~
        print("获取到所有的值:\n{0}".format(data))  # 格式化输出
class Test3():
    def test1(self):
        # 1：读取指定行
        df = pd.read_excel('2018全国医院信息化建设标准与规范(试行).xls')  # 这个会直接默认读取到这个Excel的第一个表单
        data = df.iloc[0].values  # 0表示第一行 这里读取数据并不包含表头，要注意哦！
        print("读取指定行的数据：\n{0}".format(data))
        print('\n-------------------------------------------------------------------------')
        data = df.iloc[[1, 2]].values  # 读取指定多行的话，就要在ix[]里面嵌套列表指定行数
        print("读取指定行的数据：\n{0}".format(data))
temp = Test3()
temp.test1()
