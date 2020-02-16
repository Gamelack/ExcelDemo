from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
#
# # 连接数据库
# engine = create_engine('mysql://root:123456@localhost:3306/excelDemo?charset=utf8')
# ## 编码问题
#
# # # 获取基类
# Base = declarative_base()

class 章节():  # 继承基类
    __tablename__ = '章节'
    章节id = Column(Integer, primary_key=True)
    章节名称 = Column(String(200))
    录入时间 = Column(DateTime)
class 指标():  # 继承基类
    __tablename__ = '指标'
    指标id = Column(Integer, primary_key=True)
    指标名称 = Column(String(200))
    指标内容 = Column(String(200))
    上级指标id = Column(Integer)
    所属章节 = Column(Integer, nullable=False,unique=True)
    指标说明 = Column(String(1024))
    录入时间 = Column(DateTime)
class 具体要求():  # 继承基类
    __tablename__ = '具体要求'
    要求id = Column(Integer, primary_key=True)
    所属指标 = Column(Integer)
    医院等级 = Column(String(200))
    要求数量 = Column(Integer)
    要求内容类型 = Column(String(200))
class 具体内容():  # 继承基类
    __tablename__ = '具体内容'
    内容id = Column(Integer, primary_key=True)
    所属指标id = Column(Integer)
    具体内容 = Column(String(200))
    录入时间 = Column(DateTime)

class DataModle():  # 继承基类
    __tablename__ = 'students1'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(20))
    name = Column(String(20), nullable=False)
    sex = Column(String(1))
    in_time = Column(DateTime)
    is_vaild = Column(Boolean)
    idcard = Column(Integer, unique=True)
#
#
# DataModle.metadata.create_all(engine)  # 创建表格
#
# ## 新增数据
# from sqlalchemy.orm import sessionmaker
#
# Session = sessionmaker(bind=engine)
#
#
# class OrmTest(object):
#     def __init__(self):
#         self.session = Session()
#
#     def add_one(self):
#         new_obj = DataModle(
#             nickname='123',
#             name='321',
#             sex='男',
#         )
#         self.session.add(new_obj)
#         self.session.commit()
#         return new_obj
#
#     def add_more(self):
#         new_obj = DataModle(
#             nickname='123',
#             name='321',
#             sex='男',
#         )
#         new_obj2 = DataModle(
#             nickname='wei',
#             name='lai',
#             sex='女',
#         )
#         self.session.add_all([new_obj,
#                               new_obj2])
#         self.session.commit()
#         return new_obj
#
#     ## 查询数据
#     def get_one(self):
#         return self.session.query(DataModle).get(10)  # get 是选id为2的
#
#     def get_more(self):
#         return self.session.query(DataModle).filter_by(is_vaild=True)
#
#     ## 修改数据
#     ## 将一条当作多条的一种情况
#     def update_data(self):
#         data_list = self.session.query(DataModle).filter(DataModle.id >= 5)
#         for item in data_list:
#             if item:
#                 item.is_vaild = 0
#                 self.session.add(item)  # 加入
#         self.session.commit()  # 提交
#
#     ## filter 与 filter_by 的区别
#
#     ## 删除数据
#     def delete_data(self):
#         data = self.session.query(DataModle).get(8)
#         if data:
#             self.session.delete(data)
#             self.session.commit()
#         else:
#             return False
#
#     def delete_data_more(self):
#         delete_list = self.session.query(DataModle).filter(DataModle.id <= 5)
#         for item in delete_list:
#             if item:
#                 self.session.delete(item)
#             else:
#                 return False
#         self.session.commit()
#
#
# def main():
#     obj = OrmTest()
#     obj.add_one()
#     obj.add_more()
#
#     data = obj.get_one()
#
#     ## 防止查询失误
#     if data:
#         print('ID:{0}  {1}'.format(data.id, data.sex))
#     else:
#         print('Not exist')
#
#     data_more = obj.get_more()
#     print(data_more.count())  # 计数
#     for new_obj in data_more:
#         print('ID:{0}  {1} {2} {3}'.format(new_obj.id, new_obj.sex, new_obj.name, new_obj.nickname))
#
#     obj.update_data()
#     print('数据修改成功')
#
#     obj.delete_data()
#     print('数据删除成功')
#
#     obj.delete_data_more()
#
#
# # if __name__ == '__main__':
# #     main()