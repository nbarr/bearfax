# -*- coding: utf-8 -*-

import clamd


def scan_stream(stream):
    """Scan stream-like object (that supports `read()`). After scan initial stream position restored
    """
    success, message = True, ''

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

        # if ex.args and len(ex.args) > 0:
        #     message = ex.args[0]
        # else:
        #     message = getattr(ex, 'msg', '')

    return success, message
