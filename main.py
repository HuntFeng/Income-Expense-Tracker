import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable
import plotly.graph_objects as go
import plotly.express as px

import base64
import io

import pandas as pd
import numpy as np
from dataframe_preprocess import preprocess_dataframe

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True # the data table depends on the layout which is dynamically generated, so suppress this
) 

app.layout = html.Div([
    html.Center(html.H1("Visualization of Incomes and Expenses")),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ',html.A('Select Your File'), ' Containing Transactions (CSV ONLY)']),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'font-size': '20px',
            'margin-bottom': '10px'
        },
        # Does NOT Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='visualization-area'),
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
        preprocess_dataframe(df)
        
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    return analysis_layout(df)


@app.callback(Output('visualization-area', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(content, filename):
    if content:
        children = [parse_contents(content, filename)]
        return children


def analysis_layout(df):
    # income
    global income 
    income = df[df["Credit"]!=0]
    total_income = income["Credit"].sum()
    income_of_specific_type = {}
    for Type in income["Type"].unique():
        income_of_specific_type[Type] = income[income["Type"] == Type]["Credit"].sum()
    income_of_specific_type = pd.Series(income_of_specific_type)
    # in ploly ascending is the reverse of that in seaborn   
    income_of_specific_type.sort_values(ascending=True,inplace=True) 
    income_fig = go.Figure(go.Bar(
            x=income_of_specific_type.values,
            y=income_of_specific_type.index,
            orientation='h',
            )
        )
    income_fig.update_layout(font={"size":15})
    income_pie_chart = px.pie(
        income_of_specific_type, 
        values=income_of_specific_type.values, 
        names= income_of_specific_type.index
    )
    income_pie_chart.update_layout(font={"size":15})

    # expense
    global expense 
    expense = df[df["Debit"]!=0]
    total_expense = expense["Debit"].sum()
    expense_of_specific_type = {}
    for Type in expense["Type"].unique():
        expense_of_specific_type[Type] = expense[expense["Type"] == Type]["Debit"].sum()
    expense_of_specific_type = pd.Series(expense_of_specific_type)
    expense_of_specific_type.sort_values(ascending=True,inplace=True)
    expense_fig = go.Figure(go.Bar(
            x=expense_of_specific_type.values,
            y=expense_of_specific_type.index,
            orientation='h',
            )
        )
    expense_fig.update_layout(font={"size":15})
    expense_pie_chart = px.pie(
        expense_of_specific_type, 
        values=expense_of_specific_type.values, 
        names= expense_of_specific_type.index
    )
    expense_pie_chart.update_layout(font={"size":15})
    
    div = html.Div([
        dcc.Tabs([
            dcc.Tab(
                label="Components of Income",
                children=[
                    html.H2("Components of Income"),
                    html.H4(f"Total Income: {total_income} CAD"),
                    dcc.Graph(figure=income_fig),
                    dcc.Graph(figure=income_pie_chart),
                    dcc.Dropdown(
                        id='income-dropdown',
                        options=[
                            {"label": label, "value": label} for label in income["Type"].unique()
                        ],
                        value=income["Type"].unique()[0]
                    ),
                    html.Div(id='income-table'),
                ]
            ),

            dcc.Tab(
                label="Components of Expense",
                children=[
                    html.H2("Components of Expense"),
                    html.H4(f"Total Expense: {total_expense} CAD"),
                    dcc.Graph(figure=expense_fig),

                    html.Hr(),
                    html.H3("Details of expense of specific type"),
                    dcc.Graph(figure=expense_pie_chart),
                    dcc.Dropdown(
                        id='expense-dropdown',
                        options=[
                            {"label": label, "value": label} for label in expense["Type"].unique()
                        ],
                        value=expense["Type"].unique()[0]
                    ),
                    html.Div(id='expense-table')
                ]
            )
        ])
    ])
    return div

def detail_transactions(input_df,Type):
    ddf = input_df[input_df["Type"]==Type]
    if len(ddf)<= 50:
        return html.Div([
            html.P("Less than 50 transactions, showing all results"),
            DataTable(
                columns=[{"name": i, "id": i} for i in ddf.columns],
                data=ddf.to_dict('records'),
            )
        ])
    else:
        if (ddf["Debit"] == 0).all():
            # all debit numbers are 0, so it is a dataframe of income
            data_of_specific_type = input_df[input_df["Type"]==Type]["Credit"]
        else:
            data_of_specific_type = input_df[input_df["Type"]==Type]["Debit"]
        mean = data_of_specific_type.mean()
        std = data_of_specific_type.std()
        zscore = (data_of_specific_type-mean)/std
        unnormal = data_of_specific_type[zscore > 1]
        ddf = input_df.loc[unnormal.index]
        return html.Div([
            html.P(f"Mean amount: {round(mean,2)} CAD"),
            html.P(f"Standard Deviation: {round(std,2)} CAD"),
            html.P("Too many transactions, only show those with amount > 1 standard deviation ..."),            
            DataTable(
                columns=[{"name": i, "id": i} for i in ddf.columns],
                data=ddf.to_dict('records'),
            ) 
        ])

@app.callback(
    Output('income-table', 'children'),
    [Input('income-dropdown', 'value')])
def update_income_table(Type: str):
    return detail_transactions(income, Type)

@app.callback(
    Output('expense-table', 'children'),
    [Input('expense-dropdown', 'value')])
def update_expense_table(Type: str):
    return detail_transactions(expense, Type)


if __name__ == '__main__':
    app.run_server()