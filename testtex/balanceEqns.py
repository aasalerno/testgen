import numpy as np
import chempy # not sure if I need this... may make life easier after!
import sys,re
from sympy import symbols
import argparse
from sys import argv
import periodictable as pt
from copy import copy

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


def lcf(vals):
    vals=abs(vals)
    v1=min(vals)
    v2=max(vals)
    for i in range(v1,v1*v2+1):
        if v1%i==0 and v2%i==0:
            return i
def apply_lcf(vals):
    l = lcf(vals)
    return np.array([abs(val)/l for val in vals])

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
   
    if r1.composition[8] > p1.composition[8]:
        products['H2O'] = r1.composition[8] - p1.composition[8]
    elif r1.composition[8] < p1.composition[8]:
        reactants['H2O'] = p1.composition[8] - r1.composition[8]

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
    rxns = []
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
        rxns.append(redox_balancer(rd[el],pd[el]))        
    return rxns
    
    
    

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
    rxns = get_oxidation_state(r,p)
    halfrxns = copy(rxns)
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
                halfrxns[i][j].k *= coeffs[i]
                rxns[i][j].k *= coeffs[i]
        
        rxnsStr.append(rxns[i])

else:
    bal = chempy.balance_stoichiometry(r,p)



print(chemical_equation_string(bal,atype))
print(chemical_equation_latex(bal,atype))

