#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

from itsdangerous import Serializer
from peewee import PrimaryKeyField, CharField, IntegerField, DateTimeField, BooleanField
from playhouse.shortcuts import model_to_dict
from werkzeug.security import generate_password_hash, check_password_hash

from model import BaseModel
from flask_login import UserMixin

from resource import config

__author__ = 'ethan'


class Permission(object):
    READ = 1
    ZAN = 2
    SHARE = 3
    STORE = 4
    STORE_ADD = 5
    STORE_EDIT = 6
    COUPON_ADD = 7
    COUPON_EDIT = 8
    COUPON_USED = 9
    ADMIN = 99
    ROOT = 9999


class Panel(object):
    STORE = 1  # 店铺管理
    LICENSE = 2  # 邀请码管理
    SELL = 3  # 营销管理
    INCOME = 4  # 收入管理
    PROMOTER = 5  # 推广员管理
    MASTER = 6  # 店长管理
    LINK = 7  # 创建邀请链接
    PAY = 8  # 创建付款链接
    PROHIBIT = 9  # 禁封店铺
    CHANGE = 10  # 转让店长
    STORE_EDIT = 11  # 编辑店铺
    VIP_EDIT = 12  # 修改vip时长
    PHONE_HIDE = 13  # 隐藏店长电话


class Role(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    default = BooleanField(default=False)
    permissions = CharField()
    create_at = DateTimeField(default=datetime.now)
    update_at = DateTimeField()

    @staticmethod
    def insert_roles():
        roles = {
            "customer": [Permission.READ, Permission.ZAN, Permission.SHARE],
            "supplier": [Permission.STORE, Permission.STORE_ADD, Permission.STORE_EDIT,
                         Permission.COUPON_ADD, Permission.COUPON_EDIT, Permission.COUPON_USED],
            "pre": [Permission.READ],
            "admin": [Permission.READ, Permission.ZAN, Permission.SHARE,
                      Permission.STORE, Permission.STORE_ADD, Permission.STORE_EDIT,
                      Permission.COUPON_ADD, Permission.COUPON_EDIT, Permission.COUPON_USED,
                      Permission.ADMIN],
            "root": [Permission.ADMIN, Permission.ROOT]
        }
        default_role = 'customer'
        for r in roles:
            role = None
            try:
                role = Role.get_or_none(name=r)
            except:
                pass
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            role.update_at = datetime.now()
            role.save()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            if self.permissions != 0:
                permissions = str(self.permissions).split(",")
                permissions.append(str(perm))
                self.permissions = ",".join(permissions)
            else:
                self.permissions = perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        for it in str(self.permissions).split(','):
            if int(it) & perm == perm:
                return True
        return False


class User(UserMixin, BaseModel):
    id = PrimaryKeyField()
    account = CharField(unique=True, max_length=64)
    password = CharField()
    passHash = CharField()
    openId = CharField(index=True, max_length=64)
    unionId = CharField(null=True, index=True, max_length=64)
    session_key = CharField(null=True, max_length=32)
    phone = CharField(null=True, max_length=20)

    # wechat userinfo
    nickName = CharField(max_length=64)
    gender = IntegerField()
    city = CharField(max_length=64)
    avatar = CharField(null=True)
    province = CharField(max_length=64)
    country = CharField(max_length=64)
    language = CharField(max_length=64)
    # wechat userinfo end

    last_login_ip = CharField(max_length=64)

    roleId = IntegerField(index=True)
    create_at = DateTimeField(default=datetime.now)
    update_at = DateTimeField()

    role = None

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.roleId is not None:
                self.role = Role.get_or_none(Role.id == self.roleId)
            if self.role is None:
                self.role = Role.get_or_none(Role.default == True)
        self.roleId = self.role.id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passHash, password)

    def generate_auth_token(self, expiration=604800):
        """
        生成token，7天有效期
        :param expiration:
        :return:
        """
        s = Serializer(config.SECRET_KEY, expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def has_panel(self, panel):
        return True

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def is_root(self):
        return self.can(Permission.ROOT)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        except Exception, e:
            return None
        return User.get_or_none(User.id == int(data.get('id')))

    @staticmethod
    def get_active_user(token):
        userInfo = memHandler.get(token)
        try:
            if userInfo is not None:
                return dict_to_model(json.loads(userInfo), User)
        except Exception, e:
            pass
        return None

    def __repr__(self):
        return '<User %r>' % self.account

    def set_phone(self, phone, session_key):
        self.phone = phone
        return User.update(phone=phone, session_key=session_key, update_at=datetime.now()).where(
            User.openId == self.openId).execute() > 0

    def get_dict(self):
        item = model_to_dict(self)
        item['uid'] = item.get('id')
        item.pop('id')
        item.pop('passHash')
        item.pop('session_key')
        return item
