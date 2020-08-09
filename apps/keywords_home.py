from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app
import apps.keyword_visualization as key_viz

layout = html.Div([
    dcc.Link([html.Div('Home')], href='/'),

    html.Label("Keywords:", style={'font-size': '120%'}),
    dcc.Input(
        id='my_keywords',
        placeholder="#HappyHoli, trump, ...",
        type='text',
        value='',
        minlength=1,
        maxlength=100
    ),

    html.Br(),html.Br(),
    html.Label("Language:", style={'font-size': '120%'}),
    dcc.Dropdown(
        id='my_language',
        options=[
            {'label': 'English', 'value': 'en'},
            {'label': 'Hindi', 'value': 'hi'},
            {'label': 'Telugu', 'value': 'te'},
        ],
        multi=False,
        value='en',
        disabled=False,
        searchable=False,
        clearable=False
    ),

    html.Br(),
    html.Label("Location:", style={'font-size': '120%'}),
    dcc.Input(
        id='my_location',
        placeholder="Hyderabad",
        type='text',
        value='',
        minlength=1,
        maxlength=100
    ),

    html.Br(), html.Br(),
    html.Button('Submit', id='my_button',
        style={"background-color": '#42A5F5', 'color': 'white'}),

    html.Br(),
    html.Div(id='my_visualization')

])

@app.callback(Output('my_visualization', 'children'),
              [Input('my_button', 'n_clicks')],
              [State('my_keywords', 'value'),
               State('my_language', 'value'),
               State('my_location', 'value')]
)
def update_visualization(n_clicks, ip1, language, location):
    if not n_clicks:
        return None
    else:
        return key_viz.get_layout(ip1, language, location)


if __name__ == '__main__':
    app.run_server(debug=True)
