# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import mechanize
import json
import codecs

url = "https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_home"

v = {"year":  0, "career": 1, "dept":  2,
     "level": 3, "text":   4, "teach": 5,
     "week":  6, "mtg":    7, "lang":  8}

t = ["obligatory", "code", "title", "previous", "year", "credits",
     "hours", "prac_hours", "time", "prac_time", "location",
     "prac_location", "professor", "prac_professor", "department",
     "number_outter_dept", "number_available", "number_waiting",
     "language", "note"]

br = mechanize.Browser()
br.open(url)

forms = [c for c in br.forms()]
contents = forms[2].controls[v["dept"]].get_items()

depts = {}
for i in range(len(contents) - 1):
    depts[contents[i].attrs["value"]] = contents[i].attrs["contents"]

for deptCode in depts.keys():
    forms[2]["v_dept"] = [deptCode]
    br.form = forms[2]
    response = br.submit()
    soup = BeautifulSoup(response.read())
    td = soup.find_all("td")[106:-5]

    result = []
    for i in range(len(td) / 20 - 1):
        if i == len(td) / 20 - 1:
            result.append(td[-20:])
            break
        else:
            p = 20 * i
            result.append(td[p + 1:p + 21])

    raw_data = {}
    for r in result:
        for i in range(len(r)):
            raw_data[t[i]] = r[i].text
        json_data = json.dumps(raw_data, indent=4,
                               separators=(',', ': '),
                               ensure_ascii=False)
        f = codecs.open("nchu.json", "a", encoding='utf-8')
        f.write("%s,\n" % (json_data))
        f.close()
