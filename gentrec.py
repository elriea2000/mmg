#gentrec.py

import glob
import io

fns=glob.glob("./outputs/output_*.json")

sout=io.StringIO()
sout.write("const trec=\n")
sout.write("[\n")
for i,fn in enumerate(fns):
    with open(fn,"r",encoding="utf8") as fp:
        _d=fp.read()
    sout.write(_d)
    if i<len(fns)-1: sout.write(",")
    sout.write("\n")
sout.write("]\n")

with open("./viewer/mmgp_viewer_src.js","w",encoding="utf8") as fp:
    fp.write(sout.getvalue())
