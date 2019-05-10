#!/usr/bin/env python
# encoding: utf-8

__author__ = 'ethan'

import json
import time
from datetime import datetime


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        from datetime import date
        if isinstance(obj, datetime):
            # return obj.strftime('%Y-%m-%d %H:%M:%S')
            return int(time.mktime(obj.timetuple()))
        elif isinstance(obj, date):
            # return obj.strftime("%Y-%m-%d")
            return int(time.mktime(obj.timetuple()))
        else:
            return json.JSONEncoder.default(self, obj)
