from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User


class RegistrationForm(FlaskForm):
    username = StringField('ФИО',
                           validators=[DataRequired('Поле обязательно к заполнению'), Length(min=2, max=60)])
    email = StringField('Email',
                        validators=[DataRequired('Поле обязательно к заполнению'), Email(message='Поле заполнено неверно')])
    password = PasswordField('Пароль', validators=[DataRequired('Поле заполнено неверно')])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired('Поле обязательно к заполнению'), EqualTo('password')])
    submit = SubmitField('Создать')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email занят. Пожалуйста, выберите другой.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired('Поле заполнено неверно'), Email(message='Поле заполнено неверно')])
    password = PasswordField('Пароль', validators=[DataRequired('Поле заполнено неверно')])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('ФИО',
                           validators=[DataRequired('Поле обязательно к заполнению'), Length(min=8, max=60)])
    email = StringField('Email',
                        validators=[DataRequired('Поле обязательно к заполнению'), Email(message='Поле заполнено неверно')])
    picture = FileField('Изменить личную фотографию', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Изменить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя занято. Пожалуйста, выберите другой.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Это письмо занято. Пожалуйста, выберите другой.')


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=5, max=40)])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')


class TestForm(FlaskForm):
    title = StringField('Название теста', validators=[DataRequired(), Length(min=5, max=50)])
    questions = TextAreaField('Вопросы', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')