from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, IntegerField, StringField, PasswordField, RadioField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    product = StringField('Название', validators=[DataRequired()])

    country = StringField('Страна отправки', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    # picture = BinaryField("", validators=[DataRequired()])
    cnt = 0
    submit = SubmitField('Submit')


class ProductForm2(FlaskForm):
    submit = SubmitField('Submit')
