# coding=UTF-8
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask.ext.bootstrap import Bootstrap
from bson import json_util
import json
from weibo import APIClient
from flask_oauthlib.client import OAuth
import random
from datetime import datetime
from flask import g

from module import auth, project_manager, forms, message

app = Flask(__name__, static_url_path='')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

bootstrap = Bootstrap(app)
oauth = OAuth(app)

APP_KEY = '148981535'  # app key
APP_SECRET = 'b12ec09cd669a458262881e580eba12e'  # app secret
CALLBACK_URL = 'http://tztztztztz.org:5000/code'  # callback url


@app.route('/')
def index():
    return redirect(url_for('homepage'))


@app.context_processor
def test():
    def ran():
        return str(random.randint(1, 9))

    def get_type(type):
        types = [u'微信应用', u'APP', u'SITP', u'数学建模', u'上创']
        return types[int(type)]

    def get_budget(budget):
        budgets = [u'1万以下', u'1-3万', u'3-5万', u'5万以上']
        return budgets[int(budget)]

    return dict(ran=ran, get_type=get_type, get_budget=get_budget)


@app.route('/weibo')
def login_weibo():
    client_ = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client_.get_authorize_url()
    print url
    return redirect(url)


@app.route('/code')
def get_code():
    code = request.args.get('code')
    client_ = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client_.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    client_.set_access_token(access_token, expires_in)
    session['access_token'] = access_token
    session['expires_in'] = expires_in
    session['weibo']['user'] = client_.users.show.get(uid=r.uid)
    session['username'] = session['weibo']['user']['name']
    return redirect(url_for('index'))


@app.route('/project/share', methods=['POST'])
def share_project():
    print '123'
    j = request.json
    client_ = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client_.set_access_token(session['access_token'], session['expires_in'])
    content = dict(status='项目分享!! 项目地址: http://tztztztztz.org:5000/project/'+j.project_id)
    client_.statuses.update.post(json.dumps(content, ensure_ascii=False))
    return jsonify(dict(a=123))




@app.route('/auth/homepage', methods=['POST', 'GET'])
def homepage():
    return render_template('homepage.html')


@app.route('/auth/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    user = dict()
    user['username'] = request.form['email']
    user['password'] = request.form['pass']
    user['nickname'] = request.form['nickname']
    user['name'] = request.form['name']
    user['gender'] = request.form['gender']
    user['phone'] = request.form['phone']
    user['school'] = request.form['school']
    user['major'] = request.form['major']
    user['grade'] = request.form['grade']
    if auth.signup(user):
        session['username'] = user['username']
        return render_template('homepage.html')
    else:
        error = 'sign up failed'
        return render_template('signup.html')


@app.route('/user/person', methods=['GET'])
def person():
    username = session.get('username')
    user = auth.find_user_by_username(username)
    return render_template('user_info.html', user=user)


@app.route('/user/userownproject', methods=['POST', 'GET'])
def userownproject():
    # render template without data
    if request.method == 'GET':
        return render_template('user_own_project.html')
    # request for data
    if request.method == 'POST':
        page_size = 4
        page_no = int(request.json['page_no'])
        pm = project_manager.ProjectManager()
        projects = pm.find_all_projects_by_user(username=session.get('username'),
                                                page_no=page_no,
                                                page_size=page_size)
        response = {}
        project_list = []
        for idx, project in enumerate(projects):
            proj = {'id': idx + 1, '_id': str(project['_id']), 'name': project['name'],
                    'created_time': str(project['created_time'])}
            project_list.append(proj)
        response['projects'] = project_list
        project_count = pm.get_projects_count_by_user(username=session.get('username'))
        import math
        page_count = int(math.ceil(project_count / page_size))
        response['page_count'] = page_count
        response_json = json.dumps(response, default=json_util.default)
        return response_json


@app.route('/user/userattendproject', methods=['POST', 'GET'])
def userattendproject():
    # render template without data
    if request.method == 'GET':
        return render_template('user_attend_project.html')
    # request for data
    if request.method == 'POST':
        page_size = 4
        page_no = int(request.json['page_no'])
        pm = project_manager.ProjectManager()
        projects = pm.find_attend_projects_by_user(username=session.get('username'),
                                                   page_no=page_no,
                                                   page_size=page_size)
        response = {}
        project_list = []
        for idx, project in enumerate(projects):
            proj = {'id': idx + 1, '_id': str(project['_id']), 'name': project['name'],
                    'created_time': str(project['created_time'])}
            project_list.append(proj)
        response['projects'] = project_list
        project_count = pm.get_attend_project_count_by_user(username=session.get('username'))
        import math
        page_count = int(math.ceil(project_count / page_size))
        response['page_count'] = page_count
        response_json = json.dumps(response, default=json_util.default)
        return response_json


@app.route('/user/userinfoedit', methods=['GET'])
def userinfoedit():
    username = session.get('username')
    return render_template('user_info_edit.html')


@app.route('/project/showprojectdetail)', methods=['GET'])
def showprojectdetail():
    project_id = request.args.get('project_id')
    pm = project_manager.ProjectManager()
    project = pm.find_project_by_id(project_id)
    return render_template('showprojectdetail.html', project=project)


@app.route('/auth/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/auth/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return render_template('homepage.html')
    if request.method == 'GET':
        next_url = request.args.get('next_url')
        if next_url is not None:
            return render_template('login.html', next_url=next_url)
        return render_template('login.html', next_url=url_for('homepage'))
    username = request.form['username']
    password = request.form['password']
    next_url = request.form['next_url']
    if auth.valid_login(username, password):
        session['username'] = username
        return redirect(next_url)
    else:
        error = 'invalid username/password'
        return render_template('login.html', error=error)


@app.route('/user/info', methods=['GET'])
def user_info():
    username = session.get('username')
    if username:
        user = auth.find_user_by_username(username)
        return render_template('user_info.html', user=user)
    next_url = '/user/info'
    return redirect(url_for('login', next_url=next_url))


@app.route('/user', methods=['GET'])
def user():
    if session.get('username'):
        return render_template('user.html')
    next_url = '/user'
    return redirect(url_for('login', next_url=next_url))


@app.route('/project/all', methods=['GET'])
def alldisplay():
    pm = project_manager.ProjectManager()
    page = int(request.args.get('page', 1))
    page = max(1, page)
    projects = pm.find_all_project(page=page)
    pages = pm.project_count()
    return render_template('projectshow.html', projects=projects, page=page, pages=range(pages))


@app.route('/project/more', methods=['GET', 'POST'])
def more_projects():
    pm = project_manager.ProjectManager()
    projects = list(pm.find_all_project())
    return json.dumps(projects, default=json_util.default)


@app.route('/project/<project_id>', methods=['GET'])
def singledisplay(project_id):
    pm = project_manager.ProjectManager()
    projects = pm.find_project_by_id(project_id)
    return render_template('projectdisplay.html', project=projects)


@app.route('/project/create', methods=['GET', 'POST'])
def create_project():
    if session.get('username') is None:
        next_url = 'project/create'
        return redirect(url_for('login', next_url=next_url))
    if request.method == 'GET':
        return render_template('projectpublish.html')
    if request.method == 'POST':
        project = dict()
        project['startTime'] = request.form.get('startTime')
        project['endTime'] = request.form.get('endTime')
        project['creator'] = session['username']
        project['name'] = request.form.get('name')
        project['type'] = request.form.get('type')
        project['budget'] = request.form.get('budget')
        project['description'] = request.form.get('description')
        project['contact'] = request.form.get('contact')
        project['contact_mobile'] = request.form.get('contact_mobile')
        project['contact_email'] = request.form.get('contact_email')
        project['currentPeople'] = 1
        project['created_time'] = datetime.now()
        project['team'] = [session['username']]
        project['applier'] = []
        project['maxPeople'] = int(request.form.get('maxPeople'))

        pm = project_manager.ProjectManager()
        pm.create_project(project)
        return redirect(url_for('alldisplay'))


@app.route('/project/protocol', methods=['GET'])
def projectprocotol():
    return render_template('protocol.html')


@app.route('/message', methods=['GET', 'POST'])
def my_message():
    msg = message.show_all_message(session['username'])
    print session['username']
    for result in msg:
        print result[2]
    return render_template('message.html', messages=msg)


@app.route('/project/apply', methods=['POST'])
def apply_project():
    username = session.get('username')
    if username:
        pm = project_manager.ProjectManager()
        pm.apply_project(username, request.json['project_id'])
        print request.json
        print pm.find_project_by_id(request.json['project_id'])
        return '123'
    return 'login'


@app.route('/project/quit', methods=['POST'])
def quit_project():
    username = session.get('username')
    if username:
        pm = project_manager.ProjectManager()
        is_success = pm.kick_out(username=username, project_id=request.json['project_id'])
        return jsonify(result=is_success,
                       mimetype="application/json",
                       status=200)


@app.route('/project/permit', methods=['POST'])
def permit_apply():
    username = session.get('username')
    if username:
        pm = project_manager.ProjectManager()
        mes = message.find_mes_by_id(request.json['message_id'])
        applier = mes['username']
        project_id = mes['project_id']
        if username == mes['project_owner']:
            pm.approve_applier(applier, project_id)
        else:
            print '没有权限'
            return '没有权限'
    return 'login'


@app.route('/message/test', methods=['GET', 'POST'])
def message_test():
    username = session.get('username')
    if username:
        msgs = message.get_all_message(username)
        messtate = [u'申请'.encode("utf-8"), u'同意'.encode("utf-8"), u'退出'.encode("utf-8"), u'被踢出'.encode("utf-8")]
        for msg in msgs:
            index = msg['message_type']
            print index
            msg['message_finaltype'] = messtate[index]
        return render_template("message.html", msgs=msgs)
    next_url = '/message/test'
    return redirect(url_for('login', next_url=next_url))


@app.route('/message/page', methods=['POST', 'GET'])
def message_page():
    if request.method == 'GET':
        if session.get('username') is None:
            next_url = '/message/test'
            return redirect(url_for('login', next_url=next_url))
        return render_template('message.html')
    if request.method == 'POST':
        if session.get('username') is None:
            error = {'error': 'authorization failed'}
            return json.dumps(error)

        page_size = 4
        page_no = int(request.json['page_no'])
        messages = message.find_message_by_user(username=session.get('username'),
                                                page_no=page_no,
                                                page_size=page_size)
        response = {}
        message_list = []
        for idx, msg in enumerate(messages):
            proj = {'id': idx + 1, '_id': str(msg['_id']), 'project_owner': msg['project_owner'],
                    'created_time': str(msg['created_time']),
                    'message_type': msg['message_type'],
                    'projectname': msg['projectname']}
            message_list.append(proj)
        response['messages'] = message_list
        message_count = message.count_message_by_user(username=session.get('username'))
        import math
        page_count = int(math.ceil(message_count / page_size))
        response['page_count'] = page_count
        response_json = json.dumps(response, default=json_util.default)
        return response_json


@app.route('/message/search', methods=['GET', 'POST'])
def message_search():
    username = session.get('username')
    if username:
        msgs = message.search_message(request.form['input'], username)
        return render_template("message.html", msgs=msgs)
        # return json.dumps(msgs)
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
