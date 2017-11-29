import csv

def tex_preamble():
    ret = ['''
\documentclass[pra,11pt]{revtex4-1}
\usepackage{titlesec}
\usepackage{graphicx}
\usepackage{amsmath,mathrsfs}
\usepackage{amssymb}
\usepackage{enumerate}
\usepackage{grffile}
\usepackage[version=4]{mhchem}
\title{%s}
\usepackage[nodisplayskipstretch]{setspace}
\usepackage{fancyhdr}
\pagestyle{fancy}
\rhead{%s - %s}
\newcommand{\aq}{\textrm{(aq)}}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{enumitem}
'''%(title,teacher,course)]



reader = csv.reader(open('paramsfile.csv', 'r'))
data = {}
for row in reader:
    k, v = row
    data[k] = v
    
nversions = int(data['Versions'])
subject = data['Subject']
course = data['Course']
unit = data['Unit']
topics = data['Topics']
ntopics = len(topics)
kmarks = int(data['Knowledge'])
tmarks = int(data['Thinking'])
cmarks = int(data['Communication'])
amarks = int(data['Application'])
teacher = data['Teacher']
title = data['Title']
tot_marks = kmarks + tmarks + cmarks + amarks


