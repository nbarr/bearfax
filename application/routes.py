# -*- coding: utf-8 -*-

import os.path as path
from flask import send_from_directory, request, jsonify, render_template
from application.api.base import response_error, response_not_found
from application.api.websockets import configure_websockets


def configure_routes(app):
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            path.join(app.root_path, 'static', 'images'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    #
    # Application errors
    #
    @app.errorhandler(500)
    def error_500(e):
        app.logger.exception(e)

        if request.is_xhr:
            return jsonify(response_error(message='Server unable to process your request.'))
        else:
            return render_template('errors/500.html'), 500

    @app.errorhandler(404)
    def error_404(e):
        app.logger.exception(e)

        if request.is_xhr:
            return jsonify(response_not_found(message='Resource not found.'))
        else:
            return render_template('errors/404.html'), 404
    #
    # Application views
    #

    from application.home.views import HomeMethodView
    home_view = HomeMethodView.as_view('views.home')
    app.add_url_rule('/', view_func=home_view, methods=['GET', 'POST'])

    from application.tryagain.views import TryagainMethodView
    tryagain_view = TryagainMethodView.as_view('views.tryagain')
    app.add_url_rule('/tryagain/<token>', view_func=tryagain_view, methods=['GET', 'POST'])

    from application.process.views import ProcessMethodView
    process_view = ProcessMethodView.as_view('views.process')
    app.add_url_rule('/process/<token>', view_func=process_view, methods=['GET'])

    #
    # API
    #

    #
    # WebSockets
    #
    configure_websockets(app)
