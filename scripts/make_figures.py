"""Static publication figures from aggregate CSVs; matplotlib is needed only here."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'assets/figures';O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
df=pd.read_csv(R/'docs/results/edinburgh_paired.csv');cs=['Computer-directed','Non-native-listener-directed','Infant-directed','Speech-in-noise'];short=['Computer','Non-native listener','Infant','Noise production']
fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
for ax,m,title,unit in zip(axs,['annotated_span_s','f0_range_st'],['Annotated span','Estimated F0 percentile range'],['seconds','semitones']):
 sub=df[df.metric==m].set_index('condition').loc[cs];ax.barh(short,sub.median_difference,color='#246d7e');ax.invert_yaxis();ax.axvline(0,color='#222',lw=.8);ax.set_xlabel(f'Median paired difference from plain ({unit})');ax.set_title(title)
 for i,v in enumerate(sub.median_difference):ax.text(v,i,f' {v:+.2f}',va='center',ha='left' if v>=0 else 'right',fontsize=10)
 ax.margins(x=.3)
fig.suptitle('Edinburgh: one speaker, 25 matched sentences per contrast',fontsize=14)
fig.savefig(O/'edinburgh.svg');plt.close(fig)
df=pd.read_csv(R/'docs/results/r2spin_summary.csv');fig,axs=plt.subplots(1,2,figsize=(10,4.5),layout='constrained');labels=['Context','Context +\nspeaker','Context +\nkeyword GP','Context +\nspeaker +\nkeyword GP']
for ax,m,title in zip(axs,['accuracy','brier'],['Accuracy (higher better)','Brier score (lower better)']):
 vals=df[m];ax.bar(range(4),vals,color=['#8b969d','#8b969d','#246d7e','#246d7e']);ax.set_xticks(range(4),labels,fontsize=10);ax.set_ylim(0,1 if m=='accuracy' else .25);ax.set_title(title)
 for i,v in enumerate(vals):ax.text(i,v+.01,f'{v:.4f}',ha='center',fontsize=10)
fig.suptitle('R2SPIN: 6,400 responses, 16 listeners, 8 held-out-list folds',fontsize=13)
fig.savefig(O/'r2spin.svg');plt.close(fig)
def boxes(filename,title,items):
 # Standalone conceptual vector figure: no numerical scale or measured outcome implied.
 import html
 colors=['#e2edf1','#f6eddb','#e3efe9']
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 300" role="img"><title>{html.escape(title)}</title><rect width="1000" height="300" fill="#fff"/><text x="30" y="35" font-family="sans-serif" font-size="22" fill="#193d4a">{html.escape(title)}</text>'
 for i,(head,lines) in enumerate(items):
  x=30+i*325;svg+=f'<rect x="{x}" y="65" width="290" height="190" rx="10" fill="{colors[i]}"/><text x="{x+16}" y="100" font-family="sans-serif" font-size="18" font-weight="bold">{html.escape(head)}</text>'
  for n,line in enumerate(lines):svg+=f'<text x="{x+16}" y="{135+n*28}" font-family="sans-serif" font-size="16">{html.escape(line)}</text>'
 svg+='<text x="30" y="285" font-family="sans-serif" font-size="14" fill="#53646d">Conceptual framework — arrows/integration do not denote an implemented system.</text></svg>'
 (O/filename).write_text(svg)
def context_diagram():
 import html
 parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 480" role="img"><title>Content assessment and complementary acoustic research</title><rect width="1100" height="480" fill="white"/>']
 def text(x,y,t,size=18,weight='normal'):
  parts.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" font-weight="{weight}" fill="#193d4a">{html.escape(t)}</text>')
 def box(x,y,w,h,title,lines,color):
  parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{color}" stroke="#b5cbd1"/>');text(x+16,y+32,title,20,'bold')
  for i,line in enumerate(lines):text(x+16,y+64+i*25,line)
 text(25,34,'Paediatric VR: complementary evidence, separate contributions',24,'bold')
 box(25,170,260,125,'Recorded interaction',['Intended application context','Deployment not audited'],'#e8eef0')
 box(360,65,300,130,'Content/teamwork branch',['Speech-to-text / transcript','Contextual message assessment','Project-described existing approach'],'#e8eef0')
 box(735,65,335,130,'Behavioural evidence',['Message content and check-backs','Not a test of acoustic recognition'],'#e8eef0')
 box(360,260,300,130,'Acoustic branch · Charlie',['Local extractor implemented','Timing / F0 estimates','VR application proposed'],'#e1eee8')
 box(735,260,335,130,'Human-outcome validation',['Independent listener recognition','Speaker-side prediction untested','Future evidence gate'],'#f7eddb')
 parts.append('<path d="M285 200 H320 V130 H360 M660 130 H735" fill="none" stroke="#526a75" stroke-width="3"/>')
 parts.append('<path d="M285 260 H320 V325 H360 M660 325 H735" fill="none" stroke="#a36b13" stroke-width="3" stroke-dasharray="8 6"/>')
 text(25,433,'Part B · Kang Zhe: feedback presentation; author contribution pending. No implemented integration shown.',17)
 text(25,462,'Solid lines: project-described content flow. Dashed lines: proposed application/validation relationships.',16)
 parts.append('</svg>');(O/'context.svg').write_text(''.join(parts)+'\n')
context_diagram()
boxes('constructs.svg','Keep three different forms of evidence distinct',[('Speaking instruction',['Plain / computer / listener','An elicitation condition','Not an outcome score']),('Acoustic measurement',['Timing / pitch / level','Signal-derived descriptors','Require quality checks']),('Human outcome',['Recognized words / keywords','Specified listener + condition','Required for intelligibility'])])
boxes('roadmap.svg','Evidence gates before feedback claims',[('Gate 1 · current',['Reproduce measurements','Audit labels and uncertainty','RQ1: descriptive evidence']),('Gate 2 · next',['Verify human-labelled corpus','Speaker-disjoint evaluation','RQ2: prediction test']),('Gate 3 · future',['Consent and controlled trial','Recognition + efficiency','RQ3: intervention effect'])])
for path in O.glob('*.svg'):
 path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
print('Wrote five SVG figures')
