import periodictable
import re
import csv
from numpy.random import randint
import numpy as np
import random

# Currently can't handle amines, amides, ethers or esters. 
# Also need to add in functionality for putting hydroxy/amine on the same carbon as another group.

'''
Current status:
    - aldehyde and carboxylic acid are failing in production -- FG going on last carbon, not first
    - halides not writing out properly.
    - naming system seems to be fine?
'''
fgpre=['','di','tri','tetra','penta','hexa','hepta','octa','nona','deca','undeca','dodeca','trideca']
chempre=['meth','eth','prop','but','pent','hex','hept','oct','non','dec','undec','dodec','tridec']
ncarb = range(1,len(chempre)+1)

reader=csv.DictReader(open('fg.csv','rb'))
fg=[]
fgNames=[]

for line in reader:
    fg.append(line)
    fgNames.append(fg[-1]['functional group'])


for i in range(len(fg)):
    if fg[i]['terminal']=='True':
        fg[i]['terminal'] = True
    else:
        fg[i]['terminal'] = False


def create_questions(nq,minsize=5,maxsize=10,maxsg=4):
    names=[]
    allowed=fgNames
    q=7
    allowedmajor=allowed[:q]
    allowedminor=allowed[q:]
    allowedminor=[fg[n]['name'] for n in range(q,q+len(allowedminor))]
    sizes = randint(minsize,maxsize+1,size=nq)
    sgszs = randint(1,maxsg,size=nq)
    for i,sz in enumerate(sizes):
        majgroup = randint(7)
        if not fg[majgroup]['terminal']:
            majloc=randint(1,sz+1)
            majloc=str(min(sz-majloc,majloc))
            if fg[majgroup]['functional group']=='ketone' and majloc=='1':
                majgroup-=1
            if majloc in ['1','0']:
                majloc=''
        else:
            majloc=''
        majname = chempre[sz-1]
        sgsz=sgszs[i]
        sg=[]
        locs=np.zeros(3)
        lunique,lcounts = np.unique(locs,return_counts=True)
        while any(lcounts>2) or (fg[majgroup]['functional group']=='ketone' and (majloc in lunique)):
            locs=randint(0,sz,size=sgsz)
            lunique,lcounts = np.unique(locs,return_counts=True)
        for l,loc in enumerate(locs):
            if (sgsz-loc)>0:
                locs[l]=sgsz
            locs[l]=min(locs[l],sz-locs[l])
            #import pdb; pdb.set_trace()
            if locs[l]>0:
                sg.append(chempre[randint(1,locs[l]+1)])
            else:
                sg.append(1)
        # Now check if we have any halides...
        halides=(randint(0,len(allowedminor),size=sgsz)==0)*randint(1,len(allowedminor),size=sgsz)
        sg = np.array(sg,dtype='|S10')
        sg[np.where(halides)[0]] = np.array(allowedminor)[halides[np.where(halides)[0]]]
        srt=np.argsort(sg)
        locs=locs[srt]
        sg=sg[srt]
        sgunique,sgcnts = np.unique(sg,return_counts=True)
        sgnames=[]
        sglocs=[]
        all_indicies=[]
        for j in range(len(sgunique)):
            sgnames.append(fgpre[sgcnts[j]-1]+sgunique[j])
            all_indicies.append(list(np.sort(np.array([locs[index] for index, value in enumerate(list(sg)) if value == list(sgunique)[j]]))))
        name=[]
        for j in range(len(all_indicies)):
            if j!=0:
                name.append('-')
            ai_str=[str(a+1) for a in all_indicies[j]]
            name.append(','.join(ai_str))
            name.append('-')
            if sgnames[j].split('i')[-1] in chempre:
                name.append(sgnames[j]+'yl')
            else:
                name.append(sgnames[j])
        if fg[majgroup]['functional group'] in ['carboxylic acid','ketone','aldehyde','alcohol']:
            majadd='an'
        else:
            majadd=''
        if majloc:
            name.append(majname+majadd+'-'+majloc+'-'+fg[majgroup]['suffix'])
        else:
            name.append(majname+majadd+fg[majgroup]['suffix'])
        names.append(''.join(name))
    return names
                
                
            
            
        
        
        
        
#chemicals = ['2,5-dimethylheptene','3,4,5-triethyl-3-methylheptan-2-ol']
#chemicals = ['N,N-dimethylhexamine']
chemicals=create_questions(10)

chemStructs={}
number=True


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
         '\\definesubmol\\nobond{[,0.2,,,draw=none]}',
         '\\begin{document}']
    return ''.join([a+'\n' for a in s])


def buildbackbone(carb,name='',number=True):
    for i in range(carb):
        if number:
            numstr='(!\\nobond\\chemabove[1ex]{}{%i})'%(i+1)
        else:
            numstr=''
        if i==0:
            bb = ['\\[\\chemname{\\chemfig{[:30]'+numstr]
        elif i%2:
            bb.append('-[:-30]'+numstr)
        else:
            bb.append('-'+numstr)
    bb.append('}}{%s}\\]'%name)
    return bb
        
def sidechain(chemStruct):
    # Need to pull in all locs
    locs = chemStruct['locs'][1:][0]
    locsLen = [len(l) for l in locs]
    locsLen = [sum(locsLen[0:index],locsLen[index])-1 for index,value in enumerate(locsLen)]
    locsTot = [item for sublist in locs for item in sublist]
    locsUnique=list(set(locsTot))
    locsCount=[]
    
    # And pull in the sizes...
    Cchain = chemStruct['Cchain'][1:]
    bb=chemStruct['backbone']
    for l in locsUnique:
        ang=[]
        sloc=[]
        
        # figure out where all of the indicies are, what the size of the chains need to be, given their direction
        chainlist=[]
        chainloc = [index for index, value in enumerate(locsTot) if value == l]
        for cl in chainloc:
            diff = [x-cl for x in locsLen]
            chainlist.append(Cchain[min(enumerate(diff), key=lambda x: x[1] if x[1] >= 0 else float('inf'))[0]])
        if locsTot.count(l)==2:
            if l%2:
                sloc.append(1)
                ang.append(-30)
                sloc.append(3)
                ang.append(210)
            else:
                sloc.append(5)
                ang.append(150)
                sloc.append(7)
                ang.append(30)
        elif locsTot.count(l)==1:
            if l%2:
                sloc.append(2)
                ang.append(30)
            else:
                sloc.append(6)
                ang.append(-30)
        for cloc,chain in enumerate(chainlist):
            hldbb=['(']
            # l is the location, chain is the length, cloc is which chain we are working with
            for pt in range(chain):
                if pt==0:
                    hldbb.append('[%i]-'%sloc[cloc])
                elif pt%2:
                    hldbb.append('-[:%i]'%ang[cloc])
                else:
                    hldbb.append('-[:%i]'%(-ang[cloc]))
            hldbb.append(')')
            hldbb = "".join(hldbb)
            bb[l-1]=bb[l-1]+hldbb
    
    return bb

def addmaingroup(chemStruct):
    end=fg[chemStruct['func gs loc'][0]]['tex']
    loc=chemStruct['locs'][0][0] # Need to make this better...
    if loc%2:
        locChain=2
    else:
        locChain=6
    if chemStruct['func gs'][0] == 'alkyne' or chemStruct['func gs'][0] == 'alkene':
        chemStruct['backbone'][loc-1] = end+chemStruct['backbone'][loc-1][1:]
    else:
        chemStruct['backbone'][loc-1] = chemStruct['backbone'][loc-1]+end%locChain
    return chemStruct['backbone']

#######################################################################################
totalfile=[]
totalfile.append(genpreamble())
vspace='\n\n\\vspace{0.75in}\n\n'

for c,chem in enumerate(chemicals):
    chemStructs[chem]={}
    chemStructs[chem]['name']=chem
    chemStructs[chem]['func gs']=[]
    chemStructs[chem]['func gs loc']=[]
    chemStructs[chem]['suffix']=[]
    chemStructs[chem]['locs']=[]
    chemStructs[chem]['backbone']=[]
    chemStructs[chem]['Cchain']=[]
    chemStructs[chem]['latex']=[]
    
    # Lets grab the most important group and its location.
    for g in range(len(fg)):
        testgroup = fg[g]['suffix']
        if len(testgroup)<=len(chem):
            if chem[-len(testgroup):]==testgroup:
                chemStructs[chem]['func gs'].append(fg[g]['functional group'])
                chemStructs[chem]['func gs loc'].append(g)
                chemStructs[chem]['suffix'].append(fg[g]['suffix'])
                if fg[g]['terminal']:
                    chemStructs[chem]['locs'].append([0])
                else:
                    if chem[-len(testgroup)-2].isdigit():
                        chemStructs[chem]['locs'].append([int(chem.split('-')[-2])])
                    else:
                        chemStructs[chem]['locs'].append([1])
                break
     
    # Now we need to look for the side groups (and their locations) -- this one only works for simple stuff
    # Need to make another version for N-groups
    for g in range(len(fg)):
        testgroup = fg[g]['name']
        if len(testgroup)<=len(chem):
            loc = chem.find(testgroup)
            if loc>0:
                if not chem[loc:]==fg[g]['suffix']:
                    chemStructs[chem]['func gs'].append(fg[g]['functional group'])
                    chemStructs[chem]['suffix'].append(fg[g]['name']) # Name here as it isn't a pure suffix. It's a side group
                    gloc=[]
                    csplit = chem.split(testgroup)
                    nlocs = len(csplit)-1
                    for i in range(nlocs):
                        if i > 0:
                            gloc.append(gloc[-1]+len(csplit[i])+i*len(testgroup))
                        else:
                            gloc.append(len(csplit[i]))
                    chemStructs[chem]['locs'].append(gloc)
                    
    # Now we need to figure out exactly which branches we have and where they are...
    # The first one, we know, where it is based on the first loop. We need to fix the other ones.
    #for g,group in enumerate(chemStructs[chem]['func gs']):
    scloc=[]
    sc=[]
    for pre in chempre:
        loc=chem.find(pre)
        if loc>=0:
            scloc.append(loc)
            sc.append(pre)
    maxpre=sc[scloc.index(max(scloc))]
    chemStructs[chem]['Cchain'].append(ncarb[chempre.index(maxpre)])
    sc.remove(maxpre)
    

    for sl,s in enumerate(chemStructs[chem]['suffix'][1:]):
        chemStructs[chem]['locs'][sl+1]=[]
        for prefix in sc:
            if prefix=='eth':
                chold=chem
                chem=chem.split('meth')[0]
            loc=chem.find(prefix+s)
            if loc >= 0:
                spl = chem.split(prefix+s)
                for pl,p in enumerate(fgpre):
                    if spl[0][-len(p):]==p:
                        nChain=pl+1
                        break
                    else:
                        nChain=1
                if prefix=='eth':
                    chem=chold
                findcarbons = [int(val) for val in re.findall('\\b\\d+\\b',chem.split(prefix+s)[0])][-nChain:]
                chemStructs[chem]['locs'][sl+1].append(findcarbons)
                chemStructs[chem]['Cchain'].append(chempre.index(prefix)+1)
            elif prefix=='eth':
                chem=chold
            
     
    chemStructs[chem]['backbone']=buildbackbone(chemStructs[chem]['Cchain'][0],chem,number=False)
    chemStructs[chem]['backbone']=sidechain(chemStructs[chem])
    chemStructs[chem]['backbone']=addmaingroup(chemStructs[chem])
    
    totalfile.append(''.join(chemStructs[chem]['backbone']))
    totalfile.append(vspace)
    
    
    
totalfile.append('\n\n\n\\end{document}')
    
    
f = open('test.tex','w')
f.write(''.join(totalfile))
f.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    