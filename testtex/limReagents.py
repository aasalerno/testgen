import numpy as np
import chempy # not sure if I need this... may make life easier after!
import sys,re
from sympy import symbols
import argparse
from sys import argv
import periodictable as pt
from copy import deepcopy
import gentex as tex
import chemicalDefinitions as chemdef

'''
This code will provide the framework for limiting reagents problems.
This will include merely balancing equations.
'''


anions= chemdef.gen_anions()
cations= chemdef.gen_cations()
solubility= chemdef.gen_solubility()
reactivity= chemdef.gen_reactivity()






def create_equation(nq,astex=True):


def balance_equation(eqn,astex=True):
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
	qsLatex.append(tex.chemical_equation_latex(qs,atype))

	bal = chempy.balance_stoichiometry(r,p)
	if astex:
		rxnsLatex = tex.chemical_equation_latex(bal,atype)
	else:
		rxnsLatex = tex.chemical_equation_string(bal,atype)
	return rxnsLatex