#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/27
"""__DOC__"""

from flask import jsonify
from flask_restful import Resource, reqparse
from application.models import InvoiceModel
from datetime import datetime
import calendar


class Invoices(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('linkedAccountId', type=str)
        self.parser.add_argument('billingDate', type=str)
        self.parser.add_argument('isRecurrent', type=bool, default=None)
        super(Invoices, self).__init__()

    def get(self):
        """
        该 GET 方法有三个可选参数，可以根据需要自由组合使用，返回查询结果
        三个参数都为空时返回 InvoiceModel 中的所有记录。

        *布尔值与数值进行比较的时候，首先会将布尔值转成数字(0/1)然后再比较*
        *eg: ( 2==True => 2==1 return False )*
        :return:
        """
        args = self.parser.parse_args()
        invoices = InvoiceModel.query  # query 对象，后面会用到这个对象的 filter 和 filter_by 等方法
        if args['isRecurrent'] is not None:  # 解决参数值为 False 时 if 不执行的问题
            invoices = invoices.filter_by(isRecurrent=args['isRecurrent'])
        if args['linkedAccountId']:
            invoices = invoices.filter_by(linkedAccountId=args['linkedAccountId'])
        if args['billingDate']:
            dt = args['billingDate']  # 输入参数为‘2017/05’格式的字符串
            start = datetime.strptime(dt, '%Y/%m')  # get first day of the month
            end = datetime(year=start.year, month=start.month,
                           day=calendar.monthrange(start.year, start.month)[1])  # get last day of the month
            invoices = invoices.filter(InvoiceModel.billingDate >= start.date(),
                                       InvoiceModel.billingDate <= end.date()).all()
        return jsonify([obj.to_dict() for obj in invoices])

if __name__ == '__main__':
    pass
