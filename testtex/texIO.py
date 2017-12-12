import chempy
'''
This code is built to hold all of the TeX input/output code.
'''

def chemical_equation_string(vals,atype):
    r = vals[0]
    p = vals[1]
    s = []
    for i in r.keys():
        if r[i]>1:
            s.append(str(r[i]))
        s.append(i)
        s.append('+')
    s[-1]=atype
    for i in p.keys():
        if p[i] > 1:
            s.append(str(p[i]))
        s.append(i)    
        s.append('+')
    s=s[:-1]
    return ' '.join(s)



def chemical_equation_latex(vals,atype):
    r = vals[0]
    p = vals[1]
    s = ['\\item \\ce{']
    for i in r.keys():
        s.append('\\ce{')
        if r[i]>1:
            s.append(str(r[i]))
        i=''.join(i.split(' '))
        s.append(chempy.Substance.from_formula(i).latex_name + '_{(aq)}}')
        s.append('+')
    s = s[:-1]
    if atype=='<->':
        s.append('<=>')
    else:
        s.append('->')
    for i in p.keys():
        s.append('\\ce{')
        if p[i]>1:
            s.append(str(p[i]))
        i=''.join(i.split(' '))
        s.append(chempy.Substance.from_formula(i).latex_name + '_{(aq)}}')
        s.append('+')
    s = s[:-1]
    s.append('}')
    return ' '.join(s)

def genpreamble():
    s = ['\\documentclass[pra,11pt,aps]{revtex4-1}',
         '\\usepackage[utf8]{inputenc}',
         '\\usepackage{chemfig}',
         '\\usepackage{titlesec}',
         '\\usepackage{graphicx}',
         '\\usepackage{amsmath,mathrsfs}',
         '\\usepackage{amssymb}',
         '\\usepackage{enumerate}',
         '\\usepackage{grffile}',
         '\\usepackage[version=4]{mhchem}',
         '\\definesubmol\\nobond{[,0.2,,,draw=none]}'
         ]
    return [''.join([a+'\n' for a in s])]
    
# --------------------------------------------------------------------- #    
def genbegin():
    s = ['\n\\begin{document}',
     '\\begin{enumerate}']
    return [''.join([a+'\n' for a in s])] 
