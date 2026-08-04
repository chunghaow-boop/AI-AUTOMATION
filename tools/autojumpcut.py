#!/usr/bin/env python3
"""Auto jump-cut: detect silences, cut them out, concat. The Recipe 7 primitive.
Usage: python3 autojumpcut.py in.mp4 out.mp4 [--db -32] [--min 0.30] [--pad 0.05]"""
import subprocess, sys, re, os, tempfile, argparse

def probe_dur(p):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
        '-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())

def find_silences(path, db, mindur):
    out = subprocess.run(['ffmpeg','-hide_banner','-i',path,'-af',
        f'silencedetect=n={db}dB:d={mindur}','-f','null','-'],
        capture_output=True, text=True).stderr
    starts=[float(m) for m in re.findall(r'silence_start: ([\d.]+)', out)]
    ends  =[float(m) for m in re.findall(r'silence_end: ([\d.]+)', out)]
    if len(ends)<len(starts): ends.append(probe_dur(path))
    return list(zip(starts,ends))

def keep_ranges(dur, silences, pad):
    keep=[]; cur=0.0
    for s,e in silences:
        s=min(dur,s+pad); e=max(0,e-pad)          # pad = leave a breath, avoid clipping words
        if s-cur>0.12: keep.append((cur,s))       # drop fragments under 0.12s
        cur=max(cur,e)
    if dur-cur>0.12: keep.append((cur,dur))
    return keep

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('inp'); ap.add_argument('out')
    ap.add_argument('--db',type=int,default=-32)      # threshold; quieter room = lower
    ap.add_argument('--min',type=float,default=0.30)  # min silence length to cut
    ap.add_argument('--pad',type=float,default=0.05)  # breath kept at each edge
    a=ap.parse_args()
    dur=probe_dur(a.inp)
    sil=find_silences(a.inp,a.db,a.min)
    keep=keep_ranges(dur,sil,a.pad)
    if not keep: print("nothing to keep — threshold too aggressive"); sys.exit(1)
    kept=sum(e-s for s,e in keep)
    tmp=tempfile.mkdtemp(); parts=[]
    for i,(s,e) in enumerate(keep):
        p=os.path.join(tmp,f'p{i:04d}.mp4'); parts.append(p)
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s),'-to',str(e),'-i',a.inp,
            '-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','192k',
            '-avoid_negative_ts','make_zero',p],check=True)
    lst=os.path.join(tmp,'l.txt')
    open(lst,'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,
        '-c:v','libx264','-preset','medium','-crf','19','-c:a','aac','-b:a','192k',a.out],check=True)
    print(f"in {dur:.1f}s -> out {kept:.1f}s  |  {len(sil)} silences removed  "
          f"|  {len(keep)} cuts  |  {100*(1-kept/dur):.0f}% tightened")

if __name__=='__main__': main()
