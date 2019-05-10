#!/usr/bin/env python
# encoding: utf-8
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from common import CJsonEncoder
from controller import supplier
from model import db
from resource import config

app = Flask(__name__)

app.secret_key = config.SECRET_KEY
app.json_encoder = CJsonEncoder

app.register_blueprint(supplier)

logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logStream = logging.StreamHandler()
logStream.setFormatter(logging_format)
logger.addHandler(logStream)

handler = RotatingFileHandler(config.LOG_PATH + '/running.log', maxBytes=10 * 1024 * 1024, backupCount=10,
                              encoding='UTF-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging_format)
app.logger.addHandler(handler)


@app.after_request
def after_request(response):
    if response.content_type == "application/json":
        logging.getLogger('requests').info("Response =>%s\t%s", response.status, response.response)
    return response


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
