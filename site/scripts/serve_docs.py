#!/usr/bin/env python3
"""Local QA server with HTTP gzip, matching a compressed static deployment.

Usage: python3 site/scripts/serve_docs.py OUTPUT_DIR [PORT]
This is a loopback-only test fixture, not the production server. A plain Python
HTTP server is also supported by the site but does not compress text responses.
"""
import gzip
import io
import pathlib
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


class CompressedDocs(SimpleHTTPRequestHandler):
    def send_head(self):
        path = pathlib.Path(self.translate_path(self.path))
        if path.is_dir():
            if not urlsplit(self.path).path.endswith('/'):
                return super().send_head()
            path /= 'index.html'
        if (path.is_file() and path.suffix in {'.html', '.css', '.js', '.json', '.svg'}
                and 'gzip' in self.headers.get('Accept-Encoding', '')):
            body = gzip.compress(path.read_bytes())
            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(str(path)))
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Vary', 'Accept-Encoding')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            return io.BytesIO(body)
        return super().send_head()


if __name__ == '__main__':
    root = pathlib.Path(sys.argv[1]).resolve(strict=True)
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8766
    ThreadingHTTPServer(('127.0.0.1', port), partial(CompressedDocs, directory=root)).serve_forever()
