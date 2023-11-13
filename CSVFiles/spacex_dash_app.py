# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout

#Task 1 site options
site_options = [{'label': site, 'value': site} for site in ['All Sites'] + spacex_df['Launch Site'].unique().tolist()]


app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site_dropdown',
                                    options=site_options,
                                    value='All Sites',
                                    placeholder="Launch Sites",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                #html.Div(dcc.Graph(id='success-pie-chart')),

                                dcc.RangeSlider(
                                    id='payload-slider',
                                    marks={i: str(i) for i in range(int(min_payload), int(max_payload)+1)},
                                    min=min_payload,
                                    max=max_payload,
                                    step=1,
                                    value=[min_payload, max_payload],
                                ),

                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

"""
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site_dropdown', 'value')
)
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Define callbacks to update the app based on dropdown selection
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    Input(component_id='site_dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
def update_pie_chart(selected_site):
    if selected_site == 'All Sites':
        data = spacex_df
        title = 'Success Rate for All Sites'
    else:
        data = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Success Rate for {selected_site}'

    # Calculate success and failure counts
    success_count = data[data['class'] == 1].shape[0]
    failure_count = data[data['class'] == 0].shape[0]

    # Create a pie chart using Plotly Express
    fig = px.pie(
        names=['Success', 'Failure'],
        values=[success_count, failure_count],
        title=title,
    )

    return fig

def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'All Sites':
        data = spacex_df
        title = 'Correlation between Payload and Launch Success for All Sites'
    else:
        data = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Correlation between Payload and Launch Success for {selected_site}'

    # Apply payload filter
    data = data[(data['Payload Mass (kg)'] >= payload_range[0]) & (data['Payload Mass (kg)'] <= payload_range[1])]

    # Create a scatter chart using Plotly Express
    fig = px.scatter(
        data,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title,
        labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Success'},
    )

    return fig
"""

@app.callback(
    [Output('success-pie-chart', 'figure'),
     Output('success-payload-scatter-chart', 'figure')],
    [Input('site_dropdown', 'value'),
     Input('payload-slider', 'value')]
)

def update_charts(selected_site, payload_range):
    # Your code for updating the pie chart
    if selected_site == 'All Sites':
        data_pie = spacex_df
        title_pie = 'Success Rate for All Sites'
    else:
        data_pie = spacex_df[spacex_df['Launch Site'] == selected_site]
        title_pie = f'Success Rate for {selected_site}'

    success_count_pie = data_pie[data_pie['class'] == 1].shape[0]
    failure_count_pie = data_pie[data_pie['class'] == 0].shape[0]

    fig_pie = px.pie(
        names=['Success', 'Failure'],
        values=[success_count_pie, failure_count_pie],
        title=title_pie,
    )

    # Your code for updating the scatter chart
    if selected_site == 'All Sites':
        data_scatter = spacex_df
        title_scatter = 'Correlation between Payload and Launch Success for All Sites'
    else:
        data_scatter = spacex_df[spacex_df['Launch Site'] == selected_site]
        title_scatter = f'Correlation between Payload and Launch Success for {selected_site}'

    data_scatter = data_scatter[(data_scatter['Payload Mass (kg)'] >= payload_range[0]) & (data_scatter['Payload Mass (kg)'] <= payload_range[1])]

    fig_scatter = px.scatter(
        data_scatter,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title_scatter,
        labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Success'},
    )

    return fig_pie, fig_scatter

# Run the app
if __name__ == '__main__':
    app.run_server()
