from django.apps import AppConfig
import pymysql


class MysqloprConfig(AppConfig):
    name = 'mysqlOpr'
    def connect(self):
        db = pymysql.connect(host="数据库地址",
                             user="用户名",
                             password="密码",
                             port="端口",
                             database="数据库名",
                             charset='utf8')
