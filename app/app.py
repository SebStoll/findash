# https://github.com/plotly/dash-sample-apps
# https://colorswall.com/palette/5661/

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from datetime import timedelta
import pandas as pd
from dash.dependencies import Input, Output


# INITIALIZE APP
# ==============

app = dash.Dash(__name__)
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


value_list = list(df.columns)
value_list = [e for e in value_list if e not in ('date', 'ticker')]
INITIAL_STOCKS_SC = [get_options(df['ticker'].unique())[0]['value']]
INITIAL_VALUE_SC = get_options(value_list)[0]['value']

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
    multi=True,
    value=INITIAL_STOCKS_SC,
    # style={'backgroundColor': '#1E1E1E'},
    className='stockselector'
)

dropdown_values = dcc.Dropdown(
    id='valueselector',
    options=get_options(value_list),
    multi=False,
    value=INITIAL_VALUE_SC,
    # style={'backgroundColor': '#1E1E1E'},
    className='valueselector'
)

graph_stocks_over_time = dcc.Graph(
    id='stockscomparison',
    config={'displayModeBar': False},
    animate=True
)


# INTERACTION
# ===========

def create_df_sub(dft, selected_dropdown_stocks, selected_dropdown_value, selected_dropdown_timerange):
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

    # check if list
    if not isinstance(selected_dropdown_stocks, list):
        selected_dropdown_stocks = [selected_dropdown_stocks]

    # yrange
    st = df_sub[
        df_sub['ticker'].isin(selected_dropdown_stocks)
    ][selected_dropdown_value]

    y_min = st.min()
    y_max = st.max()
    y_range = y_max - y_min

    y_min = y_min - 0.10*y_range
    y_max = y_max + 0.10*y_range
    return df_sub, x_min, x_max, y_min, y_max


@app.callback(
    Output('stockscomparison', 'figure'),
    [
        Input('stockselector', 'value'),
        Input('valueselector', 'value'),
        Input('timerangeselector', 'value'),
    ]
)
def update_stocks_comparison(selected_dropdown_stocks, selected_dropdown_value, selected_dropdown_timerange):
    df_sub, x_min, x_max, y_min, y_max = create_df_sub(df, selected_dropdown_stocks,
                                                       selected_dropdown_value, selected_dropdown_timerange)

    trace1 = []
    for stock in selected_dropdown_stocks:
        trace1.append(go.Scatter(x=df_sub[df_sub['ticker'] == stock].index,
                                 y=df_sub[df_sub['ticker'] == stock][selected_dropdown_value],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))

    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=['#2069e0', '#FF4F00', '#29c7ac', '#ffcc00', '#26beff', '#cd4528'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  # hoverlabel={'font': {'color': '#eae7af'}},
                  # hoverlabel={'bgcolor': '#eae7af'},
                  autosize=True,
                  title={'text': 'Stocks comparison', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [x_min, x_max]},
                  yaxis={'range': [y_min, y_max]},
              ),

              }

    return figure


# APP LAYOUT
# ==========

app.layout = html.Div(
    children=[
        html.Div(
            className='row',
            children=[
                # Left Panel Div
                html.Div(
                    className='four columns div-user-controls',
                    children=[
                        html.H2('DASH - STOCK PRICES'),
                        html.H3('Select time range.'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dropdown_timerange,
                            ],
                            style={'color': '#1E1E1E'}
                        ),
                        # Stocks comparison
                        html.H3('Stocks comparison.'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dropdown_stocks,
                            ],
                            style={'color': '#1E1E1E'}
                        ),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dropdown_values,
                            ],
                            style={'color': '#1E1E1E'}
                        ),
                    ]
                ),
                # Right Panel Div
                html.Div(
                    className='eight columns div-for-charts',
                    children=[
                        graph_stocks_over_time,
                    ]
                )
            ]
        ),
    ]
)


if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', port=8050, debug=True)  # If run in docker
    # app.run_server(host='127.0.0.1', port=5000, debug=True)  # If local run in windows
