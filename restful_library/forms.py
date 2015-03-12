from flask.ext.wtf import Form
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange


class LoginForm(Form):
    email = EmailField(
        'E-mail',
        validators=[InputRequired()],
        filters=[lambda v: v.lower() if v else None],
    )
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember = BooleanField('Запомнить меня')


class ApiTokenForm(Form):
    expiry_days = IntegerField(
        'Действителен дней (от 1 до 30)',
        validators=[InputRequired(), NumberRange(1, 30)],
    )
    description = TextAreaField(
        'Описание (имя кандидата, другие комментарии)',
        validators=[Length(max=300)],
    )
