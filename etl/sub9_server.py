#!/usr/bin/env python3

"""Find the 9 hashes needed for subscription local geo realtime updates"""

__author__ = "H. Martin"
__version__ = "0.1.0"

import argparse
import geohash
import json
import redis
from http.server import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser
from urllib.parse import urlparse, parse_qs

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class RequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def count_geohash(self, hashcode):
        return int(redis_client.get(hashcode + '.count'))

    def should_zoom_up(self, hashcode, minimum):
        start_count = self.count_geohash(hashcode[:-1])
        return start_count < minimum

    def zoom_out_slightly(self, nbrs, minimum):
        zoomed_nbrs = {}
        zcount = 0
        for n in nbrs:
            znbrs = geohash.neighbors(n)
            if n not in zoomed_nbrs:
                zoomed_nbrs[n] = self.count_geohash(n)
                zcount += zoomed_nbrs[n]
            for zn in znbrs:
                if zn not in zoomed_nbrs:
                    zoomed_nbrs[zn] = self.count_geohash(zn)
                    zcount += zoomed_nbrs[zn]
        
        znbrs = list(zoomed_nbrs.keys())
        if zcount < minimum:
            return self.zoom_out_slightly(znbrs, minimum)
        else:
            return znbrs

    def zoom_out(self, hashcode, minimum):
        start_count = self.count_geohash(hashcode)
        if start_count > minimum:
            print(str(start_count) + " > " + str(minimum))
            return [hashcode]

        nbrs = geohash.neighbors(hashcode)
        ncount = self.count_geohash(hashcode)
        for n in nbrs:
            i = self.count_geohash(n)
            ncount += i

        if ncount > minimum:
            nbrs.append(hashcode)
            return nbrs
        elif self.should_zoom_up(hashcode, minimum):
            return self.zoom_out(hashcode[:-1], minimum)
        else:
            return self.zoom_out_slightly(nbrs, minimum)
        
    def send_not_found(self, msg):
        self.send_error(404, message=msg)

    def do_GET(self):
        r = urlparse(self.path)
        query = parse_qs(r.query)
        gh = geohash.encode(float(query['lat'][0]), float(query['lon'][0]), precision=6)
        minimum = int(query['min'][0])
        subs = self.zoom_out(gh, minimum)
        resp_body = bytes(json.dumps({'subs':subs}), "utf8")
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