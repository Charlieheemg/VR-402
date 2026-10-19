"""Local-only server; no dependency installation or internet required."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
root=Path(__file__).resolve().parents[1]/'private/edinburgh'
print('Open http://127.0.0.1:8765/demo/ — Control-C to stop',flush=True)
ThreadingHTTPServer(('127.0.0.1',8765),partial(SimpleHTTPRequestHandler,directory=str(root))).serve_forever()
