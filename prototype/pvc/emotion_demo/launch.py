"""Serve the built offline page on loopback; needs no external connection."""
import argparse
import functools
import http.server
import sys
import webbrowser
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--no-browser',action='store_true')
parser.add_argument('--port',type=int,default=8043)
args=parser.parse_args()
page = Path(__file__).resolve().parent/'private/demo/index.html'
if not page.is_file():
    sys.exit('Demo has not been built. Install requirements-lock.txt, then run: python3 build.py --download')
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(page.parent))
try:
    server=http.server.ThreadingHTTPServer(('127.0.0.1',args.port),handler)
except OSError as error:
    sys.exit(f'Cannot start local demo: {error}. Try --port 8044.')
url=f'http://127.0.0.1:{args.port}/'
print(f'Offline demo: {url} (Ctrl-C to stop)',flush=True)
if not args.no_browser:
    webbrowser.open(url)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
