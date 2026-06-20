'''
dispall
pickup all score
'''
import json
import csv
import re
import glob
from functools import *
import argparse

parser=argparse.ArgumentParser("dispall")
parser.add_argument("-z","--zip",action='store_true',help="output as zipfile")
parser.add_argument("-t","--txt",action='store_true',help="output as text")
args=parser.parse_args()

ZIP_ON=False
if args.zip:
    ZIP_ON=True
elif args.txt:
    ZIP_ON=False

def totag(t):
    if t[0]==":":
        return "<"+t+">"
    else:
        return t
def fcname(t):
    return re.sub("^(.+?)(\\(|（).*$","\\1",t)

class BRecord:
    def __init__(self, name="", count=0):
        self.name=name
        self.count=count
class Record:
    def __init__(self,name="",info="",sr=None, ar=None):
        self.name=name
        self.info=info
        if sr==None:
            self.sr=BRecord(":soudane:", 0)
        else:
            self.sr=sr
        if ar==None:
            self.ar=[]
        else:
            self.ar=ar

#fn="./outputs/output_202606162329.json"
fn=glob.glob("./outputs/output_*.json")[-1]

with open(fn,"r",encoding="utf8") as fp:
    _data = json.load(fp)
tstamp=_data["tstamp"]
data=_data["data"]

cnts=[]
for i,d in enumerate(data):
    rec = Record(d[1],d[2])
    for r in d[3]:
        if r[0]==":soudane:":
            rec.sr.count=r[2]
        rec.ar.append(BRecord(r[0],r[2]))
    rec.ar=sorted(rec.ar,key=lambda x:x.count, reverse=True)
    #cnts.update({rec.name: rec})
    cnts.append(rec)

dsp=[
    [fcname(r.name), totag(r.sr.name), r.sr.count] + 
        reduce(lambda a,b:a+b,[[totag(s.name),s.count] for s in r.ar if s.name!=":soudane:"],[])
    for r in cnts]

dsps=sorted(dsp,key=lambda x:x[2],reverse=True)

if ZIP_ON:
    import zipfile
    import io

    sout=io.StringIO()
    writer=csv.writer(sout,delimiter="\t")
    writer.writerows(dsps)

    # 文字列のデータ
    text_content = sout.getvalue()

    # ZIPファイルを作成して文字列を書き込む
    with zipfile.ZipFile('rdispall.txt.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('rdispall.txt', text_content)
else:
    # 重い
    with open("rdispall.txt","w",encoding="utf8",newline="") as fp:
        writer=csv.writer(fp,delimiter="\t")
        writer.writerows(dsps)
