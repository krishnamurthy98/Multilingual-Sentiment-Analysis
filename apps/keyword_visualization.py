import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from app import app
import apps.sa_twitter as sa_twitter
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="sih_app")

def get_layout(ip1, language, location):
    keywords = ip1.split(',')
    if keywords[0]:
        keywords = keywords[:5]
        try:
            location = geolocator.geocode(location)
        except:
            return html.Div("Unable to fetch geo data for the location!", style={'color': 'red'})
        if location:
            # Geocode, as required by the twitter API
            geocode = "{0},{1},{2}".format(location.latitude, location.longitude, "10km")
            result = sa_twitter.perform_analysis(keywords, language, geocode)
            if result == None:
                return html.Div(['No tweets exist!\nPlease change the keywords\
                                 or language and try again'],
                                 style={'color': 'red'})
            my_df = pd.DataFrame(result[3], columns=['Number', 'clean_text', 'polarity', 'source'])
            print("my_df: ", my_df)
            top_words = result[4].values
            top_word_count = result[4].index
            labels = ['Positive', 'Negative', 'Neutral']
            values = ['32.00', '45.67', '22.33']
            max_rows = 50
            return html.Div([
                html.Br(),
                html.H2('Sentiment Analysis on "{0}"'.format(ip1)),
                html.P("Number of Tweets: " + str(result[0])),
                html.P("Postive Tweets: " + str(result[1][0])),
                html.P("Negative Tweets: " + str(result[1][1])),
                html.P("Neutral Tweets: " + str(result[1][2])),
                html.Br(),
                dcc.Graph(
                    id='pie_chart',
                    figure={
                        'data': [
                            go.Pie(labels=labels, values=result[2], hole=0.5)
                        ],
                        'layout': go.Layout(
                            margin={'l': 150, 'b': 40, 't': 10, 'r': 600},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    },
                ),
                html.H2("Most used words:"),
                html.Span("{0}\t".format(top_word_count[0]), style={'font-size': '60'}),
                html.Span("{0}\t".format(top_word_count[1]), style={'font-size': '55'}),
                html.Span("{0}\t".format(top_word_count[2]), style={'font-size': '50'}),
                html.Span("{0}\t".format(top_word_count[3]), style={'font-size': '45'}),
                html.Span("{0}\t".format(top_word_count[4]), style={'font-size': '40'}),
                html.Span("{0}\t".format(top_word_count[5]), style={'font-size': '35'}),
                html.Span("{0}\t".format(top_word_count[6]), style={'font-size': '30'}),
                html.Span("{0}\t".format(top_word_count[7]), style={'font-size': '25'}),
                html.Span("{0}\t".format(top_word_count[8]), style={'font-size': '20'}),
                html.Span("{0}\t".format(top_word_count[9]), style={'font-size': '15'}),
                html.Div(
                    [html.Table(
                        # Header
                        [html.Tr([html.Th(col) for col in my_df.columns])] +

                        # Body
                        [html.Tr([
                            html.Td(my_df.iloc[i][col]) for col in my_df.columns
                        ]) for i in range(min(50, len(my_df)))]



                    )],
                    id='opinion_table'
                )
            ])
        else:
            return html.Div("Please check Location!", style={'color': 'red'})
    else:
        return html.Div("Please check Keywords!", style={'color': 'red'})
