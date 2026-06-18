#parseemojiinfo

from bs4 import BeautifulSoup
import csv

with open("emojis.html","r",encoding="utf8") as fp:
    bs=BeautifulSoup(fp,"html.parser")

bcategories=bs.select("em-emoji-picker>template>section>div:nth-of-type(1)>div>div:nth-of-type(2)>div")

emojis=[]

#bcategory=bcategories[1]
for bcategory in [bcategories[1]]:
    buttons=bcategory.select("div:nth-of-type(2)>div>button")
    for button in buttons:
        timg=button.select_one("img")
        emojis.append([
            timg.attrs["alt"],
            timg.attrs["src"]
        ])

for bcategory in bcategories[2:]:
    buttons=bcategory.select("div:nth-of-type(2)>div>button")
    for button in buttons:
        button.attrs["aria-label"]
        emojis.append([
            button.attrs["aria-label"],
            ""
        ])


with open("emojis.csv","w",encoding="utf8",newline="") as fp:
    writer=csv.writer(fp)
    writer.writerows(emojis)
