""" To Handle the frontend """

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import random
import dash_bootstrap_components as dbc
from datetime import datetime

#Utilities
from utilities import get_month_number, get_months, get_doctor_names, get_data, graphConfig, get_department_names, get_diagnosis

#Components 
from components.navbar import navbar_layout

data = get_data()

data['Month'] = data['dischargedate'].apply(

    lambda dt: ((((datetime.strptime(dt, '%Y-%m-%d')).month)% 12)) + 1
)


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


app.layout = [
    html.H1(children='Hospital Readmission Dashboard for Analysis', style={'textAlign':'center'}),
    
    html.Br(),
    html.Br(),
    dcc.Dropdown(
        options=get_months(),
        value=random.choice(get_months()),
        id='dropdown-selection-months',
        # The 'style' property allows you to apply inline CSS
        style={
            'width': '50%',             # 1. Makes the dropdown half the width of its container
            'margin': '0 auto',         # Centers the dropdown on the page
            'color': '#212121'          # Sets the color of the selected text to dark grey
        }
    ),
    
    dcc.Graph(id='graph-content', config=graphConfig),

    html.Br(),
    html.Br(),

    dcc.Location(id='url', refresh=False),
    dcc.Graph(id='graph-content-readmission-count-per-month', config=graphConfig),

    html.Br(),
    dcc.Dropdown(
        options=get_doctor_names(),
        value = random.choice(get_doctor_names()),
        id='dropdown-selection-doctors',
        style={
            'width': '50%',             
            'margin': '0 auto',         
            'color': '#212121'          
        }
    ),

    dcc.Graph(id='graph-content-los-comparison', config = graphConfig),

    html.Br(),
    dcc.Dropdown(

        options = get_department_names(),
        value = random.choice(get_department_names()),
        id = 'dropdown-selection-departments',
        style = {    
            'width': '50%',             
            'margin': '0 auto',         
            'color': '#212121'          
        }
    ),
 
    html.Br(),

    dcc.Dropdown(

        options = get_diagnosis(),
        value = random.choice(get_diagnosis()),
        id = 'dropdown-selection-diagnosis',
        style = {    
            'width': '50%',             
            'margin': '0 auto',         
            'color': '#212121'          
        }
    ),
    
    dcc.Graph(id = 'graph-content-total-vs-readmitted-comparison', config=graphConfig),
    html.Br(),
]


# ----- Callback Functions ------

@callback(
        Output('graph-content-readmission-count-per-month', 'figure'),
        Input('url', 'pathname')
)
def update_graph_readmission_count_per_month(pathname):

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
        height=650,
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


@callback(

    Output('graph-content-los-comparison', 'figure'),
    Input('dropdown-selection-doctors', 'value')
)
def update_graph(value):
    plot3_data = data.groupby(['doctorname', 'severity', 'diagnosis'])['length_of_stay'].mean()
    plot3_data_glob = data.groupby(['severity', 'diagnosis'])['length_of_stay'].mean()

    plot3_data = plot3_data.reset_index()
    plot3_data_glob = plot3_data_glob.reset_index()


    plot3_data = pd.merge(plot3_data, plot3_data_glob, on=['severity', 'diagnosis'], how='inner')


    plot3_data['length_of_stay_y'] = plot3_data['length_of_stay_y'].astype(int)
    plot3_data['length_of_stay_x'] = plot3_data['length_of_stay_x'].astype(int)

    plot3_data.rename(columns={
        'length_of_stay_x': 'Doctor Average LOS',
        'length_of_stay_y': 'Global Average LOS'
    }, inplace=True)

    plot3_data = plot3_data[plot3_data['doctorname'] == value]


    fig = px.bar(
        plot3_data,
        x="diagnosis",  # diseases on x-axis
        y=["Doctor Average LOS", "Global Average LOS"],  # grouped bars
        barmode="group",
        title=f"Length of Stay: {value} vs Global Averages",
    )


    fig.update_layout(
        template="plotly_dark",          # dark background
        plot_bgcolor="black",            # black plotting area
        paper_bgcolor="black",           # black outside
        font=dict(size=16, color="white"),  # bigger readable font
        title=dict(font=dict(size=22)),  # bigger title
        legend=dict(
            title="Comparison",
            font=dict(size=14, color="white")
        ),
        xaxis=dict(title="Diagnosis", tickangle=-30),  # rotate x labels
        yaxis=dict(title="Length of Stay (days)"),
        height=650, width=1500           # bigger figure size
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True, dev_tools_hot_reload=True, dev_tools_silence_routes_logging=True)
