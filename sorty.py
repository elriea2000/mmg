'''
sorty
sort by specific score
'''
import json
import csv
import re
import glob
import sys

#fn="./outputs/output_202606162329.json"
fn=glob.glob("./outputs/output_*.json")[-1]

target=":soudane:"
if len(sys.argv)>1:
    target=sys.argv[1]

with open(fn,"r",encoding="utf8") as fp:
    _data = json.load(fp)
data=_data["data"]

cnt=[0]*len(data)
for i,d in enumerate(data):
    for r in d[3]:
        if r[0]==target:
            cnt[i]=int(r[2])

dsp=[[re.sub("^(.+?)(\\(|（).*$","\\1",data[i][1]),
    #   "<"+target+">",
      cnt[i]] for i in range(len(cnt))]

dsps=sorted(dsp,key=lambda x:x[1],reverse=True)

with open("rsorty_"+re.sub("[^a-zA-Z0-9_.-]","",target)+".txt","w",encoding="utf8",newline="") as fp:
    writer=csv.writer(fp,delimiter="\t")
    writer.writerows(dsps)
