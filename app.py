from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import random
import dash_bootstrap_components as dbc

# Utilities
from utilities import get_month_number, get_months, get_doctor_names, get_data, graphConfig, get_department_names, get_diagnosis
# Components 
from components.navbar import navbar_layout

data = get_data()

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

BACKGROUND_COLOR = "#0d0d0d"
CARD_COLOR = "#1a1a1a"
TEXT_COLOR = "#e0e0e0"
NEON_COLORS = {
    "months": "#39ff14",       # neon green
    "doctors": "#00eaff",      # neon cyan
    "departments": "#ff00ff",  # neon magenta
    "diagnosis": "#ffae00",    # neon orange
}

def styled_dropdown_group(dropdowns):
    """Wrap multiple dropdowns in one flex container"""
    return html.Div(
        dropdowns,
        className="dropdown-group"
    )

def styled_dropdown(options, value, id_, color_class):
    return dcc.Dropdown(
        options=options,
        value=value,
        id=id_,
        className=f"neon-dropdown {color_class}",
        style={
            "width": "90%",
            "margin": "10px auto",
            "fontSize": "14px",
        },
    )


# ---------------- Layout ---------------- #
app.layout = html.Div(
    [
        navbar_layout,

        html.Div(
            [
                # Graph 1
                html.Div(
                    [
                        styled_dropdown_group([
                            styled_dropdown(get_months(), random.choice(get_months()),
                                            "dropdown-selection-months", "neon-green"),
                        ]),
                        dcc.Graph(id="graph-content", config=graphConfig),
                    ],
                    className="graph-card",
                ),

                # Graph 2
                html.Div(
                    [dcc.Graph(id="graph-content-readmission-count-per-month", config=graphConfig)],
                    className="graph-card",
                ),

                # Graph 3
                html.Div(
                    [
                        styled_dropdown_group([
                            styled_dropdown(get_doctor_names(), random.choice(get_doctor_names()),
                                            "dropdown-selection-doctors", "neon-cyan"),
                        ]),
                        dcc.Graph(id="graph-content-los-comparison", config=graphConfig),
                    ],
                    className="graph-card",
                ),

                # Graph 4 (only dropdowns)
                html.Div(
                    [
        # Flex container with 2 dropdowns
        html.Div(
                        [
                            styled_dropdown(get_department_names(), random.choice(get_department_names()),
                                            "dropdown-selection-departments", "neon-magenta"),
                            styled_dropdown(get_diagnosis(), random.choice(get_diagnosis()),
                                            "dropdown-selection-diagnosis", "neon-orange"),
                        ],
                        className="dropdown-group",   # flex container
                    ),

                    # Graph container
                    dcc.Graph(id="graph-content-total-vs-readmitted-comparison", config=graphConfig),
                ],
                className="graph-card graph-flex",
                ),
            ],
            className="graph-grid",
        ),

        dcc.Location(id="url", refresh=False),
    ],
    className="main-layout"
)


# ---------------- Callbacks ---------------- #
@callback(
    Output('graph-content-readmission-count-per-month', 'figure'),
    Input('url', 'pathname')
)
def update_graph_readmission_count_per_month(pathname):
    map1 = data.groupby(['Month'])['readmitted'].count()
    dark_colors = px.colors.sequential.Viridis

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

    fig.update_layout(
        width=800,
        height=500,
        title_font=dict(size=22, color='white'),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            color='white'
        ),
        yaxis=dict(title="Readmission Count", color='white'),
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font=dict(family="Arial", size=14, color='white'),
    )
    return fig


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection-months', 'value')
)
def update_graph(month):
    refined = data[data['Month'] == get_month_number(month)]

    if refined.empty:
        empty_layout = {
            "title": f"No Data Available for {month}",
            "xaxis": {"visible": False}, "yaxis": {"visible": False},
            "annotations": [{"text": f"No data for {month}", "xref": "paper", "yref": "paper",
                             "showarrow": False, "font": {"size": 20, "color": "white"}}],
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
        width=800,
        height=500,
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
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
        x="diagnosis",
        y=["Doctor Average LOS", "Global Average LOS"],
        barmode="group",
        title=f"Length of Stay: {value} vs Global Averages",
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font=dict(size=14, color="white"),
        title=dict(font=dict(size=20)),
        legend=dict(title="Comparison", font=dict(size=12, color="white")),
        xaxis=dict(title="Diagnosis", tickangle=-30),
        yaxis=dict(title="Length of Stay (days)"),
        height=500, width=800
    )
    return fig


@callback(
    Output('graph-content-total-vs-readmitted-comparison', 'figure'),
    [Input('dropdown-selection-departments', 'value'), Input('dropdown-selection-diagnosis', 'value')]
)
def update_graph(dept, diag):
    trickled_data = data[['department', 'diagnosis', 'severity']].value_counts().reset_index()
    trickled_data = trickled_data.sort_values(by=['department', 'diagnosis', 'severity'], ascending=[1, 1, 1])

    trickled_data2 = data.groupby(['department', 'diagnosis', 'severity'])['readmitted'].sum()
    trickled_data2 = trickled_data2.reset_index()
    plot4_data = pd.merge(trickled_data, trickled_data2, on=['department', 'diagnosis', 'severity'], how='inner')

    plot4_data = plot4_data[(plot4_data['department'] == dept) & (plot4_data['diagnosis'] == diag)]
    plot4_data = plot4_data[['severity', 'count', 'readmitted']]

    fig = px.bar(
        plot4_data,
        x="severity",
        y=["count", "readmitted"],
        barmode='group',
        title=f'Total admitted vs Readmitted in {dept} ({diag})'
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font=dict(size=14, color="white"),
        title=dict(font=dict(size=20)),
        legend=dict(title="Comparison", font=dict(size=12, color="white")),
        xaxis=dict(title="Severity"),
        yaxis=dict(title="Patient Count"),
        height=500, width=800
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True, dev_tools_hot_reload=True, dev_tools_silence_routes_logging=True)
