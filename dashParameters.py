# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
import csv
import os

#print(os.getcwd())

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
                                'Unit 1: Structure and Properties':
                                [
                                     'Atomic Theories',
                                     'Quantum Mechanics',
                                     'Chemical Bonding',
                                     'Intermolecular Forces',
                                ],
                                'Unit 2: Organic Chemistry':
                                [
                                    'Hydrocarbons - Nomenclature',
                                    'Hydrocarbons - Drawing',
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
    #dcc.Checklist(id='units-radio'),
    #]),
    
    dcc.Markdown('''#### Units'''),    
    dcc.RadioItems(id='units-radio',
        options=[],
        value=''
    ),
    html.Hr(),
    
    dcc.Markdown('''#### Topics'''),    
    dcc.Checklist(id='topics-checklist',
        options=[],
        values=[]
    ),
    
    html.Hr(),
    dcc.Markdown(children='''#### Number of Marks'''),    
    
    dcc.Markdown('''Knowledge (without MC) '''),    
    dcc.Input(id='knowledge',value=0,type='number',
              style={'textarea':{
                'min-height': '65px','padding-top':' 6px','padding-bottom': '6px' },'width': '5em'}),
    
    dcc.Markdown('''Thinking '''),    
    dcc.Input(id='thinking',value=0,type='number',
              style={'textarea':{
                'min-height': '65px','padding-top':' 6px','padding-bottom': '6px' },'width': '5em'}),
    
    dcc.Markdown('''Communication '''),    
    dcc.Input(id='communication',value=0,type='number',
              style={'textarea':{
                'min-height': '65px','padding-top':' 6px','padding-bottom': '6px' },'width': '5em'}),
    
    dcc.Markdown('''Application '''),    
    dcc.Input(id='application',value=0,type='number',
              style={'textarea':{
                'min-height': '65px','padding-top':' 6px','padding-bottom': '6px' },'width': '5em'}),
    
    html.Hr(),
    
    dcc.Markdown('''#### Number of versions '''),
    dcc.Markdown('''Note that the versions will have different numbers for mathematical questions, or the questions in a jumbled order'''),
    
    dcc.Input(id='versions',value=1,type='number',
              style={'textarea':{
                'min-height': '65px','padding-top':' 6px','padding-bottom': '6px' },'width': '5em'}),
    
    #dcc.Markdown('''Now, we will generate the test!\
		#Please be patient, and only click the button once.\
		#This program is still in beta and may take a while to produce the test!\
		#Thank you.
		#'''),
    html.Hr(),
    html.Button('Generate Test', id='output-button',type='submit'),
    dcc.Markdown(id='information',
             children="Please enter your values, then click the button above to have the program make your test")
    #dcc.Markdown(id='information')
    
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
    dash.dependencies.Output('units-radio','options'),
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
    dash.dependencies.Input('units-radio','value')]
    )
def set_units_options(selected_subject,selected_course,selected_unit):
    ret=[]
    if selected_unit in courseList[selected_subject][selected_course].keys():
		for j in range(len(courseList[selected_subject][selected_course][selected_unit])):
			k = courseList[selected_subject][selected_course][selected_unit][j]
			ret.append({'label':k, 'value':k})
    return ret

#@app.callback(
    #dash.dependencies.Output('information', 'children'),
    #[dash.dependencies.Input('output-button', 'n_clicks')],
	#[dash.dependencies.State('versions','value')])
#def set_display_value(n_clicks,versions):
	#return "The input value was {} and the button has been clicked {} times".format(
        #versions,
        #n_clicks
    #)

@app.callback(
    dash.dependencies.Output('information', 'children'),
    [dash.dependencies.Input('output-button', 'n_clicks'),
	dash.dependencies.Input('subject-dropdown','value'),
    dash.dependencies.Input('courses-dropdown','value'),
    dash.dependencies.Input('units-radio','value'),
    dash.dependencies.Input('topics-checklist','values')],
	[dash.dependencies.State('knowledge','value'),
    dash.dependencies.State('thinking','value'),
    dash.dependencies.State('communication','value'),
    dash.dependencies.State('application','value'),
    dash.dependencies.State('versions','value')])
def write_output_file(n_clicks, subject, course, unit, topics, knowledge, thinking, communication, application, versions):
	if n_clicks == 1:
		csvfile = open('paramsfile.csv','wb')
		paramwriter = csv.writer(csvfile, delimiter=",")
		paramwriter.writerow(['Subject', subject])
		paramwriter.writerow(['Course', course])
		paramwriter.writerow(['Unit', unit])
		topicsHold=[]
		for i in topics:
			if i in courseList[subject][course][unit]:
				topicsHold.append(i)
		paramwriter.writerow(['Topics', topicsHold])
		paramwriter.writerow(['Knowledge', int(knowledge)])
		paramwriter.writerow(['Thinking', int(thinking)])
		paramwriter.writerow(['Communication', int(communication)])
		paramwriter.writerow(['Application', int(application)])
		paramwriter.writerow(['Versions', int(versions)])
		csvfile.close()
		return '''## Test layout 

K: {} 

T: {} 

C: {} 

A: {} 

With {} version(s)'''.format(
			int(knowledge),
			int(thinking),
			int(communication),
			int(application),
			int(versions)
			)

	elif n_clicks > 1:
		reader = csv.reader(open('paramsfile.csv', 'r'))
		d = {}
		for row in reader:
			k, v = row
			d[k] = v
		
		return '''## Please only click the button once. Still generating original test.
## Test layout 

K: {} 

T: {} 

C: {} 

A: {} 

With {} version(s)'''.format(
			d['Knowledge'],
			d['Thinking'],
			d['Communication'],
			d['Application'],
			d['Versions']
			)
	else:
		return "Please enter your values, then click the button above to have the program make your test"




if __name__ == '__main__':
    app.run_server()#debug=True)
    #app.scripts.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})