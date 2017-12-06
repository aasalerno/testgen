import numpy as np
import chempy # not sure if I need this... may make life easier after!
import sys,re
from sympy import symbols
import argparse
from sys import argv
import periodictable as pt

'''
This program exists to try and balance all types of equations. First it will handle simple stoich, then 
it will also handle redox
'''
program_name = 'balanceEqns.py'

ostates = np.zeros(54,int)
ostates[0] = -1
ostates[1] = 1
ostates[3] = 1
ostates[11] = 1
ostates[19] = 1
ostates[37] = 1
ostates[4] = 2
ostates[12] = 2
ostates[20] = 2
ostates[38] = 2
ostates[5] = 3
ostates[13] = 3
ostates[31] = 3
ostates[7] = -3
ostates[15] = -3
ostates[33] = -3
ostates[51] = -3
ostates[8] = -2
ostates[16] = -2
ostates[34] = -2
ostates[52] = -2
ostates[9] = -1
ostates[17] = -1
ostates[35] = -1
ostates[53] = -1
ostates0 = np.where(ostates==0)[0]


def chemical_equation_string(vals,atype):
    r = vals[0]
    p = vals[1]
    s = []
    for i in r.keys():
        s.append(str(r[i]))
        s.append(i)
        s.append('+')
    s[-1]=atype
    for i in p.keys():
        s.append(str(p[i]))
        s.append(i)    
    s=s[:-1]
    return ' '.join(s)


def redox_balancer(rd,pd,e,ifbasic=False):
    r1=chempy.Substance.from_formula(rd[0])
    p1=chempy.Substance.from_formula(pd[0])
    overallCharge = r1.charge-p1.charge-e
    if e > 0: # Add electrons to reactants
        reactants=[rd[0],str(abs(e))+'e-']
        products=[pd[0]]
            
    if e < 0: # Add electrons to products
        reactants=[rd[0]]
        products=[pd[0],str(abs(e))+'e-']

    if overallCharge < 0:
        reactants.append(str(abs(overallCharge))+'H+')
    elif overallCharge > 0:
        products.append(str(abs(overallCharge))+'H+')
   
    if r1.composition[8] > p1.composition[8]:
        products.append(str(r1.composition[8] - p1.composition[8])+'H2O')
    elif r1.composition[8] < p1.composition[8]:
        reactants.append(str(-r1.composition[8] + p1.composition[8])+'H2O')
    
    return reactants, products
        


def chemical_equation_latex(vals,atype):
    r = vals[0]
    p = vals[1]
    s = ['\\ce{']
    for i in r.keys():
        s.append('\\ce{' + str(r[i]))
        s.append(chempy.Substance.from_formula(i).latex_name + '}')
        s.append('+')
    s = s[:-1]
    if atype=='<->':
        s.append('<=>')
    else:
        s.append('->')
    for i in p.keys():
        s.append('\\ce{' + str(p[i]))
        s.append(chempy.Substance.from_formula(i).latex_name + '}')
        s.append('+')
    s = s[:-1]
    s.append('}')
    return ' '.join(s)

def get_oxidation_state(r,p):
    rd = {}
    pd = {}
    echange = {}
    rxns = []
    water=['H2O','O2','H+']
    for chem in r:
        chem=chempy.Substance.from_formula(chem)
        # oxidation state!
        ox = -sum([chem.composition[i]*ostates[i] for i in chem.composition.keys()])
        chemical = np.intersect1d(ostates0,np.array(chem.composition.keys()))[0]
        if chemical:
            rd[str(pt.elements[chemical])] = [chem.name,ox]
    for chem in p:
        chem=chempy.Substance.from_formula(chem)
        # oxidation state!
        ox = -sum([chem.composition[i]*ostates[i] for i in chem.composition.keys()])
        chemical = np.intersect1d(ostates0,np.array(chem.composition.keys()))[0]
        if chemical:
            pd[str(pt.elements[chemical])] = [chem.name,ox]
    rk = rd.keys()
    pk = pd.keys()
    elems = [val for val in rk if val in pk]
    for el in elems:
        echange[el]=rd[el]-pd[el]
        if echange[el] > 0:
            rr['e-'] = echange[el]
        if echange[el] < 0:
            pr['e-'] = abs(echange[el])
                
    
    return rr, pr, echange
    
    
    

# parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--redox', type=int, help='If this is a redox reaction, set this to True. Default=False', default=0)
parser.add_argument('--eqn', type=str, help='The equation we need to work with', default='')
args = parser.parse_args()

args = parser.parse_args()

eqn = args.eqn
redox = args.redox


eqn=''.join(eqn.split(' '))
if len(eqn.split('<->')) == 1:
    atype='->'
else:
    atype='<->'

r,p = [s.split('+') for s in eqn.split(atype)]

if redox:
    rr, pr, echange = get_oxidation_state(r,p)
    K1, K2, Kw = symbols('K1 K2 Kw')
    r.append(
else:
    bal = chempy.balance_stoichiometry(r,p)



print(chemical_equation_string(bal,atype))
print(chemical_equation_latex(bal,atype))

