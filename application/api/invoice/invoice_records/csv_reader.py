#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/24
"""__DOC__"""

import os
import csv
from flask import current_app


class CSVReader(object):
    """
    pre_api_module = None
    功能：
        读取指定的CSV文件(csvin)中指定的行(columns)
    条件：
        只查询 RecordType == LinkedLineItem 且 TotalCost != 0 的行，每行的 columns 列
    输入：
        见初始化参数
    初始化参数说明：
        csvin <str> CSV文件名
        columns <tuple> 包含所需的列名字符串 2017/05/27 移除columns=current_app.config.get('COLUMNS_DEFAULT')
    属性说明：
        self.header = [col_1, col_2, col_3, ..., col_n]
        self.rows = [{record_1}, {record_2}, {record_3}, ..., {record_n}]
        record <dict> key:columns中的列名，val:csv表中列名对应的数据
    输出说明：
        output_for_invoice_record = self.rows
    """
    def __init__(self, csvin):
        self.csvin = os.path.join(current_app.config.get('UPLOADED_CSVFILES_DEST'), csvin)
        self.header = []
        self.rows = []
        with open(self.csvin, 'rb') as f:
            reader = csv.reader(f)
            next(reader)
            self.header = next(reader)
            for row in reader:
                if float(row[self.header.index('TotalCost')]) == 0 or row[self.header.index('RecordType')] != 'LinkedLineItem':
                    pass
                else:
                    record = {'linkedAccountId': row[self.header.index('LinkedAccountId')],
                              'billingDate': row[self.header.index('BillingPeriodStartDate')],
                              'invoiceDate': row[self.header.index('InvoiceDate')],
                              'productCode': row[self.header.index('ProductCode')],
                              'costBeforeTax': row[self.header.index('CostBeforeTax')],
                              'credits': row[self.header.index('Credits')],
                              'taxAmount': row[self.header.index('TaxAmount')],
                              'totalCost': row[self.header.index('TotalCost')]}
                    # for col in columns:
                        # fix TypeError: __init__() got an unexpected keyword argument 'LinkedAccountId'
                        # record[col] = row[self.header.index(col)]
                    self.rows.append(record)

    def __repr__(self):
        return '<CSVReader %r>' % self.csvin


if __name__ == '__main__':
    csvin = '412764460734-aws-cost-allocation-ACTS-2017-03.csv'
    reader = CSVReader(csvin)
    # print 5 rows
    for i in xrange(15):
        print reader.rows[i]
