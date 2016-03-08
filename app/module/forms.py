# coding=utf-8
from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(Form):
    title = StringField(u"项目名称", validators=[DataRequired()])
    describe = TextAreaField(u"项目描述", validators=[DataRequired()])
    submit = SubmitField(u"提交")
