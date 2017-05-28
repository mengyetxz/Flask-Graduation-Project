#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/12
"""__DOC__"""

from flask import Blueprint

main_bp = Blueprint("main", __name__)

from . import views

if __name__ == '__main__':
    pass
