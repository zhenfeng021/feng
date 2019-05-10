#!/usr/bin/env python
# encoding: utf-8
__author__ = 'ethan'

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange


class MustRequired(DataRequired):
    def __init__(self):
        super(MustRequired, self).__init__()
        self.message = "必填项，不能为空"


class FloatRegexp(Regexp):
    def __init__(self):
        super(FloatRegexp, self).__init__(r'^\d*[\.]?\d*$')
        self.message = '只允许浮点数值'


class NummberARegexp(Regexp):
    def __init__(self):
        super(NummberARegexp, self).__init__(r'^\d{1,10},\d{10}$')
        self.message = "只能包含','和数字',时间戳为10位"


class CouponSKUForm(FlaskForm):
    storeId = StringField('storeId', validators=[MustRequired()])
    title = StringField('title')
    picture = StringField('picture')
    price = StringField('price',
                        validators=[MustRequired(), Length(1, 10), FloatRegexp()])
    priceRemark = StringField('priceRemark')
    summery = StringField('summery')
    detail = StringField('detail')
    unique = IntegerField('unique')
    today_available = BooleanField('today_available')
    style = SelectField('style', choices=[('day', '天'), ('expired_range', '范围')], validators=[DataRequired()])
    params = StringField('params', validators=[MustRequired(), NummberARegexp()])
