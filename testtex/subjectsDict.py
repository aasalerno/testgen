'''
This functions quick purpose is to get all of the different course lists
'''


def gen_course_list():
    courseList = {'Mathematics':
                      
                  {
                    'MPM1D':{},
                    'MFM1P':{},
                    'MPM1H':{},
                    'MPM2D':{},
                    'MFM2D':{},
                    'MCR3U':
                        {
                            'Unit 1: Functions and Transformations':{},
                            'Unit 4: Exponential Functions':{},
                            'Unit 5: Trigonometry':{},
                            'Unit 6: Trigonometric Functions':{},
                        },
                    'MCF3M':{},
                    'MBF3C':{},
                    'MEL3E':{},
                    'MHF4U':{},
                    'MCV4U':{},
                    'MDM4U':{},
                    'MCT4C':{},
                    'MAP4C':{},
                    'MEL4E':{}
                    },
                'Chemistry':
                    {
                    'SCH3U':{},
                    'SCH3C':{},
                    'SCH4U':
                        {
                                'Unit 1: Structure and Properties':
                                [
                                     'Atomic Theories',
                                     'Quantum Mechanics',
                                     'Chemical Bonding',
                                     'Intermolecular Forces',
                                ],
                                'Unit 2: Organic Chemistry':
                                [
                                    'Functional Groups - Alkane - Nomenclature',
                                    'Functional Groups - Alkane - Drawing',
                                    'Functional Groups - Alkene/Alkyne - Nomenclature',
                                    'Functional Groups - Alkene/Alkyne - Drawing',
                                    'Functional Groups - Halides - Nomenclature',
                                    'Functional Groups - Halides - Drawing',
                                    'Functional Groups - Alcohols - Nomenclature',
                                    'Functional Groups - Alcohols - Drawing',
                                    'Functional Groups - Aldehydes/Ketones - Nomenclature',
                                    'Functional Groups - Aldehydes/Ketones - Drawing',
                                    'Functional Groups - Carboxylic Acids - Nomenclature',
                                    'Functional Groups - Carboxylic Acids - Drawing',
                                    'Functional Groups - Amines - Nomenclature',
                                    'Functional Groups - Amines - Drawing',
                                    'Functional Groups - Carboxylic Acids - Nomenclature',
                                    'Functional Groups - Carboxylic Acids - Drawing',
                                    'Isomers - Draw all the isomers for...',
                                    'Organic Reactions - What will be produced?',
                                    'Organic Reactions - How can we procude...',
                                    'Polymers',
                                ],
                                'Unit 3: Rates of Reactions':
                                [
                                    'Thermochemistry',
                                    'Enthalpies of Reactions',
                                    'Energy Options',
                                    'Chemical Kenetics',
                                ],
                                'Unit 4: Electrochemistry':
                                [
                                    'Oxidation and Reduction Reactions',
                                    'The Activity Series of Metals',
                                    'Galvanic Cells',
                                    'Electrolytic Cells',
                                ],
                                'Unit 5: Chemical Systems and Equilibrium':
                                [
                                    'Introducing Equilibrium',
                                    'The Equilibrium Constant',
                                    'Acid and Bases Equilibrium',
                                    'Solubility Equilibriums',
                                ]
                        }
                                         

                    },
                'Physics':
                    {'SPH3U':{},
                     'SPH3C':{},
                     'SPH4U':{}
                    }
        }
    return courseList
