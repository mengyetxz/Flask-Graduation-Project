#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/12
"""__DOC__"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class InvoiceModel(db.Model):
    __tablename__ = 'invoices'
    linkedAccountId = db.Column(db.String(16), primary_key=True, index=True)
    billingDate = db.Column(db.Date, primary_key=True, index=True)
    invoiceDate = db.Column(db.Date, primary_key=True, index=True)
    productCode = db.Column(db.String(16), primary_key=True, index=True)
    isRecurrent = db.Column(db.Boolean)
    costBeforeTax = db.Column(db.DECIMAL)
    credits = db.Column(db.DECIMAL)
    taxAmount = db.Column(db.DECIMAL)
    totalCost = db.Column(db.DECIMAL)

    def __init__(self, linkedAccountId, billingDate, invoiceDate, productCode,
                 isRecurrent, costBeforeTax, credits, taxAmount, totalCost):
        self.linkedAccountId = linkedAccountId
        self.billingDate = billingDate
        self.invoiceDate = invoiceDate
        self.productCode = productCode
        self.isRecurrent = isRecurrent
        self.costBeforeTax = costBeforeTax
        self.credits = credits
        self.taxAmount = taxAmount
        self.totalCost = totalCost

    def to_dict(self):
        return {
            "linkedAccountId": self.linkedAccountId,
            "billingDate": self.billingDate,
            "invoiceDate": self.invoiceDate,
            "productCode": self.productCode,
            "isRecurrent": self.isRecurrent,
            "costBeforeTax": self.costBeforeTax,
            "credits": self.credits,
            "taxAmount": self.taxAmount,
            "totalCost": self.totalCost
        }

    def __repr__(self):
        return '<InvoiceModel %r>' % self.linkedAccountId

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        # return type : list
        return cls.query.all()

    @classmethod
    def find_by_linkedAccountId(cls, linkedAccountId):
        return cls.query.filter_by(linkedAccountId=linkedAccountId)


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    # 把一个方法设成属性调用
    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<UserModel %r>' % self.username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        # return type : list -> [<User u'admin'>, <User u'guest'>]
        return cls.query.all()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email_or_username(cls, email, username):
        return cls.query.filter_by(email=email).first() or \
               cls.query.filter_by(username=username).first()


# typeof user_id is unicode
@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(int(user_id))
