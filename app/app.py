# coding=UTF-8
from flask import Flask, render_template, request, session, redirect, url_for
from module import auth, project_manager, forms, message
from flask.ext.bootstrap import Bootstrap
from module.db.factory import MongoFactory

app = Flask(__name__, static_url_path='')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

bootstrap = Bootstrap(app)


@app.route('/')
def index():
	return redirect(url_for('homepage'))


@app.context_processor
def test():
	def display():
		return 'success'

	return dict(display=display)


@app.route('/auth/homepage', methods=['POST', 'GET'])
def homepage():
	return render_template('homepage.html')


@app.route('/auth/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	username = request.form['username']
	password = request.form['password']
	print username, password
	if auth.signup(username, password):
		session['username'] = username
		return render_template('homepage.html')
	else:
		error = 'sign up failed'
		return render_template('signup.html')


@app.route('/auth/person', methods=['GET'])
def persondisplay():
	return render_template('persondisplay.html')


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
	print username, password
	if auth.valid_login(username, password):
		session['username'] = username
		return render_template('homepage.html')
	else:
		error = 'invalid username/password'
		return render_template('login.html', error=error)


@app.route('/project/all', methods=['GET'])
def alldisplay():
	return render_template('projectshow.html')


@app.route('/project/single', methods=['GET'])
def singledisplay():
	return render_template('projectdisplay.html')


@app.route('/project/create', methods=['GET', 'POST'])
def create_project():
	form = forms.ProjectForm()
	if form.validate_on_submit():
		data = dict((key, unicode.encode(request.form.getlist(key)[0], 'utf-8')) for key in request.form.keys())
		# delete csrf token added by WTF
		del data['csrf_token']
		pm = project_manager.ProjectManagcdfer()
		pm.create_project(data)

	return render_template('project.html', form=form)


@app.route('/message', methods=['GET', 'POST'])
def my_message():
	messages = message.show_all_message(session['username'])
	print session['username']
	for result in messages:
		print result[2]
	return render_template('message.html', messages=messages)


@app.route('/message/test', methods=['GET', 'POST'])
def message_test():
	return render_template('message.html');


if __name__ == '__main__':
	app.run(debug=True)
