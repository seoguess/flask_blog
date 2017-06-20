#coding:utf-8

#从flask包导入Flask对象
from flask import Flask
#导入模板，需要新建一个templates文件夹
from flask import render_template
#用来获取get请求的参数
from flask import request
#导入跳转模块
from flask import redirect
#导入session
from flask import session
#导入基础配置项文件
import bloginfo
#导入MySQLdb
import MySQLdb


import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


#创建一个Flask对象
app = Flask(__name__)
app.secret_key = "\xea\tR\xe8#\xa0\xbd\x95\xf44h\xce\xa4\xd6\xdf\x98I\xcb\xea\x15\xce\x83\x7f|k\r\xa6\xafWIY\x0f"


@app.route('/')
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8001)
