import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_bootstrap_components as dbc
import numpy as np
from os import getcwd
from pathlib import Path
from dash.dependencies import Input, Output, State
from python.dataviz import reformat_figure, df, boxplot, mapbox, histogram, piechart, heatmap
from python.utils import predict_price


def get_input(_id, _type):
    if _id in ["age", "ocean-proximity", "income"]:
        if _id == "age":
            options = [
                {'label': 'Recent', 'value': 7},
                {'label': 'Average', 'value': 20},
                {'label': 'Old', 'value': 33},
                {'label': 'Most old', 'value': 46}
            ]
        elif _id == "ocean-proximity":
            options = [
                {'label': 'Near bay', 'value': 1},
                {'label': 'Near ocean', 'value': 2},
                {'label': 'Island', 'value': 3},
                {'label': '1h ocean', 'value': 4},
                {'label': 'Inland', 'value': 5}
            ]
        elif _id == "income":
            options = [
                {'label': 'Low', 'value': 1.53165},
                {'label': 'Medium', 'value': 3.0491},
                {'label': 'High', 'value': 4.139025},
                {'label': 'Very high', 'value': 9.871675}
            ]
        return dcc.Dropdown(
            id=f"input-{_id}",
            options=options
        )
    else:
        return dcc.Input(
            id=f"input-{_id}",
            type=_type,
            placeholder="",
        )


asset_folder = str(Path(getcwd()).parent.absolute()) + "\\assets"

inputs_features = ["age", "ttl-rooms", "ttl-bedrooms", "ocean-proximity", "population", "income"]
inputs = [get_input(id=inputs_features[i], type="number") for i in range(len(inputs_features))]
inputs_html = {key: value for key, value in zip(inputs_features, inputs)}
submit_button = dbc.Button("Estimate the house value", className="btn btn-lg btn-primary", id="submit-button")
output = html.Div("", id="output")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], assets_folder=asset_folder)
app.config.suppress_callback_exceptions = True
app.title = "BI Dashboard for real estate agency"

layout_dataviz = html.Div(
    [
        html.Div([
            html.Div([html.H2("Data Visualisation")], id="subtitle"),
            html.Div([
                html.Div([

                    html.Div([
                        html.H3("House value", id="label-placeholder-value"),
                        dcc.RangeSlider(
                            id='input-value',
                            className='slider',
                            min=df['median_house_value'].min(),
                            max=df['median_house_value'].max(),
                            value=[df['median_house_value'].min(), df['median_house_value'].max()]
                        ),
                        html.H4("", id="label-slider"),
                    ], className="container-slider"),
                    html.Div([
                        html.H3("Total rooms in the house", id="label-placeholder-rooms"),
                        dcc.RangeSlider(
                            id='input-rooms',
                            className='slider',
                            min=df['total_rooms'].min(),
                            max=df["total_rooms"].sort_values()[:-2].max(),
                            value=[df['total_rooms'].min(), df['total_rooms'].max()],
                            marks={str(x): str(x) for x in np.linspace(0, 62, 10).astype(int)}
                        ),
                    ], className="container-slider"),
                    html.Div([
                        html.H3("Age of the house", id="label-placeholder-age"),
                        dcc.RangeSlider(
                            id='input-agehouse',
                            className='slider',
                            min=df['housing_median_age'].min(),
                            max=df['housing_median_age'].max(),
                            value=[df['housing_median_age'].min(), df['housing_median_age'].max()],
                            marks={str(x): str(x) for x in np.linspace(0, 52, 10).astype(int)}
                        ),
                    ], className="container-slider"),

                ], className="card-header"),

                html.Div(
                    [
                        dcc.Graph(id='dynamic-graphic-01', className="dynamic-graphic"),
                        dcc.Graph(id='dynamic-graphic-02', className="dynamic-graphic"),
                        dcc.Graph(id='dynamic-graphic-03', className="dynamic-graphic-large"),
                        dcc.Graph(id='dynamic-graphic-04', className="dynamic-graphic"),
                        dcc.Graph(id='dynamic-graphic-05', className="dynamic-graphic"),
                    ], className="card-body")
            ], id="input-graph", className="card border-primary mb-3")
        ]),
    ], id="main")

layout_tool = html.Div(
    [
        html.Div([
            html.Div([html.H2("Estimation / Predictive Tool")], id="subtitle"),
            html.Div([
                html.Div("Fill in the information to estimate the price of the house.", className="card-header"),
                html.Div([
                    html.Div([
                        html.H3("Housing age", className="card-title"),
                        html.H3("Total rooms", className="card-title"),
                        html.H3("Total bedrooms", className="card-title"),
                        html.H3("Ocean proximity", className="card-title"),
                        html.H3("Population ", className="card-title"),
                        html.H3("Median income of households", className="card-title"),
                    ], id="input-features"),

                    html.Div(list(inputs_html.values()), id="input")

                ], className="card-body"),
                submit_button,
                output

            ], className="card border-dark mb-3", id="menu"),
        ]),
    ], id="main")

index_layout = html.Div([
    html.A(dbc.Button("Dashboard", className="btn btn-lg btn-primary", id="menu-button-1"), href="dashboard"),
    html.A(dbc.Button("Estimation tool", className="btn btn-lg btn-primary", id="menu-button-2"),
           href="estimation-tool"),
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav([
        html.Div([
            html.Div([html.H1("House Princing - California")], id="title", className="collapse navbar-collapse"),
        ], className="container-fluid")
    ], id="nav", className="navbar navbar-expand-lg navbar-dark bg-dark"),

    html.Div([], id="page-content")
])


# region callbacks
@app.callback(
    Output("label-slider", "children"),
    Input('input-value', 'value')

)
def update_label_slider(value):
    return "${:,} - ${:,}".format(value[0], value[1]).replace(",", " ")


@app.callback(
    [Output('dynamic-graphic-01', 'figure'),
     Output('dynamic-graphic-02', 'figure'),
     Output('dynamic-graphic-03', 'figure'),
     Output('dynamic-graphic-04', 'figure'),
     Output('dynamic-graphic-05', 'figure')],
    Input('input-value', 'value'),
    Input('input-rooms', 'value'),
    Input('input-agehouse', 'value'), )
def update_graph(target_value, target_rooms, target_age):
    mask = ((df["median_house_value"] > target_value[0]) & (df["median_house_value"] < target_value[1]) &
            (df["total_rooms"] > target_rooms[0]) & (df["total_rooms"] < target_rooms[1]) &
            (df["housing_median_age"] > target_age[0]) & (df["housing_median_age"] < target_age[1]))
    _df = df[mask]
    fig_01 = mapbox(_df)
    fig_02 = boxplot(_df)
    fig_03 = histogram(_df, x="median_house_value")
    fig_04 = piechart(_df)
    fig_05 = heatmap(_df)
    figs = reformat_figure(fig_01, fig_02, fig_03, fig_04, fig_05)
    return figs


@app.callback(
    Output(component_id='output', component_property='children'),
    Input(component_id='submit-button', component_property='n_clicks'),
    [State("input-age", "value"), State("input-ttl-rooms", "value"), State("input-ttl-bedrooms", "value"),
     State("input-ocean-proximity", "value"), State("input-population", "value"), State("input-income", "value")]
)
# age, ttls-rooms, ttl-bedrooms, ocean-proximity, income
def on_click_submit(n_clicks, *values):
    print(values)
    if any(value is None for value in values):
        return
    estimated_price = predict_price(values)
    sentence = "The house estimation is about ${:,.2f}".format(estimated_price).replace(",", " ")
    html_answer = html.Div(sentence, className="alert alert-dismissible alert-primary", id="html-output")
    return html_answer


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/estimation-tool":
        return layout_tool
    elif pathname == "/dashboard":
        return layout_dataviz
    else:
        return index_layout


# endregion


if __name__ == "__main__":
    app.run_server(debug=False)
