#!/usr/bin/env python
# encoding: utf-8
__author__ = 'ethan'


from resource.config import DB as conf
from peewee import MySQLDatabase
from playhouse.signals import Model, pre_save, post_save

db = MySQLDatabase(database=conf['database'],
                   host=conf["host"],
                   port=conf['port'],
                   user=conf['user'],
                   passwd=conf['password'],
                   charset=conf['charset'])


def table_function(model):
    name = model.__name__
    result = []
    count = 0
    for s in name:
        if 65 <= ord(s) <= 90:
            if count == 0 and s != name[0]:
                count = count + 1
                result.append('_')
            result.append(s.lower())
        elif 97 <= ord(s) <= 122:
            result.append(s.lower())
        else:
            result.append("_")
    return ''.join(result)


class BaseModel(Model):
    class Meta:
        database = db
        table_function = table_function
