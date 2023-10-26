#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data to dataframe using pandas
immi_data_org = pd.read_csv('canadian_immigration_data.csv',header=0)

# Initialize Dash app
app = dash.Dash(__name__)

# Set a title for the dashboard
app.title = "Canadain Immigration Dashboard"

# Initialize a variable with all the years 
# years_list = [x for x in range(1980, 2013)]
countries_list = immi_data_org.Country.unique()
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    html.H1("Canadian Immigration Statistics Dashboard",style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[{'label': 'Country-wise Statistics', 'value': 'Country-wise Statistics'},
                    {'label': 'Statistics for all countries', 'value': 'Statistics for all countries'}],
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-country',
            options=[{'label': x, 'value': x} for x in countries_list],
            value='Select country'
        )),
    html.Div([
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),])
])

@app.callback(
    Output(component_id='select-country', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Country-wise Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
        Input(component_id='select-country', component_property='value')])


def update_output_container(input_stat, input_country):
    if input_stat == 'Statistics for all countries':
        immi_data = immi_data_org.copy(deep=False)

# Plot 1 - Immigrantion trend for different countries from 1980 to 2013 
        immi_data.set_index('Country',inplace=True)
        chart1 = dcc.Graph(
            figure=px.bar(immi_data, 
                x=immi_data.index,
                y='Total',
                title="Immigration trend for different countries from 1980 to 2013"))

# Plot 2         
        immi_data = immi_data.reset_index(drop=True)
        immi_data_pie = immi_data.sort_values(['Total'],ascending=False)
        immi_data_pie = immi_data_pie[:15]
        chart2 = dcc.Graph(
            figure=px.pie(immi_data_pie, 
                values='Total',
                names=immi_data_pie.index,
                title="Total immigrants by country"))


        return [
            html.Div(className='chart-item', children=[html.Div(children=chart1),html.Div(children=chart2)],style={"display":'flex'})
            ]


 # Country-wise Statistic Report Plots                             
    elif (input_country and input_stat=='Country-wise Statistics') :
        print(input_country)
        immi_data_ctry = immi_data_org.copy(deep=True)
        years = [str(x) for x in range(1980,2014)]
        immi_data_ctry.set_index('Country',inplace=True)
        immi_data_trnps = immi_data_ctry[years].transpose()

        print("*"*18)
        print(immi_data_trnps.columns)
        print("*"*18)
                            
# plot 1 Line plot of immigrants from a specific country from 1980 to 2013
        Country_chart1 = dcc.Graph(figure=px.line(immi_data_trnps,
                                x=immi_data_trnps.index,
                                y=immi_data_trnps[input_country],
                                title = "Immigrants from {} by year".format(input_country)))
# plot 2 Pie chart of immigrants from a specific country from 1980 to 2013       
        Country_chart2 = dcc.Graph(figure=px.pie(immi_data_trnps,
                                values = immi_data_trnps[input_country],
                                names=immi_data_trnps.index,
                                title = "Immigrants from {} by year".format(input_country)))
    
        return [
                html.Div(className='chart-item', children=[html.Div(children=Country_chart1),html.Div(children=Country_chart2)],style={"display":'flex'}),
                ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

