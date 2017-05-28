#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/12
"""__DOC__"""

from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from . import views
