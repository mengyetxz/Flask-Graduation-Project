#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/27
"""__DOC__"""

from flask import jsonify
from flask_restful import Resource, reqparse
from invoice_records import records_merge
from ..models import InvoiceModel


class InvoiceImport(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('filename', required=True, help='filename required!')
    parser.add_argument('columns')

    @classmethod
    def post(cls):
        """
        将 CSV 文件中的 invoice 数据交给 record_merge() 合并然后导入数据库的表 InvoiceModel 中。
        ** 尚未处理 POST 多次提交时返回提示信息。**
        :return:
        """
        args = cls.parser.parse_args()
        try:
            records_merged = records_merge(args['filename'])
        except IOError:
            return "Such file does not exist! filename:'{}'".format(args['filename']), 400
        for record in records_merged:
            invoice = InvoiceModel(**record.to_dict())
            invoice.save_to_db()
        # 自定义 MyJSONEncoder: 继承 Flask.json.JSONEncoder 类, 重写 default()
        return jsonify([obj.to_dict for obj in records_merged])

if __name__ == '__main__':
    pass
