#!/usr/bin/env python3

"""Find the 9 hashes needed for subscription local geo realtime updates"""

__author__ = "H. Martin"
__version__ = "0.1.0"

import argparse
import Geohash
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser
from urllib.parse import urlparse, parse_qs


class RequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def send_not_found(self, msg):
        self.send_error(404, message=msg)

    def do_GET(self):
        r = urlparse(self.path)
        query = parse_qs(r.query)
        geohash = Geohash.encode(float(query['lat'][0]), float(query['lon'][0]), precision=6)
        resp_body = bytes(geohash, "utf8")
        self.send_response(200)
        self.send_header('content-length', len(resp_body))
        self.send_header('content-type', 'plain/text')
        self.end_headers()
        self.wfile.write(resp_body)

    do_POST = do_GET
    do_PUT = do_GET


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080)
    args = parser.parse_args()
    server = HTTPServer(('', args.port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()