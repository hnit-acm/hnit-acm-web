#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 16:27
# @Author  : Coodyz
# @Site    : https://github.com/coolbreeze2
# @File    : __init__.py
# @Software: PyCharm
import os
from datetime import datetime
from flask import Flask
from acmweb.extensions import db
from acmweb.models import (User,
                           Admin)
from acmweb.viwes import acm_bp
from acmweb.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():
    """创建Flask实例"""
    app = Flask('hnit-acm',
                template_folder=f"{basedir}/acmweb/templates",
                static_folder=f"{basedir}/acmweb/static")
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """初始化扩展"""
    db.init_app(app)
    create_db(app)


def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(acm_bp)


def create_db(app):
    """初始化数据库"""
    with app.app_context():
        if not os.path.exists(app.config['DB_FILE']):
            db.create_all()
            create_admin(app)


def create_admin(app):
    res = Admin.query.all()
    if res:
        return
    admin1 = Admin(name="admin", valid_code="123", password=app.config["ROOT_PWD"],
                   starttime=datetime(2000, 1, 1), endtime=datetime(2000, 1, 1))
    admin1.set_password(app.config["ROOT_PWD"])
    admin2 = Admin(name="root", password=app.config["ROOT_PWD"], valid_code="123",
                   starttime=datetime(2000, 1, 1), endtime=datetime(2000, 1, 1))
    admin2.set_password(app.config["ROOT_PWD"])
    db.session.add(admin1)
    db.session.add(admin2)
    db.session.commit()
