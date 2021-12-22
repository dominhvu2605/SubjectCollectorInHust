# Visualize the relationship between subjects
import csv
import graphviz
import sys
import re

# Use Digraph() for directed graph
dot = graphviz.Digraph(format='png', graph_attr={'rankdir':'LR'})

# Read file to get data
f = open(r"../crawl_hust/crawl_result.csv", encoding="utf8")
line = csv.DictReader(f)

#Save data read from file to array
data = []
for row in line:
    data.append(row)

#get parameter is subject code
if (len(sys.argv) > 1):
    mahp = sys.argv[1]

# check if the subject has a conditional subject or not
check = 0
for row in data:
    if(row['Mã HP'] != mahp):
        continue
    if(row['Học phần điều kiện']):
        check = 1
        hpdk = row['Học phần điều kiện']
        hpdk = re.sub(r"[^a-zA-Z0-9(),/]", "", hpdk)
        break
# if subject has no conditional subjects
if (check == 0):
    dot.node(mahp)
# if subject has conditional subjects
else:
    while(hpdk != ''):
        dot.edge(mahp, hpdk)
        mahp = hpdk
        check = 0
        for row in data:
            if (row['Mã HP'] == mahp):
                hpdk = row['Học phần điều kiện']
                check = 1
                break
        if(check == 0):
            hpdk = ''

dot.render('output/round-table.gv', view=True)