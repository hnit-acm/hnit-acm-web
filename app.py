# -*- coding: utf-8 -*-
"""Flask应用主文件"""
from gevent import monkey

monkey.patch_all()

import os
from acmweb.extensions import db
from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer
from acmweb import create_app

if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    app = create_app()

    app.jinja_env.auto_reload = True  # 静态文件热更
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
