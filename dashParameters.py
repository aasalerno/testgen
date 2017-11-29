# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)
baseFile='/home/asalerno/testgen/unitFiles'

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
                                'Unit 1: Structure and Properties\n':
                                [
                                     'Lesson 1 Atomic Theories',
                                     'Lesson 2 Quantum Mechanics',
                                     'Lesson 3 Chemical Bonding',
                                     'Lesson 4 Intermolecular Forces',
                                ],
                                'Unit 2: Organic Chemistry\n':
                                [
                                    'Lesson 5 Hydrocarbons',
                                    'Lesson 6 Functional Groups',
                                    'Lesson 7 Types of Organic Reactions',
                                    'Lesson 8 Polymers',
                                ],
                                'Unit 3: Rates of Reactions':
                                [
                                    'Lesson 9 Thermochemistry',
                                    'Lesson 10 Enthalpies of Reactions',
                                    'Lesson 11 Energy Options',
                                    'Lesson 12 Chemical Kenetics',
                                ],
                                'Unit 4: Electrochemistry':
                                [
                                    'Lesson 13 Oxidation and Reduction Reactions',
                                    'Lesson 14 The Activity Series of Metals',
                                    'Lesson 15 Galvanic Cells',
                                    'Lesson 16 Electrolytic Cells',
                                ],
                                'Unit 5: Chemical Systems and Equilibrium':
                                [
                                    'Lesson 17 Introducing Equilibrium',
                                    'Lesson 18 The Equilibrium Constant',
                                    'Lesson 19 Acid and Bases Equilibrium',
                                    'Lesson 20 Solubility Equilibriums',
                                ]
                        }
                                         

                    },
                'Physics':
                    {'SPH3U':{},
                     'SPH3C':{},
                     'SPH4U':{}
                    }
        }
app.layout = html.Div([
    
    html.Div([
        
    html.H1(
        children='Test TeXer',
        style={
            'textAlign': 'center'
        }),
    dcc.Markdown('''#### Subject'''),    
    dcc.Dropdown(
        id='subject-dropdown',
        options=[{'label':i, 'value':i} for i in courseList.keys()],
        value='Chemistry'
        ),
    
    html.Hr(),
    ]),
    
    html.Div([
    dcc.Markdown('''#### Course'''),    
    
    dcc.Dropdown(id='courses-dropdown'),
    html.Hr(),
    ]),
    
    #html.Div([
    #html.Label('Units'),    
    #dcc.Checklist(id='units-checklist'),
    #]),
    
    dcc.Markdown('''#### Units'''),    
    dcc.Checklist(id='units-checklist',
        options=[],
        values=[]
    ),
    html.Hr(),
    
    dcc.Markdown('''#### Topics'''),    
    dcc.Checklist(id='topics-checklist',
        options=[],
        values=[]
    ),
    
    html.Hr(),
    dcc.Markdown('''#### Number of Marks'''),    
    
    dcc.Markdown('''Knowledge (without MC) '''),    
    dcc.Input(id='knowledge',value='0',type='integer'),
    
    dcc.Markdown('''Thinking '''),    
    dcc.Input(id='thinking',value='0',type='integer'),
    
    dcc.Markdown('''Communication '''),    
    dcc.Input(id='communication',value='0',type='integer'),
    
    dcc.Markdown('''Application '''),    
    dcc.Input(id='application',value='0',type='integer'),
        
    dcc.Markdown('''
#### Dash and Markdown

Dash supports [Markdown](http://commonmark.org/help).

Markdown is a simple way to write and format text.
It includes a syntax for things like **bold text** and *italics*,
[links](http://commonmark.org/help), inline `code` snippets, lists,
quotes, and more.
'''),
    
    html.Button('Submit', id='button'),
    
    ])
    
@app.callback(
    dash.dependencies.Output('courses-dropdown', 'options'),
    [dash.dependencies.Input('subject-dropdown','value')]
    )
def set_courses_options(selected_subject):
    ret = [{'label':i, 'value':i} for i in courseList[selected_subject].keys()]
    ret.sort()
    return ret

@app.callback(
    dash.dependencies.Output('courses-dropdown','value'),
    [dash.dependencies.Input('courses-dropdown','options')]
    )
def set_courses_value(available_options):
    return available_options[0]['value']


@app.callback(
    dash.dependencies.Output('units-checklist','options'),
    [dash.dependencies.Input('subject-dropdown','value'),
    dash.dependencies.Input('courses-dropdown','value')]
    )
def set_units_options(selected_subject,selected_course):
    ret = [{'label':i, 'value':i} for i in courseList[selected_subject][selected_course].keys()]
    ret.sort()
    return ret

@app.callback(
    dash.dependencies.Output('topics-checklist','options'),
    [dash.dependencies.Input('subject-dropdown','value'),
    dash.dependencies.Input('courses-dropdown','value'),
    dash.dependencies.Input('units-checklist','values')]
    )
def set_units_options(selected_subject,selected_course,selected_units):
    ret=[]
    for i in range(len(selected_units)):
        for j in range(len(courseList[selected_subject][selected_course][selected_units[i]])):
            k = courseList[selected_subject][selected_course][selected_units[i]][j]
            ret.append({'label':k, 'value':k})
    return ret


if __name__ == '__main__':
    app.run_server(debug=True)
