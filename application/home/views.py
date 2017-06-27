# -*- coding: utf-8 -*-

import uuid
import PyPDF2
from werkzeug.utils import secure_filename
from flask import render_template, current_app, request
from flask.views import MethodView
from application.config import settings
from application.config.messages import get_message
from application.extensions import recaptcha
from application.home.forms import HomeUploadForm
from application.common.s3files import s3_upload_file, s3_get_file, s3_delete_file
from application.common.antivirus import scan_stream
from application.common.formatters import safe_join
from application.common.filters import is_ascii, strip_non_numeric
from application.models import Task, User
from application.database import session
from application.common.token_serialize import serialize
from application.common.mailer import send_confirmation_mail


class HomeMethodView(MethodView):
    def get(self):
        return render_template('home.html', form=HomeUploadForm())

    def post(self):
        form = HomeUploadForm()

        if form.validate_on_submit() and recaptcha.verify():
            task = None
            file = form.document.data
            task_uid = uuid.uuid4().hex
            filename = '{}_{}'.format(task_uid, secure_filename(file.filename))
            prefix = form.email.data[0]
            if not is_ascii(prefix):
                prefix = '_'
            prefix = safe_join([prefix, form.email.data], '/', remove_duplicated_separators=True)

            try:
                pdf_reader = PyPDF2.PdfFileReader(file.stream)
            except Exception as ex:
                current_app.logger.exception(ex)
                form.document.errors.append(get_message('INVALID_DOCUMENT'))
                return render_template('home.html', form=form)

            pdf_pages_count = pdf_reader.getNumPages()

            if pdf_pages_count > settings.MAX_PDF_PAGES:
                form.document.errors.append(get_message('MAX_PDF_PAGES_ALLOWED',
                                                        pages=settings.MAX_PDF_PAGES, actual=pdf_pages_count))
                return render_template('home.html', form=form)

            try:
                file.stream.seek(0)

                no_virus, message = scan_stream(file.stream)
                if not no_virus:
                    form.document.errors.append(get_message('DOCUMENT_CONTAINS_VIRUSES',
                                                            document=file.filename, message=message))
                    return render_template('home.html', form=form)

                file.stream.seek(0)

                s3_upload_file(
                    current_app.config['AWS_ACCESS_KEY_ID'], current_app.config['AWS_SECRET_KEY_ID'],
                    current_app.config['AWS_BUCKET'], file.stream, filename, prefix
                )

                obj, url, metadata = s3_get_file(
                    current_app.config['AWS_ACCESS_KEY_ID'], current_app.config['AWS_SECRET_KEY_ID'],
                    current_app.config['AWS_BUCKET'], filename, prefix
                )

                user = session.query(User).filter(User.email == form.email.data).first()

                if not user:
                    user = User(
                        email=form.email.data,
                        register_ip=request.headers.get('X-Forwarded-For', request.remote_addr)
                    )
                    session.add(user)
                    session.flush()

                task = Task(
                    user=user,
                    task_uid=task_uid,
                    document_orig_name=file.filename,
                    document_name=filename,
                    prefix=prefix,
                    status=Task.STATUS_UNCONFIRMED,
                    url=url,
                    fax=strip_non_numeric(form.fax.data),
                    pages_count=pdf_pages_count
                )
                session.add(task)
                session.commit()

                token = serialize({'user_id': user.id, 'task_id': task.id, 'task_uid': task.task_uid})
                send_confirmation_mail([form.email.data], task, token)
            except Exception as ex:
                current_app.logger.exception(ex)
                session.rollback()

                s3_delete_file(
                    current_app.config['AWS_ACCESS_KEY_ID'], current_app.config['AWS_SECRET_KEY_ID'],
                    current_app.config['AWS_BUCKET'], filename, prefix
                )

                if task and task.id:
                    session.delete(task)
                    session.commit()

                raise

            return render_template('verify_email.html')

        if not request.form.get('g-recaptcha-response', '').strip():
            form.errors['g-recaptcha-response'] = [get_message('RECAPTCHA_REQUIRED')]

        return render_template('home.html', form=form)
