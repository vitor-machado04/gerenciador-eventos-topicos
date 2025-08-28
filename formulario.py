# pip install flask_wtf, wtforms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length

class FormularioCriarconta(FlaskForm):
    username = StringField('Nome: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Senha: ', validators=[Length(6, 20)])
    submit = SubmitField('Registrar')

class FormularioEvento(FlaskForm):
    nome = StringField("Nome: ", validators=[DataRequired()])
    data = DateField("Data: ", format='%Y-%m-%d')
    descricao = TextAreaField("Descricao:")
    submit = SubmitField("ADC/UPD Evento")

class FormularioLogin(FlaskForm):
    username = StringField('Nome: ', validators=[DataRequired()])
    password = PasswordField('Senha: ', validators=[Length(6, 20), DataRequired()])
    submit = SubmitField('Login')

