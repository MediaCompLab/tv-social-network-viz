import json
from flask import Flask, g, current_app, render_template, abort, request, jsonify, send_from_directory
# import  config
import os
from utils.ext import db
from flask_cors import CORS
from model import *
from utils.sqlite import SQLiteHelper
import os
from utils.dbini import datainit
from flask_migrate import Migrate
from utils.generate_token import login_required, get_user_id, generate_token, verify_token

from utils.graph import get_graph_diff

app = Flask(__name__)
app.config.from_pyfile('config.py')
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录
UPLOAD_FOLDER = basedir + '/upload'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print(app.config['SECRET_KEY'])
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CORS(app, resources=r'/*', supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'big.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
mydb = SQLiteHelper(os.path.join(BASE_DIR, 'big.db'))
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        sql = "select count(1)cnt from t_user where  username=? and password=?"
        res = mydb.get_one(sql, (username, password))
        print(res)
        if int(res[0]) > 0:
            sql = "select id from t_user where  username=? and password=?"
            res = mydb.get_all(sql, (username, password))
            user_id = res[0][0]
            with app.app_context():
                token = generate_token(user_id).decode()
            return jsonify({'code': 200, 'token': token})
        else:
            return jsonify({'code': 305})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', )
        password = request.form.get('password', )
        print(username, password)
        sql = 'select count(1)cnt from t_user where username=?'
        result = mydb.get_one(sql, (username,))
        print(result)
        if int(result[0]) > 0:
            message = '用户已存在请重新注册'
            return jsonify({'code': 305, 'msg': message})
        else:
            sql = 'insert into t_user(username,password) values(?,?)'
            mydb.create(sql, (username, password))
            message = '用户注册成功请登录'
            return jsonify({'code': 200, 'msg': message})


@app.route('/uploadfiles', methods=['GET', 'POST'])
@login_required
def uploadfiles():
    if request.method == 'POST':
        try:
            file = request.files.get('file')
            print(file)
            submituser = request.form.get('submituser', '')
            print('提交用户', submituser)
            return jsonify({'code': 0, 'msg': '传入成功'})
        except:
            return jsonify({'code': 100, 'msg': '导入失败'})


@app.route('/uploadfile', methods=['GET', 'POST'])
@login_required
def uploadfile():
    if request.method == 'POST':
        try:
            file = request.files.get('file')
            print(file)
            upload_file = request.files['file']
            task = request.form.get('identifier')  # 获取文件唯一标识符
            chunk = request.form.get('chunkNumber')  # 获取该分片在所有分片中的序号
            filename = '%s%s' % (task, chunk)  # 构成该分片唯一标识符
            local_package_root = app.config['UPLOAD_FOLDER']
            upload_file.save(os.path.join(local_package_root, filename))
            return jsonify({'code': 0, 'msg': '传入成功'})
        except:
            return jsonify({'code': 100, 'msg': '导入失败'})
    else:
        local_package_root = app.config['UPLOAD_FOLDER']
        task = request.args.get('identifier')  # 获取文件唯一标识符
        chunk = request.args.get('chunkNumber')  # 获取该分片在所有分片中的序号
        filename = '%s%s' % (task, chunk)  # 构成该分片唯一标识符
        chunk_file = os.path.isfile(os.path.join(local_package_root, filename))
        if chunk_file:
            return jsonify({'skipUpload': 'yes'})
        else:
            return jsonify({'skipUpload': ''})


@app.route('/mergefile', methods=['GET', 'POST'])
@login_required
def mergefile():
    if request.method == 'GET':
        try:
            batchno = request.args.get('batchno')
            name = request.args.get('name')
            local_package_root = app.config['UPLOAD_FOLDER']
            task = request.args.get('uniqueIdentifier')  # 获取文件唯一标识
            target_file = os.path.join(local_package_root, name)
            print(batchno, name, local_package_root, target_file)
            chunk = 1  # 分片序号
            with open(target_file, 'wb') as target:  # 创建新文件
                while True:
                    try:
                        filename = os.path.join(local_package_root, '%s%s' % (task, chunk))
                        # print('是否是文件',filename,os.path.isfile(filename))
                        source_file = open(filename, 'rb')  # 按序打开每个分片
                        target.write(source_file.read())  # 读取分片内容写入新文件
                        source_file.close()
                    except IOError:
                        break
                    chunk += 1
                    print('打印文件', filename)
                    os.remove(filename)  # 删除该分片，节约空间
            print('合并成功')
            datainit(name, batchno)
            return jsonify({'code': 200, 'msg': '传入成功数据库成功写入'})
        except:
            return jsonify({'code': 305, 'msg': '导入失败'})


@login_required
@app.route('/download/<name>', methods=['GET', 'POST'])
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/apifirstnode', methods=['GET', 'POST'])
@login_required
def apifirstnode():
    sql = """select distinct  batchno from big"""
    result = mydb.get_all(sql)
    result = [dict(name=i[0], isleaf=0, title=i[0], relate=f'{i[0]}') for i in result]
    return jsonify(result)


@app.route('/apisecnode', methods=['GET', 'POST'])
@login_required
def apisecnode():
    if request.method == 'POST':
        batchno = request.form.get('batchno', '')
        print(batchno)
        sql = """select distinct  season from big where batchno=?"""
        result = mydb.get_all(sql, (batchno,))
        result = [dict(name=i[0], isleaf=0, title='season--' + str(i[0]), relate=f'{batchno}--{i[0]}') for i in result]
        print(result)
        return jsonify(result)


@app.route('/apithrnode', methods=['GET', 'POST'])
@login_required
def apithrnode():
    if request.method == 'POST':
        batchno = request.form.get('batchno', '')
        season = request.form.get('season', '')
        sql = """select distinct  episode from big where batchno=? and season=?"""
        result = mydb.get_all(sql, (batchno, season))
        result = [dict(name=i[0], isleaf=0, title='episode--' + str(i[0]), relate=f'{batchno}--{season}--{i[0]}') for i
                  in result]
        print(result)
        return jsonify(result)


@app.route('/apifounode', methods=['GET', 'POST'])
@login_required
def apifounode():
    if request.method == 'POST':
        batchno = request.form.get('batchno', '')
        season = request.form.get('season', '')
        episode = request.form.get('episode', '')
        sql = """select distinct  scene from big where batchno=? and season=? and episode=?"""
        result = mydb.get_all(sql, (batchno, season, episode))
        result = [
            dict(name=i[0], isleaf=0, title='scene--' + str(i[0]), relate=f'{batchno}--{season}--{episode}--{i[0]}') for
            i in result]
        print(result)
        return jsonify(result)


@app.route('/apifivnode', methods=['GET', 'POST'])
@login_required
def apifivnode():
    if request.method == 'POST':
        batchno = request.form.get('batchno', '')
        season = request.form.get('season', '')
        episode = request.form.get('episode', '')
        scene = request.form.get('scene', '')
        sql = """select distinct  line from big where batchno=? and season=? and episode=? and scene=?"""
        result = mydb.get_all(sql, (batchno, season, episode, scene))
        result = [dict(name=i[0], isleaf=1, title='line--' + str(i[0]),
                       relate=f'{batchno}--{season}--{episode}--{scene}--{i[0]}') for i in result]
        print(result)
        return jsonify(result)


@app.route('/apidraw', methods=['GET', 'POST'])
@login_required
def apidraw():
    if request.method == 'POST':
        # 后端可以获取数据
        print(request.form)
        relate0 = request.form.get('0[relate]', '')
        relate1 = request.form.get('1[relate]', '')
        print('apidraw', relate0, relate1)
        # split relate to get the data
        relate0_ref = relate0.split('--')
        relate1_ref = relate1.split('--')
        print('apidraw', relate0_ref, relate1_ref)
        # read data from database
        sql = """select result from big where batchno=? and season=? and episode=? and scene=? and line=?"""

        graph_json = None
        # if the second is empty, return the other
        if relate1_ref[0] == '':
            graph0 = mydb.get_one(sql, (relate0_ref[0], relate0_ref[1], relate0_ref[2], relate0_ref[3], relate0_ref[4]))
            graph_json = json.loads(graph0[0])
        # otherwise, return the difference
        else:
            graph0 = mydb.get_one(sql, (relate0_ref[0], relate0_ref[1], relate0_ref[2], relate0_ref[3], relate0_ref[4]))
            graph1 = mydb.get_one(sql, (relate1_ref[0], relate1_ref[1], relate1_ref[2], relate1_ref[3], relate1_ref[4]))
            diff_graph = get_graph_diff(graph0[0], graph1[0])
            graph_json = diff_graph

        return jsonify({'code': 200, 'data': graph_json})


@app.route('/apiunibatchno', methods=['GET', 'POST'])
@login_required
def apiunibatchno():
    if request.method == 'POST':
        batchno = request.form.get('batchno')
        print(batchno)
        sql = """select count(1) from big where batchno=?"""
        result = mydb.get_one(sql, (batchno,))
        print('数据')
        print('数据', result[0])
        if (result[0] > 0):
            return jsonify({'code': 305, 'msg': '批次已存在请换个名字'})
        else:
            return jsonify({'code': 200})


@app.route('/apidelnode', methods=['GET', 'POST'])
@login_required
def apidelnode():
    relate = request.form.get('relate', '')
    args = relate.split('--')
    if len(args) == 1:
        sql = """delete from big where batchno=?"""
        mydb.update(sql, (args[0],))
    if len(args) == 2:
        sql = """delete from big where batchno=? and Season=?"""
        mydb.update(sql, (args))
    if len(args) == 3:
        sql = """delete from big where batchno=? and Season=? and Episode=?"""
        mydb.update(sql, (args))
    if len(args) == 4:
        sql = """delete from big where batchno=? and Season=? and Episode=? and Scene=?"""
        mydb.update(sql, (args))
    if len(args) == 5:
        sql = """delete from big where batchno=? and Season=? and Episode=? and Scene=? and  Line=?"""
        mydb.update(sql, (args))
    return jsonify({'code': 200, 'msg': '删除数据成功'})


@app.route('/apiverify', methods=['GET', 'POST'])
@login_required
def apiverify():
    return jsonify({'code': 200})


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)
