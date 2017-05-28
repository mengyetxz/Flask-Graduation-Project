#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/12
"""__DOC__"""

from flask import jsonify, request, render_template
from . import main_bp


stores = [{
    'name': 'My Store',
    'items': [{'name': 'my item', 'price': '15.99'}]
}]


@main_bp.route('/')
def home():
    return render_template('main.html')


# post /store data: {name :}
@main_bp.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# get /store/<name> data: {name:}
@main_bp.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


# get store
@main_bp.route('/store', methods=['GET'])
def get_stores():
    return jsonify(stores)


# post /store/<name> data: {name:}
@main_bp.route('/store/<string:name>', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


# get /store/<name>/item data: {name:}
@main_bp.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


if __name__ == '__main__':
    pass
