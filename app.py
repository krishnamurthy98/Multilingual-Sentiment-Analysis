import dash

app = dash.Dash('Sentiment Analysis')
server = app.server
app.config.suppress_callback_exceptions = True
app.css.append_css({
     'external_url': "https://codepen.io/chriddyp/pen/bWLwgP.css"
 })
