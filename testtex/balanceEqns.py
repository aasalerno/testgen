import numpy as np
import chempy # not sure if I need this... may make life easier after!
import sys,re
from sympy import symbols
import argparse
from sys import argv
import periodictable as pt
from copy import deepcopy

'''
This program exists to try and balance all types of equations. First it will handle simple stoich, then 
it will also handle redox

Of course... The generator is encountering issues.
1) Not handling diatomic molecules well...
'''
program_name = 'balanceEqns.py'

ostates = np.zeros(200,int)
ostates[0] = -1
ostates[1] = 1
#ostates[3] = 1
#ostates[11] = 1
##ostates[19] = 1
##ostates[37] = 1
#ostates[4] = 2
#ostates[12] = 2
##ostates[20] = 2
##ostates[38] = 2
#ostates[5] = 3
#ostates[13] = 3
#ostates[31] = 3
ostates[7] = -3
ostates[15] = -3
#ostates[33] = -3
ostates[51] = -3
ostates[8] = -2
#ostates[16] = -2
#ostates[34] = -2
ostates[52] = -2
ostates[9] = -1
ostates[17] = -1
ostates[35] = -1
ostates[53] = -1
ostates0 = np.where(ostates==0)[0]


# Table of half equations, always adding electrons
redoxTable=[[{'F2':1},{'F-':2}],
            [{'S2O8-2':1},{'SO4-2':2}],
            [{'Co+3':1},{'Co+2':1}],
            #[{'H2O2':1},{'H2O':2}],
            [{'Au+':1},{'Au':1}],
            [{'Ce+4':1},{'Ce+3':1}],
            [{'MnO4-':1},{'Mn+2':1}],
            [{'Au+3':1},{'Au':1}],
            [{'Cl2':1},{'Cl-':2}],
            [{'Cr2O7-2':1},{'Cr+3':2}],
            #[{'O2':1},{'H2O':2}],
            [{'Br2':1},{'Br-':2}],
            [{'Hg+2':1},{'Hg':1}],
            [{'Fe+3':1},{'Fe+2':1}],
            #[{'O2':1},{'H2O2':1}],
            [{'MnO4-1':1},{'MnO2':1}],
            [{'I2':1},{'I-':2}],
            [{'Cu+':1},{'Cu':1}],
            [{'Cu+2':1},{'Cu':1}],
            [{'Sn+4':1},{'Sn+2':1}],
            #[{'H+':2},{'H2':1}],
            [{'Fe+3':1},{'Fe':1}],
            [{'Pb+2':1},{'Pb':1}],
            [{'Sn+2':1},{'Sn':1}],
            [{'Ni+2':1},{'Ni':1}],
            [{'V+4':1},{'V+2':1}],
            [{'Co+2':1},{'Co':1}],
            [{'Cd+2':1},{'Cd':1}],
            #[{'Se':1},{'H2Se':1}],
            [{'Cr+3':1},{'Cr+2':1}],
            [{'Fe+2':1},{'Fe':1}],
            [{'Cr+3':1},{'Cr':1}],
            [{'Zn+2':1},{'Zn':1}],
            [{'Mn+2':1},{'Mn':1}],
            [{'V+2':1},{'V':1}],
            [{'Al+3':1},{'Al':1}],
            [{'Ti+2':1},{'Ti':1}],
            [{'Mg+2':1},{'Mg':1}],
            [{'Na+':1},{'Na':1}],
            [{'Ca+2':1},{'Ca':1}],
            [{'Ba+2':1},{'Ba':1}],
            [{'K+':1},{'K':1}],
            [{'Li+':1},{'Li':1}]]
                


def lcf(vals):
    vals=abs(vals)
    v1=min(vals)
    v2=max(vals)
    for i in range(v1,v1*v2+1):
        if i%v1==0 and i%v2==0:
            return i

def apply_lcf(vals):
    vals=abs(vals)
    if max(vals)%min(vals) == 0:
        l = max(vals)
    else:
        l = lcf(vals)
    return np.array([l/abs(val) for val in vals])

def redox_balancer(rd,pd,isbasic=False):
    e=rd[1]-pd[1]
    r1=chempy.Substance.from_formula(rd[0])
    p1=chempy.Substance.from_formula(pd[0])
    reactants={}
    products={}
    reactants[rd[0]]=1
    products[pd[0]]=1
    overallCharge = r1.charge-p1.charge-e
    if e > 0: # Add electrons to reactants
        reactants['e-']=abs(e)
    if e < 0: # Add electrons to products
        products['e-']=abs(e)
    if overallCharge < 0:
        reactants['H+']= abs(overallCharge)
    elif overallCharge > 0:
        products['H+']= abs(overallCharge)
    
    if 8 in r1.composition.keys():
        r1Oc = r1.composition[8]
    else:
        r1Oc = 0
    if 8 in p1.composition.keys():
        p1Oc = p1.composition[8]
    else:
        p1Oc = 0
    if r1Oc > p1Oc:
        products['H2O'] = r1Oc - p1Oc
    elif r1Oc < p1Oc:
        reactants['H2O'] = p1Oc - r1Oc

    if isbasic:
        if 'H+' in reactants.keys():
            if 'H2O' in reactants.keys():
                reactants['H2O']+=reactants['H+']
            else:
                reactants['H2O']=reactants['H+']
            products['OH-']=reactants.pop('H+',0)

        elif 'H+' in products.keys():
            if 'H2O' in products.keys():
                products['H2O']+=products['H+']
            else:
                products['H2O']=products['H+']
            reactants['OH-']=products.pop('H+',0)

        if 'H2O' in reactants.keys() and 'H2O' in products.keys():
            numH2O = reactants['H2O'] - products['H2O']
            if numH2O > 0:
                products.pop('H2O')
                reactants['H2O']=abs(numH2O)
            elif numH2O < 0:
                reactants.pop('H2O')
                products['H2O']=abs(numH2O)
    return [reactants, products]
        

def get_oxidation_state(r,p):
    rd = {}
    pd = {}
    rxns = []
    for chem in r:
        chem=chempy.Substance.from_formula(chem)
        # oxidation state!
        if len(chem.composition.keys())==1 and chem.composition[chem.composition.keys()[0]]==2:
            ox = 0
            chemical=chem.composition.keys()[0]
        elif len(chem.composition.keys())==1 and chem.composition[chem.composition.keys()[0]]==1:
            ox = 0
            chemical=chem.composition.keys()[0]
        elif len(chem.composition.keys())==2 and (0 in chem.composition.keys()):
            ox = chem.composition[0]
            chemical = [i for i in chem.composition.keys() if i is not 0][0]
        elif len(chem.composition.keys())==1 and chem.composition[chem.composition.keys()[0]]==1:
            ox = 0
            chemical=chem.composition.keys()[0]
        else:
            ox = -sum([chem.composition[i]*ostates[i] for i in chem.composition.keys()])
            chemical = np.intersect1d(ostates0,np.array(chem.composition.keys()))[0]
        if chemical:
            rd[str(pt.elements[chemical])] = [chem.name,ox]
    for chem in p:
        chem=chempy.Substance.from_formula(chem)
        # oxidation state!
        if len(chem.composition.keys())==1 and chem.composition[chem.composition.keys()[0]]==2:
            ox = 0
            chemical=chem.composition.keys()[0]
        elif len(chem.composition.keys())==2 and (0 in chem.composition.keys()):
            ox = chem.composition[0]
            chemical = [i for i in chem.composition.keys() if i is not 0][0]
        else:
            ox = -sum([chem.composition[i]*ostates[i] for i in chem.composition.keys()])
            chemical = np.intersect1d(ostates0,np.array(chem.composition.keys()))[0]
        if chemical:
            pd[str(pt.elements[chemical])] = [chem.name,ox]
    rk = rd.keys()
    pk = pd.keys()
    elems = [val for val in rk if val in pk]
    for el in elems:
        rxns.append(redox_balancer(rd[el],pd[el]))        
    return rxns


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

# parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--redox', type=int, help='If this is a redox reaction, set this to True. Default=False', default=0)
parser.add_argument('--eqn', type=str, help='The equation we need to work with', default='')
parser.add_argument('--questions',type=int, help='Number of questions if you want them generated.', default=0)
args = parser.parse_args()

args = parser.parse_args()

eqn = args.eqn
redox = args.redox
nqs = args.questions


halfrxnsLatex=genpreamble()+['\\title{Half Reactions}']+genbegin()
rxnsLatex=genpreamble()+['\\title{Full Reactions}']+genbegin()
qsLatex=genpreamble()+['\\title{Questions}']+genbegin()



if nqs:
    eqns=[]
    rtlen = len(redoxTable)
    for nq in range(nqs):
        same=True
        while same:
            locs = np.random.randint(0,rtlen,size=2)
            locs.sort()
            r1 = redoxTable[locs[0]][0].keys()[0] 
            r2 = redoxTable[locs[1]][1].keys()[0]
            p1 = redoxTable[locs[0]][1].keys()[0] 
            p2 = redoxTable[locs[1]][0].keys()[0]
            if not any([r1==p1,r1==r2,r1==p1,r1==p2,r2==p1,r2==p2,p1==p2]):
                same=False
        eqns.append(r1 + ' + ' + r2 + ' -> ' + p1 + ' + ' + p2)
   
    redox=True
   
    for eqn in eqns:
        #eqn=''.join(eqn.split(' '))
        if len(eqn.split('<->')) == 1:
            atype='->'
        else:
            atype='<->'

        r,p = [s.split(' + ') for s in eqn.split(atype)]
        qs=[{},{}]
        for i in r:
            qs[0][i]=1
        for i in p:
            qs[1][i]=1
        qsLatex.append(chemical_equation_latex(qs,atype))

        if redox:
            for i in range(len(r)):
                r[i]=''.join(r[i].split(' '))
            for i in range(len(p)):
                p[i]=''.join(p[i].split(' '))
 
            rxns = get_oxidation_state(r,p)
            halfrxns = deepcopy(rxns)
            K1, K2, Kw = symbols('K1 K2 Kw')
            print(rxns)
            e1=chempy.Equilibrium(rxns[0][0],rxns[0][1],K1)
            e2=chempy.Equilibrium(rxns[1][0],rxns[1][1],K2)
            try:
                coeffs=chempy.Equilibrium.eliminate([e1,e2],'e-')
            except TypeError:
                coeffs=[1,1]
            coeffs=apply_lcf(abs(np.array(coeffs,int)))
            # now we apply the coefficients and pop out the e-
            halfrxnsStr=[]
            rxnsStr=[]
            fullrxns=[{},{}]
            for i in range(len(rxns)):
                # First ensure that we write out the half rxns, then the full
                for j in range(len(rxns[i])):
                    for k in rxns[i][j].keys():
                        halfrxns[i][j][k] = halfrxns[i][j][k]*coeffs[i]
                        rxns[i][j][k] = rxns[i][j][k]*coeffs[i]
                    rxns[i][j].pop('e-',None)
                halfrxnsStr.append(halfrxns[i])
            
            for i in range(len(rxns)):
                for j in range(len(rxns[i])):
                    for k in rxns[i][j].keys():
                        fullrxns[j][k]=rxns[i][j][k] 
            
            for key in fullrxns[0].keys():
                if key in fullrxns[1].keys():
                    fullrxns[0].pop(key,None)
                    fullrxns[1].pop(key,None)                
            rxnsLatex.append(chemical_equation_latex(fullrxns,atype))
                
            for i in range(len(halfrxnsStr)):
                halfrxnsLatex.append(chemical_equation_latex(halfrxnsStr[i],atype))
                #rxnsLatex.append(chemical_equation_latex(rxnsStr[i],atype))
                
            halfrxnsLatex=['\n\n'.join(halfrxnsLatex)]
            rxnsLatex=['\n\n'.join(rxnsLatex)]
        qsLatex.append('\n\n')
        halfrxnsLatex.append('\n\n')
        rxnsLatex.append('\n\n')
    
    
else:
    #eqn=''.join(eqn.split(' '))
    if len(eqn.split('<->')) == 1:
        atype='->'
    else:
        atype='<->'

    r,p = [s.split(' + ') for s in eqn.split(atype)]
    qs=[{},{}]
    for i in r:
        qs[0][i]=1
    for i in p:
        qs[1][i]=1
    qsLatex.append(chemical_equation_latex(qs,atype))

    if redox:
        rxns = get_oxidation_state(r,p)
        halfrxns = deepcopy(rxns)
        K1, K2, Kw = symbols('K1 K2 Kw')
        e1=chempy.Equilibrium(rxns[0][0],rxns[0][1],K1)
        e2=chempy.Equilibrium(rxns[1][0],rxns[1][1],K2)
        coeffs=chempy.Equilibrium.eliminate([e1,e2],'e-')
        coeffs=apply_lcf(np.array(coeffs,int))
        # now we apply the coefficients and pop out the e-
        halfrxnsStr=[]
        rxnsStr=[]
        for i in range(len(rxns)):
            # First ensure that we write out the half rxns, then the full
            for j in range(len(rxns[i])):
                for k in rxns[i][j].keys():
                    halfrxns[i][j][k] = halfrxns[i][j][k]*coeffs[i]
                    rxns[i][j][k] = rxns[i][j][k]*coeffs[i]
            halfrxnsStr.append(halfrxns[i])
            rxns[i][j].pop('e-',None)
            rxnsStr.append(rxns[i])
    
    
        for i in range(len(halfrxnsStr)):
            halfrxnsLatex.append(chemical_equation_latex(halfrxnsStr[i],atype))
            rxnsLatex.append(chemical_equation_latex(rxnsStr[i],atype))
            
        halfrxnsLatex=['\n\\\\\n'.join(halfrxnsLatex)]
        rxnsLatex=['\n\\\\\n'.join(rxnsLatex)]

    else:
        bal = chempy.balance_stoichiometry(r,p)
        rxnsLatex = chemical_equation_latex(bal,atype)

halfrxnsLatex.append('\n\n\n\\end{enumerate}\n\\end{document}')
rxnsLatex.append('\n\n\n\\end{enumerate}\n\\end{document}')
qsLatex.append('\n\n\n\\end{enumerate}\n\\end{document}')
    
f = open('tex/halfrxns.tex','w')
f.write(''.join(halfrxnsLatex))
f.close()

f = open('tex/rxns.tex','w')
f.write(''.join(rxnsLatex))
f.close()

f = open('tex/qs.tex','w')
f.write(''.join(qsLatex))
f.close()

