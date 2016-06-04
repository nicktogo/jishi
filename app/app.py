# coding=UTF-8
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask.ext.bootstrap import Bootstrap
from bson import json_util
import json
from weibo import APIClient
from flask_oauthlib.client import OAuth
import random
from datetime import datetime
import os
from flask import g
from module import jweibo

from module import auth, project_manager, forms, message, comment

app = Flask(__name__, static_url_path='')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

bootstrap = Bootstrap(app)
oauth = OAuth(app)

APP_KEY = '148981535'  # app key
APP_SECRET = 'b12ec09cd669a458262881e580eba12e'  # app secret
CALLBACK_URL = 'http://lvh.me:5000/code'  # callback url


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

    def get_type_img(type):
        types = [['wechat1.jpg', 'wechat2.jpg', 'wechat3.png'],['app1.png', 'app2.jpg', 'app3.jpg'],['sitp1.jpg', 'sitp2.jpg', 'sitp3.png'],['math1.jpg', 'math2.jpg', 'math3.jpg'],['shanghai1.jpg', 'shanghai2.jpg', 'shanghai3.jpg']]
        return types[int(type)]

    def get_messgae_number():
        username = session.get('username')
        if username:
            return message.UnSolvedMessageCount(username)
        else:
            return 0
    return dict(ran=ran, get_type=get_type, get_budget=get_budget, get_type_img=get_type_img,get_messgae_number=get_messgae_number)


@app.route('/weibo')
def login_weibo():
    callbackUrl = request.args.get('next', CALLBACK_URL)
    client_ = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=callbackUrl)
    url = client_.get_authorize_url()
    print url
    return redirect(url)


@app.route('/code')
def get_code():
    code = request.args.get('code')
    client_ = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client_.request_access_token(code)
    wuser = jweibo.find_user(int(r.uid))
    if wuser:
        print 'no'
    else:
        print 'yes'
        access_token = r.access_token
        expires_in = r.expires_in
        client_.set_access_token(access_token, expires_in)
        weibo_info = client_.users.show.get(uid=r.uid)
        wuser = jweibo.create_user(weibo_info, code, access_token, expires_in)
        wuser['_id'] = str(wuser['_id'])
        session['user'] = wuser
        session['username'] = wuser['username']
        return redirect(url_for('homepage', first='yes'))
    wuser['_id'] = str(wuser['_id'])
    session['user'] = wuser
    session['username'] = wuser['username']
    return redirect(url_for('homepage'))


@app.route('/project/share', methods=['POST'])
def share_project():
    j = request.json
    module_dir = os.path.dirname(__file__)
    f_path = os.path.join(module_dir, 'static', 'img', 'logo.png')
    f = open(f_path, 'rb')
    wid = jweibo.get_wid(session['username'])
    print wid
    if wid:
        wclient = jweibo.get_client(wid=wid)
        wclient.statuses.upload.post(status=u'济事项目分享,小伙伴们快来加入吧 http://tztztztztz.org:5000/project/' + j['project_id'],
                                     pic=f)
        return jsonify(dict(result='success'))
    else:
        return jsonify(dict(result='error'))


@app.route('/auth/homepage', methods=['POST', 'GET'])
def homepage():
    isFirst = request.args.get('first','no')
    followers = []
    followings = []
    if isFirst == 'yes':
        client_ = jweibo.get_client(session['user']['wid'])
        follower_result = client_.friendships.followers.get(uid=session['user']['wid'])
        if follower_result['total_number'] < 3:
            followers_number = follower_result['total_number']
        else:
            followers_number = 3
        if followers_number == 0:
            followers = []
        else:
            followers = follower_result['users'][:followers_number]
        folloing_result = client_.friendships.friends.get(uid=session['user']['wid'])
        if folloing_result['total_number'] < 3:
            followings_number = folloing_result['total_number']
        else:
            followings_number = 3
        if followings_number == 0:
            followings = []
        else:
            followings = folloing_result['users'][:followings_number]
    return render_template('homepage.html', isFirst=isFirst, followers=followers, followings=followings)


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
            proj = {'id': idx + 1,'status': project['status'],'_id': str(project['_id']), 'name': project['name'],
                    'created_time': str(project['created_time'])}
            project_list.append(proj)
        response['projects'] = project_list
        project_count = pm.get_projects_count_by_user(username=session.get('username'))
        import math
        page_count = int(math.ceil(project_count / page_size))
        response['page_count'] = page_count
        response_json = json.dumps(response, default=json_util.default)
        return response_json


@app.route('/projectstart', methods=['GET'])
def start_project():
    project_id = request.args.get('project_id')
    project_manager.ProjectManager().start_project(project_id)
    return redirect(url_for('showprojectdetail', project_id=project_id))

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


@app.route('/user/userinfoedit', methods=['GET','POST'])
def userinfoedit():
    username = session.get('username')
    if username:
        user = auth.find_user_by_username(username)
    if request.method == 'GET':
        return render_template('user_info_edit.html', user=user)
    if request.method == 'POST':
        user['school'] = request.form['userschool']
        user['grade'] = request.form['usergrade']
        user['phone'] = request.form['userphone']
        user['email'] = request.form['useremail']
        user['interest'] = request.form['userinterest']
        auth.user_info_edit(user)
        return redirect(url_for('user_info'))

@app.route('/project/showprojectdetail)', methods=['GET'])
def showprojectdetail():
    project_id = request.args.get('project_id')
    pm = project_manager.ProjectManager()
    project = pm.find_project_by_id(project_id)
    for i, t_user in enumerate(project['team']):
        _user = auth.find_user_by_username(t_user)
        project['team'][i] = _user
    project['creator'] = auth.find_user_by_username(project['creator'])
    cm = comment.CommentManager()
    comments = cm.get_all_comment_by_projectid(str(project['_id']))
    for _comment in comments:
        _username = _comment['username']
        _user = auth.find_user_by_username(_username)
        _comment['user'] = _user
    print project['_id']
    print comments
    return render_template('showprojectdetail.html', project=project, comments=comments)

@app.route('/project/edit',methods=['GET','POST'])
def project_edit():
    project_id =  request.args.get('project_id')
    pm = project_manager.ProjectManager()
    project = pm.find_project_by_id(project_id)
    return render_template('project_edit.html', project=project)


@app.route('/auth/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('user', None)
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
        session['user'] = g.user
        print g.user
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


@app.route('/user/<username>', methods=['GET'])
def show_user(username):
    user = auth.find_user_by_username(username)
    return render_template('user_info.html', user=user)


@app.route('/user/attend', methods=['GET'])
def user_attend():
    username = session.get('username')
    if username:
        user = auth.find_user_by_username(username)
        return render_template('user_attend_project.html', user=user)
    next_url = '/user/attend'
    return redirect(url_for('login', next_url=next_url))

@app.route('/user/own', methods=['GET'])
def user_own():
    username = session.get('username')
    if username:
        user = auth.find_user_by_username(username)
        return render_template('user_own_project.html', user=user)
    next_url = '/user/own'
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


@app.route('/project/search', methods=['GET','POST'])
def project_search():
    pm = project_manager.ProjectManager()
    input = request.form['input']
    print 'input' + input
    page = int(request.args.get('page', 1))
    page = max(1, page)
    projects = pm.project_search(input, page=page)
    pages = len(list(projects)) / 3 + 1
    print pages
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
        project['status'] = 0
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
            pm.approve_applier(applier, project_id,request.json['message_id'])
            return jsonify(dict(result='ok'))
        else:
            print '没有权限'
            return jsonify(dict(result='false'))
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
            next_url = '/message/page'
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
                    'username':msg['username'],
                    'created_time': str(msg['created_time']),
                    'message_type': msg['message_type'],
                    'isSolved': msg['isSolved'],
                    'user_name':session.get('username'),
                    'projectname': msg['projectname']}
            message_list.append(proj)

        response['messages'] = message_list
        message_count = message.count_message_by_user(username=session.get('username'))
        import math
        page_count = int(math.ceil(float(message_count) / float(page_size)))
        print page_count, message_count
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


@app.route('/project/createcomment', methods=['GET','POST'])
def create_comment():
    username = session.get('username')
    if username:
        cm = comment.CommentManager()
        cm.create_comment(username, request.form['input'], request.form['project_id'])
        return redirect(url_for('showprojectdetail',project_id=request.form['project_id']))
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
