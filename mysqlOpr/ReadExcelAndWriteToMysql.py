import pymysql
import xlrd

# import importlib
# importlib.reload(sys) #出现呢reload错误使用

'''
如果插入失败，有可能是：
1.字符串或表、连接的编码不统一
2.数据库编码与上述不统一
SHOW VARIABLES LIKE 'character%';
SET character_set_database=utf8;
'''


def open_excel():
    try:
        book = xlrd.open_workbook("2018全国医院信息化建设标准与规范(试行).xls")  # 文件名，把文件与py文件放在同一目录下
    except:
        print("open excel file failed!")
    try:
        sheet = book.sheet_by_name("Sheet1")  # execl里面的worksheet1
        return sheet
    except:
        print("locate worksheet in excel failed!")


def connectMysql():
    db = None
    # 连接数据库
    db = pymysql.connect(host="127.0.0.1", user="root",
                         password="123456",
                         database="exceldemo",
                         charset='utf8',
                         port=3306
                         )
    return db


def search_count():
    db = connectMysql()
    if db:
        cursor = db.cursor()
        select = "select count(id) from excel数据"  # 获取表中xxxxx记录数
        cursor.execute(select)  # 执行sql语句
        line_count = cursor.fetchone()
        print(line_count[0])


def insert_deta():
    db = connectMysql()
    if db:
        sheet = open_excel()
        cursor = db.cursor()
        for i in range(1, sheet.nrows):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            for j in range(1, sheet.ncols):
                date1 = sheet.cell(i, j).value  # 取第i行第j列
                # date1=date1.encode("utf8").decode("utf8")
                value = (i, j, str(date1))
                if date1:
                    print("if:" + str(value))
                    sql = "INSERT INTO excel数据(横坐标,纵坐标,数据) VALUES(%s,%s,%s)"
                    cursor.execute(sql, value)  # 执行sql语句
                    db.commit()
                else:
                    print('else:' + str(value))
                    continue

        cursor.close()  # 关闭连接
        db.close()


insert_deta()

# 关闭数据
print("ok ")
