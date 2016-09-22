import requests
from lxml import etree
URL_PREFIX = "http://www.elections.gov.hk/legco2016/eng"
SELECT_XPATH = "//select[@name=\"menu1\"]"
r = requests.get(URL_PREFIX + "/tt_fc_FC.html")
root = etree.HTML(r.text)
options = root.xpath(SELECT_XPATH)[0].xpath("option")
categories = []
all_totals = []
all_percentages = []
times = []
for option in options:
    category = option.text
    categories.append(category)
    r_2 = requests.get(URL_PREFIX + "/" + option.attrib["value"])
    root_2 = etree.HTML(r_2.text)
    table = root_2.xpath(SELECT_XPATH)[0].getparent().getparent().getparent()
    percentages = []
    totals = []
    temp_times = []
    for row in table.xpath('tr')[2:]:
        texts  = [td.text for td in row.xpath('td')]
        time, total, rate = texts[0], int(texts[1].replace(",", "")), float(texts[2].replace("%", ""))
        if len(times) == 0:
            temp_times.append(time)
        percentages.append(rate)
        totals.append(total) 

    if len(times) == 0:
        times = temp_times
    if len(totals) == 0:
        totals = [0] * len(times)
    if len(percentages) == 0:
        percentages = [0] * len(times)
    all_totals.append(totals)
    all_percentages.append(percentages)

print ",".join(["\"%s\"" % s  for s in ["Time"] + ["Voter Turnout (%s)"%c for c in categories] + ["Cumulative Turnout Rate (%s)"%c for c in categories]])
for i in range(0, len(times)):
    time = times[i]
    row = [time]
    row += [str(t[i]) for t in all_totals]
    row += [str(t[i]) for t in all_percentages]
    print ",".join(row)

    
