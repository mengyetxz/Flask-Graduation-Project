#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/25
"""__DOC__"""

from flask_wtf import FlaskForm
from .. import csvfiles
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class CSVForm(FlaskForm):
    csvfile = FileField(u'请选择要上传的文件(.csv)：', validators=[FileAllowed(csvfiles, u'只能上传CSV文件！'), FileRequired(u'空文件！')])
    submit = SubmitField(u'上传')


if __name__ == '__main__':
    pass
