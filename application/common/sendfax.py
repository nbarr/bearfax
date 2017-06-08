# -*- coding: utf-8 -*-

from twilio.rest import Client
from twilio.rest.fax import Fax


def get_fax_client(sid, token):
    client = Client(sid, token)
    return Fax(client)


def send_fax(sid, token, to, from_, pdf_url):
    fax_client = get_fax_client(sid, token)
    fax = fax_client.faxes.create(from_=from_, to=to, media_url=pdf_url)
    return fax


def list_faxes(sid, token, to):
    fax_client = get_fax_client(sid, token)
    return fax_client.faxes.list(to=to)


def get_fax(sid, token, fax_id):
    fax_client = get_fax_client(sid, token)
    fax = fax_client.faxes.get(fax_id)

    if not fax:
        return None

    return fax.fetch()
