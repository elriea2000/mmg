import pyperclip
import datetime
import sys

d=pyperclip.paste()
if d[:6]!="<html ":
    print("invalid clipboard")
    sys.exit(1)
ofn="./snapshots/snapshot_"+datetime.datetime.now().strftime("%Y%m%d%H%M")+".html"
with open(ofn,"w",encoding="utf8") as fp:
    fp.write(d)
