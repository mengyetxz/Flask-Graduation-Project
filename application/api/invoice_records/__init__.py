#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/24
"""
return jsonify(records_merged) 时 Error:
<InvoiceRecord %r> is not JSON serializable
表示 InvoiceRecord 类不能序列化成 JSON 对象
所以添加自定义类的 JSON 序列化方法

Thinking:
-- 1 start -- Error：RuntimeError: Working outside of request context.
class RecordsMerge(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('filename', required=True, help='filename cant be blank')
    parser.add_argument('columns')
    args = parser.parse_args()  # args can't be class variable

    @classmethod
    def get(cls):
        return str(records_merge(cls.args['filename']))

Error Message:
    raise RuntimeError(_request_ctx_err_msg)
RuntimeError: Working outside of request context.
-- 1 end --

-- 2 start -- 正确
class RecordsMerge(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('filename', required=True, help='filename cant be blank')
    parser.add_argument('columns')

    @staticmethod
    def get():
        args = RecordsMerge.parser.parse_args()
        return str(records_merge(args['filename']))
-- 2 end --

-- 3 start -- 正确
class RecordsMerge(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('filename', required=True, help='filename cant be blank')
    parser.add_argument('columns')

    @classmethod
    def get(cls):
        args = cls.parser.parse_args()
        return str(records_merge(args['filename']))
-- 3 end --
"""

from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with
from csv_reader import CSVReader
from invoice_record import InvoiceRecord


resource_fields = {
    "linkedAccountId": fields.String,
    "billingDate": fields.DateTime,  # db.Column(db.Date)
    "invoiceDate": fields.DateTime,  # db.Column(db.Date)
    "productCode": fields.String,
    "isRecurrent": fields.Boolean,
    "costBeforeTax": fields.Float,
    "credits": fields.Float,
    "taxAmount": fields.Float,
    "totalCost": fields.Float,
    'uri': fields.Url('api.records_merge')
}


class RecordsMerge(Resource):
    """
    Rest API for testing function records_merge(csvin):
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename', type=str, required=True, help='filename cant be blank')
        self.parser.add_argument('columns')
        super(RecordsMerge, self).__init__()

    @marshal_with(resource_fields)
    def get(self):
        """
        for testing function records_merge(filename)
        :return:
        """
        args = self.parser.parse_args()
        merged = records_merge(args['filename'])
        # return jsonify([obj.to_dict() for obj in merged])
        return merged


def records_merge(filename):
    reader = CSVReader(csvin=filename).rows
    # put record into list of records, <record> is instance of <class InvoiceRecord>，*该对象不能序列化成JSON*
    records = []
    for record in reader:
        records.append(InvoiceRecord(**record))
    # 合并后的 record 对象存放在 records_merged 列表
    records_merged = []
    for record in records:
        if record not in records_merged:
            records_merged.append(record)
        else:
            records_merged[records_merged.index(record)] += record
    # 合并完成
    return records_merged


if __name__ == '__main__':
    def records_merge(csvin):
        """
        :param csvin: 账单文件
        :param columns: 需要的列 2017/05/27 移除columns
        :return: 返回合并后的列表
        """
        reader = CSVReader(csvin).rows
        records = []
        for record in reader:
            records.append(InvoiceRecord(**record))
        records_merged = []
        for record in records:
            if record not in records_merged:
                records_merged.append(record)
            else:
                records_merged[records_merged.index(record)] += record
        return records_merged

    # test function: records_merge(csvin, columns)
    csv_name = '412764460734-aws-cost-allocation-ACTS-2017-03.csv'
    # cols = current_app.config.get('COLUMNS_DEFAULT')
    records_merged = records_merge(csv_name)
    records_merged.sort(reverse=True)

    # test return values
    for i in xrange(15):
        print records_merged[i].linkedAccountId,
        print records_merged[i].billingDate.strftime('%Y/%m'),
        print records_merged[i].invoiceDate.strftime('%Y/%m'),
        print records_merged[i].productCode,
        print records_merged[i].costBeforeTax,
        print records_merged[i].credits,
        print records_merged[i].taxAmount,
        print records_merged[i].totalCost
    # 输出结果，这里发现第 5 行的 TotalCost 为 0 值，而 CSVReader 已经过滤了 0 值，这是为什么呢？
    # 经过分析，这确实不是 CSVReader 的锅，而是 recordMerge 将PK相同的记录合并，正负值相加后的结果
    # 而得到的 0 值，业务逻辑上是有意义的，表示客户所产生的资源使用费被 Credits 抵扣，最终花费为 0
    '''
    425155429375 2017/03 2017/04 AmazonS3 0.035629 0.000000 0.000000 0.035629
    623377202974 2017/03 2017/03 AmazonEC2 94610.000000 0.0 5676.600000 100286.600000
    412764460734 2017/03 2017/04 AmazonEC2 1260.804901 -477.534309 46.999999 830.270595
    488275793382 2017/03 2017/04 AmazonEC2 171.961821 -43.006743 7.740004 136.695082
    639127770567 2017/03 2017/04 AmazonEC2 2141.456479 -2141.456479 0.000000 0.000000
    639127770567 2017/03 2017/04 AmazonS3 0.001195 0.000000 0.000000 0.001195
    623377202974 2017/03 2017/04 AmazonRDS 857.194839 0.000000 51.430000 908.624839
    626162493902 2017/03 2017/04 AmazonS3 0.002213 0.000000 0.000000 0.002213
    425155429375 2017/03 2017/04 AWSDataTransfer 0.157790 0.000000 0.010000 0.167790
    639127770567 2017/03 2017/04 AWSDataTransfer 11.734457 0.000000 0.700000 12.434456
    626162493902 2017/03 2017/04 AmazonEC2 4783.468240 -1196.320153 215.220001 3802.368089
    626162493902 2017/03 2017/04 AmazonRDS 7348.320002 0.000000 440.900000 7789.220002
    515743265704 2017/03 2017/04 AWSDataTransfer 0.031553 0.000000 0.000000 0.031553
    412764460734 2017/03 2017/04 AmazonS3 6.942127 0.000000 0.420001 7.362129
    515743265704 2017/03 2017/04 AmazonEC2 770.981678 -192.818447 34.700002 612.863233
    '''
