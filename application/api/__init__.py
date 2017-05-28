#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/18
"""__DOC__"""

from flask import Blueprint
from flask_restful import Api
from .items import Item, ItemList
from .users import UserRegister, UserModify
from .uploaded_file_manager import FileManager
from .invoice_records import RecordsMerge
from invoice_import import InvoiceImport
from invoices import Invoices

api_bp = Blueprint("api", __name__)

api = Api()
api.init_app(api_bp)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(UserRegister, '/users', endpoint='users')
api.add_resource(UserModify, '/users/<int:current_user_id>')

api.add_resource(FileManager, '/file_manager', endpoint='file_manager')
api.add_resource(InvoiceImport, '/invoices/import', endpoint='invoice_import')
api.add_resource(Invoices, '/invoices', endpoint='invoices')


# RecordsMerge 返回的值为 [<InvoiceRecord>,<InvoiceRecord>,<InvoiceRecord>...]
# 由于前端 HTTP (GET) 请求接受的响应通常为JSON格式，而 InvoiceRecord 的对象不能序列化成 JSON
# 所以在这里注册的 API 不能直接为前端调用，仅作测试目的
api.add_resource(RecordsMerge, '/test/records_merge', endpoint='records_merge')

if __name__ == '__main__':
    pass
