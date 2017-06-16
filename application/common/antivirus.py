# -*- coding: utf-8 -*-

import clamd


def scan_stream(stream):
    """Scan stream-like object (that supports `read()`). After scan initial stream position restored
    """
    success, message = False, ''

    try:
        if not stream.closed:
            position = stream.tell()
            clamd_socket = clamd.ClamdUnixSocket('/var/run/clamd.scan/clamd.sock')
            result = clamd_socket.instream(stream)

            success = result and 'stream' in result and result['stream'][0].lower() == 'ok'
            message = '' if success else result['stream'][1]

            stream.seek(position)
    except Exception as ex:
        print('>> scan_stream exception:', ex)
        message = ex.msg

    return success, message
