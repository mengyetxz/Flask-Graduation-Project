#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/25
"""__DOC__"""

import os
from flask import current_app, jsonify
from flask_restful import Resource, reqparse
from application import csvfiles  # 这里不应该从 application 中导入 ... 待修改


class CSVFilesManager(Resource):
    @staticmethod
    def get():
        """
        返回目录 'UPLOADED_CSVFILES_DEST' 下的所有文件名及其URL
        :return: ｛文件名：URL， ...｝
        """
        file_dir = current_app.config.get('UPLOADED_CSVFILES_DEST')
        filename_list = os.listdir(file_dir)
        return jsonify({filename: csvfiles.url(filename) for filename in filename_list})

    @staticmethod
    def delete():
        """
        根据参数 filename 删除目录 'UPLOADED_CSVFILES_DEST' 下的指定的文件
        :return: 204 NO CONTENT
        """
        # parse args
        parser = reqparse.RequestParser()
        parser.add_argument('filename', required=True)
        args = parser.parse_args()
        filename = args['filename']
        # get url
        file_dir = current_app.config.get('UPLOADED_CSVFILES_DEST')
        filename_list = os.listdir(file_dir)
        if filename in filename_list:
            os.remove(os.path.join(file_dir, filename))
        return '', 204  # 204 NO CONTENT


if __name__ == '__main__':
    pass
