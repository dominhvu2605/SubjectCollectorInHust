# Visualize the relationship between subjects
import csv
import graphviz

# Use Digraph() for directed graph
dot = graphviz.Digraph()

# Read file to get data
f = open(r"D:\20211\Prj3\Crawl\crawl_hust\result.csv", encoding="utf8")
line = csv.DictReader(f)

# Read line by line
# If the set has conditional sets, draw the relationship between them
# Export the results to a file pdf
for row in line:
    if(row['Học phần điều kiện']):
        course = row['Mã HP']
        conditionalCourse = row['Học phần điều kiện']
        dot.node(course, course)
        dot.node(conditionalCourse, conditionalCourse)
        dot.edge(course, conditionalCourse)

dot.render('output/round-table.gv', view=False)