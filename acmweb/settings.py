#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 16:29
# @Author  : Coodyz
# @Site    : https://github.com/coolbreeze2
# @File    : settings.py
# @Software: PyCharm
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dawd2y3872jkrg')

    ROOT_PWD = "dhw8ye892yjkhfgh"
    DB_FILE = "acmWeb.db"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, DB_FILE))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = BaseConfig
