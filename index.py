from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import keywords_home
# from apps import live_analysis_home
import flask

app.layout = html.Div([
    # Represents the url bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.H1('Sentiment Analysis Using Machine Learning', style={'font-family': 'nasalization',
            'color': '#5bc0de', 'background-color': 'white', 'padding': '10px',
            'border-radius': '20px', 'margin': '0px'}), html.Hr(),

    # Content will be rendered in this element
    html.Div(id='page_content')
])

static_image_route = '/static/'
image_directory = '/Users/vineethkolluru/Downloads/Dash Application/'
index_page = html.Div([
    html.Fieldset([dcc.Link(html.Img(id='image_1',src='/static/keyword_search_image.png',
                   alt="no_image", style={'height': '300px', 'width': '534px',
                   'transition': '0.3s', 'border-radius': '5px'}), href='/keywords_home'), html.Hr(),
                   html.P("Allows you to get the pulse of the basis of keywords specified")], style={'display': 'inline-block', 'border' : 'solid 1px black', 'padding' : '1% 1% 0% 1%', 'margin': '3.5%', 'border-radius': '5px'}, dir='ltr')],
    #html.Br(),
    # html.Fieldset([dcc.Link(html.Img(id='image_2',src='/static/keyword_search_image.png',
    #                alt="no_image", style={'height': '300px', 'width': '534px',
    #                'transition': '0.3s', 'border-radius': '5px'}), href='/live_analysis_home'), html.Hr(),
    #                html.P("Allows you to get the pulse live!")], style={'display': 'inline-block', 'border' : 'solid 1px black', 'padding' : '1%', 'margin': '3.5%', 'border-radius': '5px'})],

    style={'text-align' : 'center', 'font-size' : '1.25em'})

not_found = html.Div([
    html.P('Page not found. Error: 404'),
    dcc.Link('Go to Home Page', href='/')
])


@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')],
)
def display_page(pathname):
    if pathname == '/':
        return index_page
    elif pathname == '/keywords_home':
        return keywords_home.layout
    # elif pathname == '/live_analysis_home':
    #     return live_analysis_home.layout
    else:
        return not_found


@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    return flask.send_from_directory(image_directory, image_name)

if __name__ == '__main__':
    app.run_server(debug=True)
