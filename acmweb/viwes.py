#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 15:15
# @Author  : Coodyz
# @Site    : https://github.com/coolbreeze2
# @File    : blueprints.py
# @Software: PyCharm
import random
from datetime import datetime
from acmweb.models import (User,
                           Admin)
from acmweb.extensions import db
from flask import (Blueprint,
                   send_file,
                   render_template,
                   request,
                   flash,
                   session,
                   abort,
                   redirect,
                   url_for)
from acmweb.xlwrite import get_registerInfo

acm_bp = Blueprint('acm', __name__)


def is_valid(major, classes, student_num, name, phone_num, qq_num):
    """信息验证"""
    if (len(major) + len(name) + len(qq_num)) is 0:
        return '请完善所有信息'
    if len(classes) != 4:
        return '请确认班级号为4位，如1701'
    if len(student_num) != 11:
        return '请确认学号为11位'
    if len(phone_num) != 11:
        return '请确认手机号为11位'
    return True


@acm_bp.route("/download", methods=['GET'])
def download():
    if session.get("is_valid"):
        random_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        r = "".join([random.choice(random_str) for i in range(6)])
        filename = f"ACM新生报名表-{datetime.date(datetime.now())}-" + r + ".xlsx"
        users = User.query.all()
        register_info = get_registerInfo(users=users)
        return send_file(register_info, attachment_filename=filename, as_attachment=True, cache_timeout=0)
    else:
        abort(403)


@acm_bp.route('/', methods=['GET'])
def home():
    """主页面"""
    return render_template("index.html")


@acm_bp.route('/index', methods=['GET'])
def index():
    """主页面"""
    return render_template("index.html")


@acm_bp.route('/robot', methods=['GET'])
def robot():
    """机器人"""
    return render_template("robotIndex.html")


@acm_bp.route('/acm', methods=['GET'])
def acm():
    """acm"""
    return render_template("acmIndex.html")


@acm_bp.route('/acmer', methods=['GET'])
def acmer():
    """acmer兵种树"""
    return render_template("acmer.html")


@acm_bp.route('/photo', methods=['GET'])
def photo():
    """acm照片墙"""
    return render_template("photo.html")


@acm_bp.route('/nao_photo', methods=['GET'])
def nao_photo():
    """nao照片墙"""
    return render_template("NaoPhoto.html")


@acm_bp.route('/vs_code', methods=['GET', 'POST'])
def vs_code():
    """报名表下载页面"""
    if request.method == 'GET':
        return render_template("vs_code.html")
    elif request.method == 'POST':
        form = request.form
        valid_code = form.get("valid_code")
        ad = Admin.query.filter_by(name="admin").first()
        if ad.valid_code == valid_code:
            session['is_valid'] = True
            flash(message="Success: 下载成功！", category='info')
            return redirect(url_for('acm.download'))
        else:
            flash(message="Error: 提取码错误！", category='error')
            return redirect(url_for('acm.vs_code'))


@acm_bp.route('/auth', methods=['GET', 'POST'])
def auth():
    """认证页面"""
    if request.method == 'GET':
        return render_template("atuh.html")
    elif request.method == 'POST':
        form = request.form
        username = form.get("username")
        password = form.get("password")
        ad = Admin.query.filter_by(name=username).first()
        if ad.check_password(password):
            session['username'] = username
            return redirect(url_for("acm.admin"))
        else:
            flash(message="Error: 登陆失败！", category="error")
            return redirect(url_for("acm.auth"))


@acm_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    """管理员"""
    username = session.get('username')
    if not username:
        abort(403)
    ad = Admin.query.filter_by(name="admin").first()
    if request.method == 'POST':
        form = request.form
        password = form.get("password")
        valid_code = form.get("valid_code")
        starttime = form.get("starttime")
        endtime = form.get("endtime")
        if username != "root" and password:
            flash(message="Error: 无改密权限！", category="error")
            return redirect(url_for("acm.admin"))
        else:
            if username == "root":
                ad.set_password(password)
            ad.valid_code = valid_code if valid_code else ad.valid_code
            try:
                ad.starttime = datetime.strptime(starttime, "%Y-%m-%d") if starttime else ad.starttime
                ad.endtime = datetime.strptime(endtime, "%Y-%m-%d") if endtime else ad.endtime
            except ValueError:
                return redirect(url_for("acm.admin"))
        db.session.add(ad)
        db.session.commit()
        flash(message="Success: 更改成功！", category="info")
        return redirect(url_for("acm.admin"))
    return render_template('admin.html',
                           valid_code=ad.valid_code,
                           starttime=ad.starttime,
                           endtime=ad.endtime,
                           username=username)


@acm_bp.route('/login', methods=['GET', 'POST'])
def login():
    """报名页面"""
    flag = True
    ad = Admin.query.filter_by(name="admin").first()
    now_time = datetime.date(datetime.today())
    if now_time < ad.starttime:
        flag = False
        flash(message=f"Error: 报名未开始！", category='error')
    elif now_time > ad.endtime:
        flag = False
        flash(message=f"Error: 报名已截止！", category='error')
    if request.method == 'POST':
        major = request.form['major']
        classes = request.form['classes']
        student_num = request.form['studentNum']
        name = request.form['name']
        phone_num = request.form['phoneNum']
        qq_num = request.form['qqNum']
        group = request.form['group']

        valid = is_valid(major, classes, student_num, name, phone_num, qq_num)
        if isinstance(valid, bool) and flag:
            user = User(name=name, student_num=student_num, major=major,
                        classes=classes, phone_num=phone_num, qq_num=qq_num, group=group)
            res_user = User.query.filter_by(student_num=student_num).first()
            if res_user:
                res_user.major = major
                res_user.classes = classes
                res_user.student_num = student_num
                res_user.name = name
                res_user.phone_num = phone_num
                res_user.qq_num = qq_num
                res_user.group = group
            else:
                db.session.add(user)
            db.session.commit()
            flash(message="Success: 报名成功！", category='info')
        else:
            flash(message=f"Error: {valid}", category='error')
        return redirect(url_for("acm.login"))
    return render_template('login.html')
