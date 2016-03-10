# coding=utf-8
from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(Form):
    title = StringField(u"项目名称", validators=[DataRequired()])
    describe = TextAreaField(u"项目描述", validators=[DataRequired()])
    requirements = TextAreaField(u"项目需求", validators=[DataRequired()])
    number_of_member = SelectField(u"项目人数", validators=[DataRequired()], coerce=int,
                                   choices=[(1, 1), (2, 2), (3, 3)])
    time = StringField(u"时间", validators=[DataRequired()])
    submit = SubmitField(u"提交")
