# coding=UTF-8
from flask import Flask, render_template, request, session, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from bson import json_util
import json
from weibo import APIClient
from flask_oauthlib.client import OAuth
import random
from datetime import datetime

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
        return str(random.randint(1,9))

    return dict(ran=ran)


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
    print 'access_token is', access_token
    expires_in = r.expires_in
    client_.set_access_token(access_token, expires_in)
    return redirect(url_for('index'))


@app.route('/auth/homepage', methods=['POST', 'GET'])
def homepage():
    return render_template('homepage.html')


@app.route('/auth/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    username = request.form['email']
    password = request.form['pass']
    if auth.signup(username, password):
        session['username'] = username
        return render_template('homepage.html')
    else:
        error = 'sign up failed'
        return render_template('signup.html')


@app.route('/auth/person', methods=['GET'])
def persondisplay():
    return render_template('persondisplay.html')


@app.route('/auth/personedit', methods=['GET'])
def personedit():
    return render_template('person.html')


@app.route('/project/showprojectdetail', methods=['GET'])
def showprojectdetail():
    return render_template('showprojectdetail.html')


@app.route('/auth/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return render_template('login.html')


@app.route('/auth/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return render_template('homepage.html')
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    if auth.valid_login(username, password):
        session['username'] = username
        return render_template('homepage.html')
    else:
        error = 'invalid username/password'
        return render_template('login.html', error=error)


@app.route('/project/all', methods=['GET'])
def alldisplay():
    pm = project_manager.ProjectManager()
    page = int(request.args.get('page', 1))
    projects = pm.find_all_project(page=page)
    return render_template('projectshow.html', projects=projects,page=page)


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
    if request.method == 'GET':
        return render_template('projectpublish.html')
    if session.get('username'):
        project = dict()
        project['creator'] = session['username']
        project['name'] = request.form.get('name')
        project['type'] = request.form.get('type')
        project['budget'] = request.form.get('budget')
        project['description'] = request.form.get('description')
        project['contact'] = request.form.get('contact')
        project['contact_mobile'] = request.form.get('contact_mobile')
        project['currentPeople'] = 1
        project['created_time'] = datetime.now()
        project['team'] = [session['username']]
        project['applier'] = []
        project['maxPeople'] = int(request.form.get('maxPeople'))

        pm = project_manager.ProjectManager()
        pm.create_project(project)
        return redirect(url_for('alldisplay'))
    return redirect(url_for('login'))


@app.route('/project/projectpublish', methods=['GET'])
def projectpublish():
    return render_template('projectpublish.html')



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
        pm.apply_project(username,request.json['project_id'])
        # projectapplyed = pm.find_project_by_id(request.json['project_id'])
        # projectOwner = projectapplyed['name']
        # projectName = projectapplyed['projectname']
        # message.apply(username,request.json['project_id'],projectName,projectOwner)
        print request.json
        print pm.find_project_by_id(request.json['project_id'])
        return '123'
    return 'login'


@app.route('/project/permit', methods=['POST'])
def permit_apply():
    username = session.get('username')
    if username:
        pm = project_manager.ProjectManager()
        mes = message.find_mes_by_id(request.json['message_id'])
        project_id = mes['project_id']
        pm.approve_applier(username,project_id)
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
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
