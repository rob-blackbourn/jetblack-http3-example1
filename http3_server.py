"""Example server"""

import asyncio
import logging
import os
import sys

from bareasgi import Application, text_writer
import bareutils.header as header
import bareutils.response_code as response_code
from hypercorn.asyncio import serve
from hypercorn.config import Config

logging.basicConfig(level=logging.DEBUG)

async def http_request_callback(scope, info, matches, content):
    if scope['scheme'] == 'http':
        host, _port = header.host(scope['headers'])
        url = b'https://' + host + b'/index.html'
        return response_code.TEMPORARY_REDIRECT, [(b'location', url)]

    text = f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>HTTP/3 Example</title>
  </head>
  <body>
    This is http/{scope['http_version']}
  </body>
</html>
"""
    headers = [
        (b'content-type', b'text/html'),
        (b'content-length', str(len(text)).encode())
    ]
    return response_code.OK, headers, text_writer(text)

app = Application()
app.http_router.add({'GET'}, '/index.html', http_request_callback)
app.http_router.add({'GET'}, '/', http_request_callback)

config = Config()
config.insecure_bind = [ '0.0.0.0:80' ]
config.bind = [ '0.0.0.0:443' ]
config.quic_bind = [ '0.0.0.0:443' ]
config.certfile = sys.argv[1]
config.keyfile = sys.argv[2]

asyncio.run(serve(app, config))