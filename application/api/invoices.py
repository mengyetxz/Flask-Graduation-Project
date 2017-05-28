#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/27
"""__DOC__"""

from flask import jsonify
from flask_restful import Resource, reqparse
from ..models import InvoiceModel


class Invoices(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('invoice')

    @classmethod
    def get(cls):
        invoices = InvoiceModel.find_all()
        return jsonify([obj.to_dict() for obj in invoices])

if __name__ == '__main__':
    pass
