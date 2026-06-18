'''
disp2
pickup soudane and the other largest score
'''
import json
import csv
import re
import glob

#fn="./outputs/output_202606162329.json"
fn=glob.glob("./outputs/output_*.json")[-1]

with open(fn,"r",encoding="utf8") as fp:
    _data = json.load(fp)
tstamp=_data["tstamp"]
data=_data["data"]

cnt=[0]*len(data)
snd=[["",0] for r in range(len(data))]
cntd={r[0]:i for i,r in enumerate(data)}
for i,d in enumerate(data):
    for r in d[3]:
        if r[0]==":soudane:":
            cnt[i]=int(r[2])
        else:
            if snd[i][1]<r[2]:
                if r[0][0]==":":
                    snd[i][0]="<"+r[0]+">"
                else:
                    snd[i][0]=r[0]
                snd[i][1]=r[2]

dsp=[[re.sub("^(.+?)(\\(|（).*$","\\1",data[i][1]),"<:soudane:>",cnt[i],snd[i][0],snd[i][1]] for i in range(len(cnt))]

dsps=sorted(dsp,key=lambda x:x[2],reverse=True)

with open("rdisp2.txt","w",encoding="utf8",newline="") as fp:
    writer=csv.writer(fp,delimiter="\t")
    writer.writerows(dsps)
