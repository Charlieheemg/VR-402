"""Inspect downloaded public documentation/schema, not outcomes or audio.

No extraction to arbitrary archive paths, no model fitting, no label publication.
See dataset-decision.md for pinned public download URLs and unresolved gates.
"""
from pathlib import Path
import json,hashlib,tarfile
ROOT=Path(__file__).resolve().parents[1]

def audit():
    private=ROOT/'prototype/pvc/private/dataset-audit'
    archive=private/'cpc1-labels.tar.gz'
    assert hashlib.md5(archive.read_bytes()).hexdigest()=='db62ba9c018dca184453fc60901519df'
    schema=[]
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.endswith('.json') and not Path(member.name).name.startswith('._'):
                rows=json.load(tar.extractfile(member))
                schema.append(dict(file=member.name,rows=len(rows),fields=sorted(rows[0])))
        license_text=tar.extractfile('clarity_CPC1_data/LICENSE').read().decode()
        speech_license=tar.extractfile('clarity_CPC1_data/Clarity_speech_database_license_1.00.txt').read().decode()
        assert 'Attribution-ShareAlike 4.0' in license_text
        assert 'You may not replay' in speech_license
    record=json.loads((private/'cpc1-record.json').read_text())
    result=dict(checked_date='2026-10-19',cpc1_record='https://zenodo.org/records/17046604',
        archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        landing_record_license=record['metadata']['license']['id'],
        archive_license='CC BY-SA 4.0 with separate Clarity speech database license 1.00',
        label_files=schema,audio_downloaded=False,audio_label_join_verified=False,
        models_trained=0,outcome_values_exported=False,
        slusi_readme_sha256=hashlib.sha256((private/'slusi-readme.txt').read_bytes()).hexdigest())
    (ROOT/'docs/results/dataset-access-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':audit()
