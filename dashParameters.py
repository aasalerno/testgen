# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)
baseFile='/home/asalerno/testgen/unitFiles'


subjects=['Mathematics','Chemistry','Physics']
courseMath = ['MPM1D','MFM1P','MPM1H','MPM2D','MFM2D','MCR3U','MCF3M','MBF3C','MEL3E','MHF4U','MCV4U','MDM4U','MCT4C','MAP4C','MEL4E']
courseChem = ['SCH3U','SCH3C','SCH4U']
coursePhys = ['SPH3U','SPH3C','SPH4U']

subjList = [{'label':i, 'value':i} for i in subjects]
mathList = [{'label':i, 'value':i} for i in courseMath]
chemList = [{'label':i, 'value':i} for i in courseChem]
physList = [{'label':i, 'value':i} for i in coursePhys]
courseList = {'Mathematics':mathList,'Chemistry':chemList,'Physics':physList}

app.layout = html.Div([
    html.Label('Subject'),
    dcc.Dropdown(
        id='subject-dropdown',
        options=subjList,
        value='Mathematics'
        ),
    
    html.Hr(),
    
    html.Label('Course'),    
    
    dcc.Dropdown(id='courses-dropdown'),
    
    #html.Hr(),
    #html.Hr(),
    
    #html.Div(id='display-selected-values'),
    
    html.Hr(),
    
    html.Label('Units'),
    
    html.Hr(),
    html.Hr(),
    
    #dcc.Checklist(id='units-checklist'),
    
    html.Button('Submit', id='button')
    
    ])
    
@app.callback(
    dash.dependencies.Output('courses-dropdown', 'options'),
    [dash.dependencies.Input('subject-dropdown','value')]
    )
def set_courses_options(selected_subject):
    return courseList[selected_subject]

@app.callback(
    dash.dependencies.Output('courses-dropdown','value'),
    [dash.dependencies.Input('courses-dropdown','options')]
    )
def set_courses_value(available_options):
    return available_options[0]['value']

#@app.callback(
    #dash.dependencies.Output('display-selected-values', 'children'),
    #[dash.dependencies.Input('subject-dropdown','value'),
     #dash.dependencies.Input('courses-dropdown','value')]
    #)
#def set_display_children(selected_subject,selected_course):
    #return u'{} is a subject that has the course {}'.format(selected_subject,selected_course)

#@app.callback(
    #dash.dependencies.Output('units-checklist', 'options'),
    #[dash.dependencies.Input('subject-dropdown','value'),
     #dash.dependencies.Input('courses-dropdown','value')]
    #)
#def units_options(selected_subject,selected_course):
    #locFile=baseFile+selected_subject+'/'+selected_course
    
    #html.Label('Radio Items'),
    #dcc.RadioItems(
        #options=[
            #{'label': 'New York City', 'value': 'NYC'},
            #{'label': u'Montréal', 'value': 'MTL'},
            #{'label': 'San Francisco', 'value': 'SF'}
        #],
        #value='MTL'
    #),

    #html.Label('Checkboxes'),
    #dcc.Checklist(
        #options=[
            #{'label': 'New York City', 'value': 'NYC'},
            #{'label': u'Montréal', 'value': 'MTL'},
            #{'label': 'San Francisco', 'value': 'SF'}
        #],
        #values=['MTL', 'SF']
    #),

    #html.Label('Text Input'),
    #dcc.Input(value='MTL', type='text'),

    #html.Label('Slider'),
    #dcc.Slider(
        #min=0,
        #max=9,
        #marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        #value=5,
    #),
#], style={'columnCount': 2})

#@app.callback(Output('output','children'), [Input('dropdown','value')])

if __name__ == '__main__':
    app.run_server(debug=True)