"""Private review plots only; requires optional figure dependencies and soundfile."""
from pathlib import Path
import numpy as np,pandas as pd,soundfile as sf,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1];p=root/'prototype/pvc/private/quality-review';raw=root/'prototype/pvc/private/edinburgh'
for sid in [1,6,9]:
 fig,axes=plt.subplots(4,2,figsize=(15,12))
 for i,code in enumerate([19,20,21,22]):
  stem=f'MKH800_{code}_{sid:04d}';y,sr=sf.read(raw/'clear_speech_wavs'/(stem+'.wav'));t=np.arange(len(y))/sr
  ax=axes[i,0];ax.plot(t,y,lw=.4);ax.set_title(stem+' waveform');ax.set_ylabel('Amplitude');ax.set_xlabel('Seconds')
  if code==20 and sid in [6,9]:ax.axvline({6:2.94,9:3.3}[sid],color='red',label='TextGrid end');ax.legend()
  ax=axes[i,1];ax.specgram(y,NFFT=512,Fs=sr,noverlap=384,cmap='Greys',vmin=-100,vmax=-35);ax.set_ylim(0,650)
  for name,col,label in [('opensmile','opensmile_hz','openSMILE LLD'),('praat','praat_hz','Praat AC 60–400')]:
   d=pd.read_csv(p/(stem+'-'+name+'.csv'));v=d[col].where(d[col]>0);ax.plot(d.time_s,v,'.',ms=2,label=label)
  ax.set_title('Spectrogram and automated pitch (neither is a human reference)');ax.set_ylabel('Hz');ax.set_xlabel('Seconds');ax.legend(fontsize=8)
 fig.tight_layout();fig.savefig(p/f'review-{sid:04d}.png',dpi=120);plt.close(fig)
