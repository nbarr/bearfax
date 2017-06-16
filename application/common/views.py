# -*- coding: utf-8 -*-

from flask import render_template
from flask.views import MethodView


class StaticPageView(MethodView):
    """View aimed to return static pages without any backend view (nevertheless frontend could interact via API).
    """

    def __init__(self, *args, **kwargs):
        self.template = kwargs.get('template')
        self.context = kwargs.get('context', {})

        if 'template' in kwargs:
            del kwargs['template']
        if 'context' in kwargs:
            del kwargs['context']

        super().__init__(*args, **kwargs)

    def get(self):
        return render_template(self.template, **self.context)
