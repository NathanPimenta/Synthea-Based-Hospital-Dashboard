""" To Handle the frontend """

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import random
import dash_bootstrap_components as dbc
from sklearn.preprocessing import LabelEncoder

from datetime import datetime

data = pd.read_csv('Datasets/HCP.csv')
le = LabelEncoder()

data['Month'] = data['dischargedate'].apply(

    lambda dt: ((((datetime.strptime(dt, '%Y-%m-%d')).month)% 12)) + 1
)


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

months = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
month_options = list(months.values())

def get_month_number(month_name):
    for number, name in months.items():
        if name == month_name:
            return number
    return None

app.layout = [
    html.H1(children='Hospital Readmission Dashboard for Analysis', style={'textAlign':'center'}),
    
    html.Br(),
    html.Br(),
    dcc.Dropdown(
        options=month_options,
        value=random.choice(month_options),
        id='dropdown-selection-months',
        # The 'style' property allows you to apply inline CSS
        style={
            'width': '50%',             # 1. Makes the dropdown half the width of its container
            'margin': '0 auto',         # Centers the dropdown on the page
            'color': '#212121'          # Sets the color of the selected text to dark grey
        }
    ),
    
    dcc.Graph(id='graph-content'),

    html.Br(),
    html.Br(),

    dcc.Location(id='url', refresh=False),
    dcc.Graph(id='graph-content-readmission-count-per-month')
]

@callback(
        Output('graph-content-readmission-count-per-month', 'figure'),
        Input('url', 'pathname')
)
def update_graph_readmission_count_per_month(pathname):

    data['readmitted'] = le.fit_transform(data['readmitted'])
    map1 = data.groupby(['Month'])['readmitted'].count()

    dark_colors = px.colors.sequential.Viridis

# Create bar chart
    fig = px.bar(
        map1.reset_index(),
        x='Month',
        y='readmitted',
        text='readmitted',
        title="Readmission Count per Month",
        color='Month',
        color_continuous_scale=dark_colors
    )

    fig.update_traces(textposition='outside')

    # Dark layout styling
    fig.update_layout(
        width=1000,
        height=500,
        title_font=dict(size=26, color='white'),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            color='white'
        ),
        
        yaxis=dict(
            title="Readmission Count",
            color='white'
        ),
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e",
        font=dict(family="Arial", size=16, color='white'),
    )

    return fig

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection-months', 'value')
)
def update_graph(month):
    
    
    # Filter the DataFrame
    refined = data[data['Month'] == get_month_number(month)]

    if refined.empty:
        empty_layout = {
            "title": f"No Data Available for {month}",
            "xaxis": {"visible": False}, "yaxis": {"visible": False},
            "annotations": [{"text": f"No data for {month}", "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 20, "color": "white"}}],
            "plot_bgcolor": 'rgba(0,0,0,0)', "paper_bgcolor": 'rgba(0,0,0,0)', "font_color": 'white'
        }
        return {"layout": empty_layout}

    mapForDiagandSever1Month = refined.groupby(['diagnosis', 'severity'])['readmitted'].count().reset_index()
    mapForDiagandSever1Month.columns = ['Diagnosis', 'Severity', 'ReadmissionCount']

    fig = px.bar(
        mapForDiagandSever1Month, 
        x='Diagnosis', y='ReadmissionCount', color='Severity', 
        title=f'Readmission Count for {month}', text='ReadmissionCount'
    )

    fig.update_traces(textposition='inside', insidetextanchor='middle')
    
    fig.update_layout(
        barmode='stack',
        xaxis_tickangle=-45,
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        width=1000,
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)