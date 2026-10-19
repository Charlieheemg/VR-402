"""Proposed feasibility assignments only: no participants, audio or outcomes.

24 hypothetical listeners x 12 unique texts; 6 hypothetical talkers x 12
texts x 2 styles. Each clip is assigned twice, with no text repeated for a
listener. This small design checks logistics; it is not powered model validation.
"""
from pathlib import Path
import csv,random
ROOT=Path(__file__).resolve().parents[1]

def assignments():
    rows=[]
    for listener in range(24):
        offset=listener % 6
        style_block=(listener//6) % 2
        trials=[]
        for text in range(12):
            speaker=(text+offset)%6
            style=(text//6+style_block)%2
            trials.append(dict(listener=f'L{listener+1:02d}',text=f'T{text+1:02d}',
                               speaker=f'S{speaker+1:02d}',style=['ordinary','clear_instruction'][style]))
        random.Random(405+listener).shuffle(trials)
        rows.extend(dict(trial=i+1,**row) for i,row in enumerate(trials))
    return rows

if __name__=='__main__':
    out=ROOT/'docs/methodology/proposed-pilot-assignments.csv'
    rows=assignments()
    with out.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");writer.writeheader();writer.writerows(rows)
    print(f'{len(rows)} hypothetical trial assignments; no outcomes generated')
