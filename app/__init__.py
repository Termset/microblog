import os
from flask import app
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ADMINS, MAIL_PASSWORD, MAIL_POST, MAIL_SERVER,MAIL_USERNAME
from flask_mail import Mail

mail = Mail(app)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentails = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentails = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_POST), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentails)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')









