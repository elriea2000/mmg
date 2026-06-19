from bs4 import BeautifulSoup
import json
import os
import re
import csv
import glob
import sys

# 絵文字リスト
with open("emojis.csv","r",encoding="utf8") as fp:
    reader=csv.reader(fp)
    emojis = [r for r in reader]

emojis_mbk=[e for e in emojis if e[1]!=""]
emojis_mbk_inv={e[1]:e[0] for e in emojis_mbk}

# ターゲットファイル
# fn="./snapshots/snapshot_202606172215.html"
if len(sys.argv)>1:
    fn=sys.argv[1]
else:
    fn=glob.glob("./snapshots/snapshot_*.html")[-1]
tstamp=re.split("(\.|_)",os.path.split(fn)[-1])[2]

# 無視するレス番一覧（削除されたものとか）
ignore_id=[0,1,2,26,49,56,67,70,71,72,85,97,109]

with open(fn,"r",encoding="utf8") as fp:
    bs = BeautifulSoup(fp,"html.parser")

# レスたち
cards = bs.select("div.thread-messages>div")

data={"tstamp":tstamp,"data":[]}

for ic,card in enumerate(cards):
    # 無視
    if ic in ignore_id: continue
    # リンクのインラインを削除
    for b in card.select("div[class=\"my-1 h-32 w-full max-w-xl rounded-md border bg-muted/80\"]"):
        b.replace_with("")
    # 名前など抽出
    cbody=card.findChildren("div", recursive=False)[1].findChild("div").findChildren("div", recursive=False)[0]
    for b in cbody.find_all("br"):
        b.replace_with("\n")
    cbodys=[re.sub("(^\s+|\s+$)","",r) for r in cbody.get_text().split("\n") if r!=""]
    cbtitle=re.sub("(^・|)","",cbodys[0])
    cbinfo="\n".join(cbodys[1:])
    # 絵文字抽出
    btns = card.select("div:nth-of-type(2)>div:nth-of-type(2)>button")
    dbtns=[]
    for btn in btns:
        spans = btn.select("span")
        bsrc = spans[0].select_one("img").attrs["src"]
        if bsrc[:26]=="https://storage.mebuki.moe":
            balt=emojis_mbk_inv[bsrc]
        else:
            balt=spans[0].select_one("img").attrs["alt"]
        
        dbtns.append([
            balt,
            bsrc,
            int(spans[1].text)
        ])
    data["data"].append([ic,cbtitle,cbinfo, dbtns])

ofn="./outputs/output_"+tstamp+".json"
with open(ofn,"w",encoding="utf8") as fp:
    json.dump(data,fp,indent=2,ensure_ascii=False)
