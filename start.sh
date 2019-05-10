#!/bin/sh

exec nohup uwsgi -i uwsgi.ini >/dev/null 2>&1 &