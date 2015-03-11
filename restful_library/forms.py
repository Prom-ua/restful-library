from flask.ext.wtf import Form
from wtforms import PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired


class LoginForm(Form):
    email = EmailField(
        'E-mail',
        validators=[InputRequired()],
        filters=[lambda v: v.lower() if v else None],
    )
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember = BooleanField('Запомнить меня')
