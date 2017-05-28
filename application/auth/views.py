#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/12
"""__DOC__"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from ..models import UserModel
from .forms import LoginForm, RegisterForm


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserModel(email=form.email.data,
                         username=form.username.data,
                         password=form.password.data)
        user.save_to_db()
        # 注册完自动登陆该用户
        login_user(user)
        return redirect(url_for('invoice.index'))
    return render_template('login.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.find_by_email(form.email.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)

            flash(u'登陆成功')
            # The page they were attempting to access will be passed in
            # the next query string variable, so you can redirect there
            # if present instead of the homepage.
            arg_next = request.args.get('next')

            return redirect(arg_next or url_for('invoice.index'))
        flash(u'无效的用户名或密码')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'退出成功')
    return redirect(url_for('auth.login'))


