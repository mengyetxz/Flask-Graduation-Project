#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/18
"""__DOC__"""

from flask_restful import Resource, reqparse, abort
from ..models import UserModel


def abort_if_args_doesnt_exist():
    pass


def abort_if_args_already_exist():
    pass


class UserRegister(Resource):
    @staticmethod
    def get():
        users = UserModel.find_all()
        return [{'email': user.email,
                 'username': user.username,
                 'id': user.id} for user in users]

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        # if don't check this condition will get errors:
        # IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.username
        # [SQL: u'INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)']
        # [parameters: (u'm@1.com', u'm', 'pbkdf2:sha1:1000$bCy26wLo$43da0111503414651a9e4a739626b4b1d2ad4389')]
        if UserModel.find_by_email_or_username(args['email'], args['username']):
            abort(400, message="This email or user already exists")
            # abort method do the same as below
            # return {'message': 'This email or user already exists'}, 400

        user = UserModel(email=args['email'], username=args['username'], password=args['password'])
        user.save_to_db()
        return {'email': args['email'], 'username': args['username']}


class UserModify(Resource):
    # 给已经登陆的用户提供修改user信息的权限
    @staticmethod
    def put(current_user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        user = UserModel.find_by_email_or_username(args['email'], args['username'])
        # 验证是否是当前登陆的用户
        if user and user.id != current_user_id:
            abort(400, message="email or username already exist")
        if not user:
            user = UserModel.get(current_user_id)
        user.email = args['email'] or user.email
        user.username = args['username'] or user.username
        if args['password']:
            user.password = args['password']
        user.save_to_db()
        return {'email': user.email, 'username': user.username}

    @staticmethod
    def delete():
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('username')
        args = parser.parse_args()
        if not (args['email'] or args['username']):
            abort(400, message="Email or username required")
        me = UserModel.find_by_email_or_username(args['email'], args['username'])
        if not me:
            abort(400, message="The user doesn't exists")
        me.delete_from_db()
        return "delete success"


if __name__ == '__main__':
    pass
