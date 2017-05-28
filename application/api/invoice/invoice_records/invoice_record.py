#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/24
"""__DOC__"""

from datetime import datetime
from decimal import Decimal


class InvoiceRecord(object):
    """
    pre_api_module = api_for_csv_reader
    功能：
        提供一组操作：将输入的数据进行格式转换并把PK相同的Record合并，结果有利于存入关系型数据库
    输入：
        见初始化参数说明
    初始化参数说明：
        对应CSV中需要处理的列
    输出:
        output = ??? 待定，暂未确定flask model, 目前只提供直接访问实例属性
    output_for_invoice_model = {
        "LinkedAccountId"   "1"
        "BillingDate"       "2017/01/01 0:0:0"
        "InvoiceDate"       "2017/01/01 0:0:0"
        "ProductCode"       "EC2"

        "CostBeforeTax"     "Decimal"
        "Credits"           "Decimal"
        "TaxAmount"         "Decimal"
        "TotalCost"         "Decimal"   }
    """
    def __init__(self, linkedAccountId, billingDate, invoiceDate, productCode,
                 costBeforeTax, credits, taxAmount, totalCost):
        # The four items below are PK (primary key)
        self.linkedAccountId = linkedAccountId
        self.billingDate = billingDate
        self.invoiceDate = invoiceDate
        self.productCode = productCode

        # 如果是经常性费用，则返回 True
        self.isRecurrent = self.billingDate.strftime("%Y/%m") != self.invoiceDate.strftime("%Y/%m")

        self.costBeforeTax = Decimal(costBeforeTax)
        self.credits = Decimal(credits)
        self.taxAmount = Decimal(taxAmount)
        self.totalCost = Decimal(totalCost)

    def to_dict(self):
        """
        return value for InvoiceModel
        :return:
        """
        return {"linkedAccountId": self.linkedAccountId,
                "billingDate": self.billingDate.date(),  # db.Column(db.Date)
                "invoiceDate": self.invoiceDate.date(),  # db.Column(db.Date)
                "productCode": self.productCode,
                "isRecurrent": self.isRecurrent,
                "costBeforeTax": self.costBeforeTax,
                "credits": self.credits,
                "taxAmount": self.taxAmount,
                "totalCost": self.totalCost}

    @property
    def billingDate(self):
        return self._billingDate

    @billingDate.setter
    def billingDate(self, date):
        try:
            self._billingDate = datetime.strptime(str(date), '%Y/%m/%d %H:%M:%S')
        except ValueError:
            self._billingDate = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')

    @property
    def invoiceDate(self):
        return self._invoiceDate

    @invoiceDate.setter
    def invoiceDate(self, date):
        try:
            self._invoiceDate = datetime.strptime(str(date), '%Y/%m/%d %H:%M:%S')
        except ValueError:
            self._invoiceDate = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')

    def __eq__(self, other):
        # The four items below are PK (primary key)
        if isinstance(other, InvoiceRecord) and \
           self.linkedAccountId == other.linkedAccountId and \
           self.billingDate.strftime("%Y/%m") == other.billingDate.strftime("%Y/%m") and \
           self.invoiceDate.strftime("%Y/%m") == other.invoiceDate.strftime("%Y/%m") and \
           self.productCode == other.productCode:
            return True
        else:
            return False

    def __hash__(self):
        # hash(PK)
        return hash(self.linkedAccountId + " " +
                    self.billingDate.strftime("%Y/%m") + " " +
                    self.invoiceDate.strftime("%Y/%m") + " " +
                    self.productCode)

    def __add__(self, other):
        # 如果PK不相等则不允许加法运算
        if not isinstance(other, InvoiceRecord):
            raise TypeError("'{}' is not an instance of <class InvoiceRecord>".format(other))
        if not self.__eq__(other):
            raise TypeError("Method '+' is not allowed because <PK> dont matched")
        total_costBeforeTax = self.costBeforeTax + other.costBeforeTax
        total_credits = self.credits + other.credits
        total_taxAmount = self.taxAmount + other.taxAmount
        total_totalCost = self.totalCost + other.totalCost
        return InvoiceRecord(self.linkedAccountId, self.billingDate, self.invoiceDate, self.productCode,
                             total_costBeforeTax, total_credits, total_taxAmount, total_totalCost)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __repr__(self):
        return '<InvoiceRecord %r>' % self.isRecurrent

    def __str__(self):
        return '<InvoiceRecord %s>' % self.isRecurrent

if __name__ == '__main__':
    # args = accountId = "123412341234", datatime = 2017 03
    # meta record:
    reader = [
        {'linkedAccountId': '425155429375', 'productCode': 'AmazonEC2', 'taxAmount': '0.006826', 'invoiceDate': '2017/04/04 03:26:20', 'totalCost': '1', 'credits': '0.000000', 'billingDate': '2017/03/01 00:00:00', 'costBeforeTax': '0.149548'},
        {'linkedAccountId': '425155429375', 'productCode': 'AmazonEC2', 'taxAmount': '0.006509', 'invoiceDate': '2017/04/04 03:26:20', 'totalCost': '2', 'credits': '0.000000', 'billingDate': '2017/03/01 00:00:00', 'costBeforeTax': '0.142611'},
        {'linkedAccountId': '412764460734', 'productCode': 'AmazonEC2', 'taxAmount': '0.007846', 'invoiceDate': '2017/04/04 03:26:20', 'totalCost': '3', 'credits': '0.000000', 'billingDate': '2017/03/01 00:00:00', 'costBeforeTax': '0.112955'},
        {'linkedAccountId': '412764460734', 'productCode': 'AmazonEC2', 'taxAmount': '0.040444', 'invoiceDate': '2017/04/04 03:26:20', 'totalCost': '4', 'credits': '0.000000', 'billingDate': '2017/03/01 00:00:00', 'costBeforeTax': '0.582266'},
        {'linkedAccountId': '412764460734', 'productCode': 'AmazonEC2', 'taxAmount': '-12.983402', 'invoiceDate': '2017/04/04 03:26:20', 'totalCost': '5', 'credits': '-216.300000', 'billingDate': '2017/03/01 00:00:00', 'costBeforeTax': '0.000000'}]
    # output_should_be_like = [{record_1}, {record_2}, {record_3}, ... , {record_n}]
    records = []
    for record in reader:
        records.append(InvoiceRecord(**record))

    # sum() can get two vars or one list as arguments.
    print sum([records[0], records[1]])
