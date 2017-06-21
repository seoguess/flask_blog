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
#导入Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def mysql_get_value(sql, args, is_fetch):
    rt_cnt, rt_list = "", []
    conn = MySQLdb.connect(host="localhost", \
                           port=3306,\
                           user="shawn",\
                           passwd="huangdonghui",\
                           db="blog",\
                           charset='utf8')
    cursor = conn.cursor()
    rt_cnt = cursor.execute(sql, args)
    if is_fetch:
        rt_list = cursor.fetchall()
    else:
        conn.commit()
    cursor.close()
    conn.close()
    return rt_cnt, rt_list

SQL_recent_topic = "select id,title,url,tag,author,date,content from topic order by id desc limit 12"
SQL_recommond_list = "select title,url,date from topic where mark != 0 limit 3"
SQL_tag_url = 'select tagname,tagurl from taginfo where tagid =%s'
SQL_tag_url2 = 'select tagname,tagurl from taginfo where tagid in (%s)'
SQL_topic_view = 'select id,title,tag,author,date,content from topic where id=%s'
# SQL_prev_topic = 'SELECT title,url FROM topic WHERE id >= ((SELECT MAX(id) FROM topic)-(SELECT MIN(id) FROM topic)) * RAND() + (SELECT MIN(id) FROM topic)  LIMIT 2'
SQL_prev_topic = 'select title,url,id from topic order by rand() limit 2'

#创建一个Flask对象
app = Flask(__name__)
app.secret_key = "\xea\tR\xe8#\xa0\xbd\x95\xf44h\xce\xa4\xd6\xdf\x98I\xcb\xea\x15\xce\x83\x7f|k\r\xa6\xafWIY\x0f"
#关联数据库，初始化db
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "mysql://shawn:huangdonghui@localhost/blog"
db = SQLAlchemy(app)


#定义Post类
class Post(db.Model):  
    __tablename__='topic'  
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(80),unique=True)
    tag=db.Column(db.String(10))
    author=db.Column(db.String(80),default="无名小编")
    date=db.Column(db.DateTime)
    content=db.Column(db.Text)
    mark=db.Column(db.Integer,default=0)  


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SECRET_KEY'] = "random string"

# db = SQLAlchemy(app)

# class data(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(100))
#     content = db.Column(db.Text)
#     author = db.Column(db.String(20))

#     def __init__(self, title, content, author):
#         self.title = title
#         self.content = content
#         self.author = author

@app.route('/')
def show_all():
    blog_title = bloginfo.BLOG_WHOLE_TITLE
    blog_indro = bloginfo.BLOG_INDRO
    results = mysql_get_value(SQL_recent_topic,(),True)[1]
    columns = ("id", "title", "url", "tag", "author", "date","content")
    cnt = [ dict(zip(columns, result)) for result in results ]

    for i in cnt:
        if i.get('tag'):
            if "," not in i.get('tag'):
                i['tag_count'] = 0
                i['tag_info'] = mysql_get_value(SQL_tag_url,(i.get('tag')),True)[1][0]
            # i['tag_info'],
            # print mysql_get_value(SQL_recent_topic,(),True)[1]
            # print (i.get('tag')),"hah"
            else:
                i['tag_count'] = 1
                conn = MySQLdb.connect(host="localhost", \
                                       port=3306,\
                                       user="shawn",\
                                       passwd="huangdonghui",\
                                       db="blog",\
                                       charset='utf8')
                cursor = conn.cursor()
                rt_cnt = cursor.execute(SQL_tag_url2 % i.get('tag'))
                rt_list = cursor.fetchall()
                cursor.close()
                conn.close()

                i['tag_info'] = rt_list


    recommonds = mysql_get_value(SQL_recommond_list,(),True)[1]
    recommonds_list = [ dict(zip(("title", 'url', 'date'),recommond)) for recommond in recommonds ]
    pagination=Post.query.paginate(1,per_page=1,error_out=False)
    posts=pagination.items
    return render_template('index.html', blog_title = blog_title, blog_indro = blog_indro, cnt=cnt, r_list = recommonds_list,pagination=pagination,posts = posts)

# @app.route('/add', methods = ['GET', 'POST'])
# def new():
#     if request.method == 'POST':
#         if not request.form['title'] or not request.form['content']:
#             flash('Please enter all the fields', 'error')
#         else:
#             content = data(request.form['title'], request.form.get('content'), request.form.get('author', 'Shawn'))
#             db.session.add(content)
#             db.session.commit()
#             flash('Record was successfully added')
#             return redirect(url_for('show_all'))
#     return render_template('add.html')

# @app.route('/edit/<int:uid>', methods = ['GET', 'POST'])
# def edit(uid):
#     if request.method == 'POST':
#         if not request.form['title'] or not request.form['content']:
#             flash('Please enter all the fields', 'error')
#         else:
#             edit_content = data.query.get(uid)
#             if request.form.get('delete') == 'delete':
#                 db.session.delete(edit_content)
#                 db.session.commit()
#                 flash('Remove was successfully')
#             else:
#                 edit_content.title = request.form['title']
#                 edit_content.content = request.form['content']
#                 edit_content.author = request.form['author']
#                 db.session.commit()
#                 flash('Edit was successfully')
#             return redirect(url_for('show_all'))
#     return render_template('edit.html', edit_content = data.query.get(uid))


@app.route('/topic/<int:id>.html')
def topic_view(id):
    results = mysql_get_value(SQL_topic_view,(str(id)),True)[1][0]
    columns = ("id","title", "tag", "author", "date","content")
    cnt = dict(zip(columns, results))
    prev_results = mysql_get_value(SQL_prev_topic,(),True)[1]
    return render_template('file.html', cnt_id = id, cnt = cnt, prevs = prev_results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8003)
