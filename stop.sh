#!/bin/sh

exec `ps aux|grep "uwsgi -i"|awk '{print $2}'|xargs kill -9`