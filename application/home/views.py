# -*- coding: utf-8 -*-

from flask import render_template, request
from flask.views import MethodView
from application.home.forms import HomeUploadForm


class HomeMethodView(MethodView):
    def get(self):
        return render_template('home.html', form=HomeUploadForm())

    def post(self):
        form = HomeUploadForm()

        if form.validate_on_submit():
            pass
            # TODO: Get stream from file storage
            # TODO: Upload file to S3
            # TODO: Add it to the queue

        return render_template('home.html', form=form)
