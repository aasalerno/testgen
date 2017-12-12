import chempy
from sympy import symbols
import periodictable as pt

def gen_ostates():	
	ostates = np.zeros(200,int)
	ostates[0] = -1
	ostates[1] = 1
	#ostates[3] = 1
	#ostates[11] = 1
	##ostates[19] = 1
	##ostates[37] = 1
	#ostates[4] = 2
	#ostates[12] = 2
	#ostates[20] = 2
	#ostates[38] = 2
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
	return ostates

def gen_redox_table():
	redox_table=[[{'F2':1},{'F-':2}],
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
	return redox_table

def gen_anions():
	anionList=[['N-3','nitride'],
			   ['O-2','oxide'],
			   ['F-','fluoride'],
			   ['P-3','phosphide'],
			   ['S-2','sulfide'],
			   ['Cl-','chloride'],
			   ['Br-','bromide'],
			   ['I-','iodide'],
			   ['NO2-','nitrite'],
			   ['NO3-','nitrate'],
			   ['CO3-2','carbonate'],
			   ['HCO3-','bicarbonate'],
			   ['ClO3-','chlorate'],
			   ['ClO2-','chlorite'],
			   ['PO4-3','phosphate'],
			   ['SO3-2','sulfite'],
			   ['SO4-2','sulfate'],
			   ['OH-','hydroxide']
	]
	anions=[]
	for i in range(len(anionList)):
		anions.append([chempy.Substance.from_formula(anionList[i][0]),anionList[i][1]])
	return anions

def  gen_cations():
	cationList=[['NH4+','ammonium'],
				['Li+','lithium'],
				['Be+2','berylium'],
				['Na+','sodium'],
				['Mg+2','magnesium'],
				['Al+3','aluminum'],
				['K+','potassium'],
				['Ca+2','calcium'],
				['Fe+3','iron(III)'],
				['Fe+2','iron(II)'],
				['Ni+2','nickel(II)'],
				['Ni+3','nickel(III)'],
				['Cu+2','copper(II)'],
				['Cu+','copper(I)'],
				['Zn+2','zinc'],
				['Ag+','silver'],
				['Sn+4','tin(IV)'],
				['Sn+2','tin(II)']
	]
	cations=[]
	for i in range(len(cationList)):
		cations.append([chempy.Substance.from_formula(cationList[i][0]),cationList[i][1]])
	return cations