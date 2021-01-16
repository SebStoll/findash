# https://github.com/plotly/dash-sample-apps
# https://colorswall.com/palette/5661/

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import timedelta
import pandas as pd
from dash.dependencies import Input, Output


# INITIALIZE APP
# ==============

# Bootswatch themes:
# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN,
# LUX, MATERIA, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE,
# SOLAR, SPACELAB, SUPERHERO, UNITED, YETI

# app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.config.suppress_callback_exceptions = True


# DATA
# ====

# Read test data from within project
# df = pd.read_csv('data/stockdata.csv')

# Read "production data"
# Assumption: Folder findash_data on same level as
# folder app/
df = pd.read_csv('../findash_data/stockdata.csv')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['date', 'ticker'])

df.index = pd.to_datetime(df['date'])


# COMPONENTS
# ==========


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

INITIAL_STOCK_SC = get_options(df['ticker'].unique())[0]['value']

dropdown_timerange = dcc.Dropdown(
    id='timerangeselector',
    options=[
        {'label': 'Full range', 'value': -99},
        {'label': '7d back', 'value': 7},
        {'label': '30d back', 'value': 30},
        {'label': '90d back', 'value': 90},
        {'label': '180d back', 'value': 180},
        {'label': '365d back', 'value': 365},
    ],
    value=-99,
    multi=False,
    className='timerangeselector'
)

dropdown_stocks = dcc.Dropdown(
    id='stockselector',
    options=get_options(df['ticker'].unique()),
    multi=False,
    value=INITIAL_STOCK_SC,
    # style={'backgroundColor': '#1E1E1E'},
    className='stockselector'
)

timerangeselector = dbc.FormGroup(
    [
        dbc.Label("Select time range", html_for="timerangeselector"),
        dropdown_timerange,
    ]
)
stockselector = dbc.FormGroup(
    [
        dbc.Label("Select stock", html_for="stockselector"),
        dropdown_stocks,
    ]
)
form = dbc.Form([timerangeselector, stockselector])


# INTERACTION
# ===========

def create_df_sub(dft, selected_dropdown_stock, selected_dropdown_timerange):
    df_sub = dft.copy()

    # xrange
    x_min_full = df_sub.index.min()
    x_max_full = df_sub.index.max()

    if selected_dropdown_timerange > 0:
        x_min = x_max_full - timedelta(days=selected_dropdown_timerange)
        x_max = x_max_full
    else:
        x_min = x_min_full
        x_max = x_max_full

    df_sub = df_sub[
        (df_sub.index >= x_min)
        & (df_sub.index <= x_max)
        ]

    #######
    # Update close_nld
    for ticker in df_sub['ticker'].unique():

        close_min = df_sub.loc[
            (df_sub.index == df_sub.index.min())
            & (df_sub.ticker == ticker), 'Close'].values[0]

        df_sub.loc[df_sub.ticker == ticker, 'close_nld'] = \
            df_sub.loc[df_sub.ticker == ticker, 'Close'] / close_min*100
    ##########

    return df_sub


@app.callback(
    Output('stockscomparison', 'figure'),
    [
        Input('stockselector', 'value'),
        Input('timerangeselector', 'value'),
    ]
)
def update_stocks_comparison(selected_dropdown_stock, selected_dropdown_timerange):
    df_sub = create_df_sub(
        df, selected_dropdown_stock, selected_dropdown_timerange
    )
    data = [
        go.Ohlc(
            x=df_sub[df_sub['ticker'] == selected_dropdown_stock].index,
            open=df_sub[df_sub['ticker'] == selected_dropdown_stock]['Open'],
            high=df_sub[df_sub['ticker'] == selected_dropdown_stock]['High'],
            low=df_sub[df_sub['ticker'] == selected_dropdown_stock]['Low'],
            close=df_sub[df_sub['ticker'] == selected_dropdown_stock]['Close'],
        )
    ]

    figure = {'data': data,
              'layout': go.Layout(
                  # hovermode='x',
                  # hoverlabel={'font': {'color': '#eae7af'}},
                  # hoverlabel={'bgcolor': '#eae7af'},
                  # autosize=True,
                  title={'text': selected_dropdown_stock},
                  xaxis_rangeslider_visible=False,
                  # xaxis={'range': [x_min, x_max]},
                  # yaxis={'range': [y_min, y_max]},
              ),

              }

    return figure


# APP LAYOUT
# ==========


app.layout = dbc.Container(fluid=True, children=[
    ## Top
    html.H1("Bootstrap Grid System Example")
    , form
    ## Body
    , dbc.Row(dbc.Col(dcc.Graph(id='stockscomparison')))
])


if __name__ == '__main__':
    # app.run_server(debug=True)
    # app.run_server(host='0.0.0.0', port=8050, debug=True)  # If run in docker
    app.run_server(host='127.0.0.1', port=5000, debug=True)  # If local run in windows



