#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/7
"""__DOC__"""

import os
import datetime
from decimal import Decimal
from flask.json import JSONEncoder

# path of the current file the configure path
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # path setting of uploading and downloading excel file
    UPLOADED_CSVFILES_DEST = os.path.join(basedir, 'application', 'static', 'uploaded', 'csv_files')
    ALLOWED_EXTENSIONS = {'csv'}
    # EXPORT_FOLDER = os.path.join(basedir, 'static', 'data', 'export_file')

    # columns default for api_invoice_records
    COLUMNS_DEFAULT = (
        'LinkedAccountId',
        'BillingPeriodStartDate',
        'InvoiceDate',
        'ProductCode',
        'CostBeforeTax',
        'Credits',
        'TaxAmount',
        'TotalCost')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    threaded = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_DEV') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_TEST') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_PRO') or \
         'sqlite:///' + os.path.join(basedir, 'data-pro.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime.date):
            return o.strftime('%Y/%m')
        return super(MyJSONEncoder, self).default(o)


if __name__ == '__main__':
    pass
