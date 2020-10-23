#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 15:14
# @Author  : Coodyz
# @Site    : https://github.com/coolbreeze2
# @File    : models.py
# @Software: PyCharm
from acmweb.extensions import db
from datetime import datetime
from werkzeug.security import (generate_password_hash,
                               check_password_hash)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), unique=False, nullable=False)
    student_num = db.Column(db.String(15), unique=True, nullable=False)
    major = db.Column(db.String(20), unique=False, nullable=False)
    classes = db.Column(db.String(20), unique=False, nullable=False)
    phone_num = db.Column(db.String(11), unique=False, nullable=False)
    qq_num = db.Column(db.String(16), unique=False, nullable=False)
    group = db.Column(db.String(10), unique=False, nullable=False)
    reg_time = db.Column(db.DATE, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % self.name


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    valid_code = db.Column(db.String(6), unique=False, nullable=False)
    starttime = db.Column(db.DATE, unique=False, nullable=False)
    endtime = db.Column(db.DATE, unique=False, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
