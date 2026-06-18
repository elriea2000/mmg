import glob
import csv

emojis_fns=glob.glob("emojis_src/emojis_*.csv")

data=[]

for fn in emojis_fns:
    with open(fn,"r",encoding="utf8") as fp:
        reader=csv.reader(fp)
        data=data+[r for r in reader]

ndata=[]
ndd=[]

for d in data:
    if not d[0] in ndd:
        ndd.append(d[0])
        ndata.append(d)

with open("emojis.csv","w",encoding="utf8",newline="") as fp:
    writer=csv.writer(fp)
    writer.writerows(ndata)
