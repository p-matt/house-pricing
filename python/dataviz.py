import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

px.set_mapbox_access_token("pk.eyJ1IjoicC1tYXR0IiwiYSI6ImNrd2MxZGVoMTNxYmkydXJvbmJ5bWJlM24ifQ.Cb4ErYW8qlMv8j0sS2hVBQ")


def init():
    global df
    df = pd.read_csv('../jupyter/data/housing.csv')
    df['total_rooms'] = df['total_rooms'] / df['households']
    df['total_bedrooms'] = df['total_bedrooms'] / df['households']
    df['population'] = df['population'] / df['households']
    df = df[['housing_median_age', 'total_rooms', 'total_bedrooms', 'median_income', 'population', 'ocean_proximity',
             "longitude", "latitude", "median_house_value"]]


def mapbox(_df):
    return px.scatter_mapbox(data_frame=_df, lat="latitude", lon="longitude", color="median_house_value",
                             center=dict(lat=38, lon=-120), zoom=4.75).update_layout(margin=dict(l=5, r=5, b=5, t=5),
                                                                                     width=600, height=500)


def boxplot(_df):
    fig = go.Figure()
    cols = ['housing_median_age', 'total_rooms', 'total_bedrooms', 'median_income', 'population']
    for col in cols:
        fig.add_trace(go.Box(y=_df[col].values, name=_df[col].name))
    fig.update_yaxes(type="log")
    return fig.update_layout(width=600, height=500)


def histogram(_df, x):
    return px.histogram(_df, x=x).update_layout(margin=dict(l=5, r=5, b=5, t=5), height=500)


def piechart(_df):
    return px.pie((_df['ocean_proximity'].value_counts(normalize=True) * 100).round(2).reset_index(), names='index',
                  values='ocean_proximity').update_traces(textposition='inside', textinfo='percent+label')


def heatmap(_df):
    dfc = _df.select_dtypes(np.number).corr()
    z = dfc.values.tolist()
    z_text = [[str(round(y, 2)) for y in x] for x in z]
    fig = ff.create_annotated_heatmap(z, x=list(_df.select_dtypes(np.number).columns),
                                      y=list(_df.select_dtypes(np.number).columns),
                                      annotation_text=z_text, colorscale='agsunset')

    # add custom xaxis title
    fig.add_annotation(dict(font=dict(color="black", size=14),
                            x=0.5,
                            y=-0.15,
                            showarrow=False,
                            text="",
                            xref="paper",
                            yref="paper"))

    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="black", size=10),
                            x=-0.35,
                            y=0.5,
                            showarrow=False,
                            text="",
                            textangle=-70,
                            xref="paper",
                            yref="paper"))
    # add colorbar
    fig['data'][0]['showscale'] = True
    return fig


def reformat_figure(*figs):
    new_figs = []
    for fig, title in zip(figs, titles):
        new_figs.append(fig.update_layout(margin=dict(l=5, r=5, b=5, t=50), title=title))
    return new_figs


titles = ["House value in California", "Quantitative analysis", "House value - Histogram",
          "Ocean proximity distribution", "Heatmap - Correlation matrix"]
df = None

init()
