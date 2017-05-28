#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/20
"""__DOC__"""

from flask_restful import Resource, reqparse

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Name is required!"
                        )

    @staticmethod
    def get(name):
        return {'item': filter(lambda x: x['name'] == name, items)}

    @staticmethod
    def post(name):
        if len(filter(lambda x: x['name'] == name, items)):
            return {'message': "An item name {} already exists.".format(name)}

        args = Item.parser.parse_args()
        item = {'name': name, 'price': args['price']}
        items.append(item)
        return item

    @staticmethod
    def delete(name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item {} deleted'.format(name)}

    @staticmethod
    def put(name):
        args = Item.parser.parse_args()
        item = filter(lambda x: x['name'] == name, items)
        if not len(item):
            item = {'name': name, 'price': args['price']}
            items.append(item)
        else:
            item[0].update(args)
        return item


class ItemList(Resource):
    @staticmethod
    def get():
        return {'items': items}


if __name__ == '__main__':
    pass
