#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/12
"""__DOC__"""

import os
from flask import render_template, request, redirect, url_for, session, current_app, jsonify, flash
from .forms import CSVForm, csvfiles
from . import invoice_bp


@invoice_bp.route('/')
def index():
    return render_template("invoice/index.html")


@invoice_bp.route('/upload/csv', methods=['GET', 'POST'])
def upload_file():
    form = CSVForm()
    if form.validate_on_submit():
        # save file to UPLOADED_FILES_DEST
        filename = csvfiles.save(form.csvfile.data)
        # session['filename'] = filename
        # session['file_url'] = csvfiles.url(filename)
        flash(u'上传成功！')
        return redirect(url_for('.upload_file'))
    else:
        # file_url = session.get('file_url')
        # method = GET, get list of all files
        file_dir = current_app.config.get('UPLOADED_CSVFILES_DEST')
        filename_list = os.listdir(file_dir)
        files = {filename: csvfiles.url(filename) for filename in filename_list}
        return render_template('invoice/upload.html', form=form, files=files)


@invoice_bp.route('saving_to_db')
def uploaded_file():
    filename = request.args.get('filename')
    return render_template('invoice/saving_to_db.html', filename=filename)


@invoice_bp.route('/upload/file_manager')
def file_manager():
    pass


if __name__ == '__main__':
    pass
