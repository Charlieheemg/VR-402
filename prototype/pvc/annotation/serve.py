"""Local PVC annotation. Standard library only; recordings never leave localhost."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
from pathlib import Path
import random
import re
import threading
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
FIELDS = ['clip_id', 'rater_id', 'pvc_score', 'notes', 'timestamp',
          'rating_status', 'audio_sha256', 'definition_version']


class Study:
    def __init__(self, clips, output):
        self.output = Path(output)
        self.lock = threading.Lock()
        self.clips = {}
        for path in sorted(Path(clips).glob('*')):
            if path.is_file() and path.suffix.lower() == '.wav':
                key = path.stem
                if key in self.clips:
                    raise ValueError(f'Duplicate clip ID: {key}')
                self.clips[key] = {'path': path, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        if not self.clips:
            raise ValueError('No WAV clips found directly in the supplied folder')
        self.output.mkdir(parents=True, exist_ok=True)

    def rater_path(self, rater):
        if not isinstance(rater, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', rater):
            raise ValueError('Use a pseudonymous rater ID: 1–64 letters, digits, underscores or hyphens')
        return self.output / f'{rater}.csv'

    def verified_audio(self, clip):
        """Return exactly the bytes checked against this study's frozen hash."""
        data = self.clips[clip]['path'].read_bytes()
        if hashlib.sha256(data).hexdigest() != self.clips[clip]['sha256']:
            raise ValueError('Audio changed while the study was running. Restore the original clip or start a new study; rating rejected.')
        return data

    def rows(self, rater):
        path = self.rater_path(rater)
        if not path.exists():
            return []
        with path.open(newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        for row in rows:
            if row['rater_id'] != rater:
                raise ValueError('Rater ID differs only by case from an existing ID. Use a distinct ID.')
            if row['clip_id'] in self.clips and row['audio_sha256'] != self.clips[row['clip_id']]['sha256']:
                raise ValueError('Audio changed for an existing clip ID. Use a new study output folder; do not mix ratings.')
        return rows

    def save(self, body):
        rater, clip = body.get('rater_id'), body.get('clip_id')
        path = self.rater_path(rater)
        if not isinstance(clip, str) or clip not in self.clips:
            raise ValueError('Unknown clip ID')
        score, status = body.get('pvc_score'), body.get('rating_status')
        if status == 'rated':
            if type(score) is not int or score not in range(1, 6):
                raise ValueError('Select a score from 1 to 5')
        elif status == 'unrateable':
            if score is not None:
                raise ValueError('Unrateable clips must have a blank score')
        else:
            raise ValueError('Unknown rating status')
        notes = body.get('notes', '')
        if not isinstance(notes, str) or len(notes) > 2000:
            raise ValueError('Notes must be text, at most 2000 characters')
        # Recheck immediately before persistence, including unrateable responses.
        # Audio serving also checks the same bytes, so changed content is never served.
        self.verified_audio(clip)
        row = dict(clip_id=clip, rater_id=rater, pvc_score=score if score is not None else '',
                   notes=notes, timestamp=datetime.now(timezone.utc).isoformat(), rating_status=status,
                   audio_sha256=self.clips[clip]['sha256'], definition_version='PVC v0.1')
        rows = self.rows(rater)
        if any(r['clip_id'] == clip for r in rows):
            raise ValueError('This clip already has a saved response for this rater. Reload to resume.')
        rows.append(row)
        # Handler lock + atomic replacement avoids partial CSVs and duplicate saves.
        temp = path.with_suffix('.csv.tmp')
        with temp.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
            f.flush()
            import os
            os.fsync(f.fileno())
        temp.replace(path)
        return row


def make_server(study, port=8765):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Do not print rater IDs or clip URLs into terminal logs.

        def reply(self, data, mime='application/json', status=200, download=False):
            if not isinstance(data, bytes):
                data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            if download:
                self.send_header('Content-Disposition', 'attachment; filename="pvc_ratings.csv"')
            self.end_headers()
            self.wfile.write(data)

        def local_request(self):
            allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
            if self.headers.get('Host') not in allowed:
                raise ValueError('Use the localhost URL printed by the server')
            origin = self.headers.get('Origin')
            if origin and origin not in {'http://' + host for host in allowed}:
                raise ValueError('Cross-origin requests are not supported')

        def do_GET(self):
            try:
                self.local_request()
                url = urlparse(self.path)
                query = parse_qs(url.query)
                if url.path in ('/', '/app.js'):
                    name = 'index.html' if url.path == '/' else 'app.js'
                    mime = 'text/html; charset=utf-8' if name.endswith('.html') else 'text/javascript; charset=utf-8'
                    self.reply((HERE/name).read_bytes(), mime)
                elif url.path == '/api/session':
                    rater = query.get('rater_id', [''])[0]
                    rows = study.rows(rater)
                    done = {r['clip_id'] for r in rows}
                    remaining = [key for key in study.clips if key not in done]
                    random.SystemRandom().shuffle(remaining)
                    self.reply(dict(clips=remaining, total=len(study.clips), completed=len(done & study.clips.keys())))
                elif url.path == '/audio':
                    clip = query.get('clip_id', [''])[0]
                    if clip not in study.clips:
                        raise ValueError('Unknown clip ID')
                    self.reply(study.verified_audio(clip), 'audio/wav')
                elif url.path == '/export':
                    rows = study.rows(query.get('rater_id', [''])[0])
                    stream = io.StringIO(newline='')
                    writer = csv.DictWriter(stream, fieldnames=FIELDS)
                    writer.writeheader()
                    writer.writerows(rows)
                    self.reply(stream.getvalue().encode('utf-8'), 'text/csv; charset=utf-8', download=True)
                else:
                    self.reply({'error':'Not found'}, status=404)
            except (ValueError, OSError) as error:
                self.reply({'error':str(error)}, status=400)

        def do_POST(self):
            try:
                self.local_request()
                if self.path != '/api/rating':
                    self.reply({'error':'Not found'}, status=404)
                    return
                if self.headers.get('Content-Type') != 'application/json':
                    raise ValueError('Expected JSON')
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 16000:
                    raise ValueError('Invalid request length')
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError('Expected a JSON object')
                with study.lock:
                    row = study.save(body)
                self.reply({'saved':True, 'timestamp':row['timestamp']})
            except (ValueError, OSError) as error:
                self.reply({'error':str(error)}, status=400)

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clips', type=Path, required=True, help='Folder of approved single-speaker WAV clips')
    parser.add_argument('--output', type=Path, default=HERE.parent/'private/annotation')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    try:
        study = Study(args.clips, args.output)
        server = make_server(study, args.port)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(f'Open http://127.0.0.1:{server.server_port} — {len(study.clips)} clips', flush=True)
    print(f'Ratings save immediately to {study.output.resolve()}. Stop with Ctrl-C.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
