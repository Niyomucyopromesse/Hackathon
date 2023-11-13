import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load data for agriculture area
df = pd.read_excel("NISR.xlsx", sheet_name='Table1', header=2)
notcol = ['Unnamed: 0', 'Seasonal', 'years']
valid = [col for col in df.columns if col not in notcol]

# Load data for agriculture inputs
df1 = pd.read_excel("NISR.xlsx", sheet_name='Table2', header=2)
notcol1 = ['Unnamed: 0', 'seasons', 'years']
valid1 = [col for col in df1.columns if col not in notcol1]

# Load data for cultivated area by cropping systems
df2 = pd.read_excel("NISR.xlsx", sheet_name='Table3', header=2)
notcol2 = ['Unnamed: 0', 'years', 'Seasonal']
valid2 = [col for col in df2.columns if col not in notcol2]

# data for agriculture practice
df3 = pd.read_excel("NISR.xlsx", sheet_name='Table4', header=2)
df3.columns = df3.columns.str.strip()
notcol3 = ['Unnamed: 0', 'years', 'Seasonal']
valid3 = [col for col in df3.columns if col not in notcol3]

app = dash.Dash(__name__)

# light and dark themes
light_theme = {'background_color': 'white', 'font_color': 'black', 'theme_label_color': 'black'}
dark_theme = {'background_color': 'black', 'font_color': 'white', 'theme_label_color': 'white'}

#default theme
current_theme = light_theme

app.layout = html.Div(children=[
    html.H1('SEASONAL AGRICULTURE SURVEY', style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.B('Select year'),
            dcc.Dropdown(
                id='year',
                options=[
                    {'label': str(year), 'value': str(year)} for year in df['years'].unique()
                ],
                value=str(df['years'].unique()[0]),
                style={'width': '100%', 'color': current_theme['font_color']}  
            ),
        ], className='menu-container'),

        html.Div([
            html.B('change theme'),
            dcc.RadioItems(
                id='theme-switcher',
                options=[
                    {'label': 'Light ', 'value': 'light'},
                    {'label': 'Dark ', 'value': 'dark'},
                ],
                value='dark',
                labelStyle={'display': 'block', 'color': 'font_color'}  
            ),
        ], className='theme-switcher-container'),
    ], id='left-column', className='left-column', style={'background-color': current_theme['background_color'], 'color': current_theme['font_color']}),

    html.Div([
        html.Div([
            html.P('GRAPH OF AGRICULTURE INPUTS'),
            dcc.Dropdown(
                id="finputs2",
                options=[{'label': col1, 'value': col1} for col1 in valid1],
                value=valid1[0],
                style={'width': '100%', 'color': current_theme['font_color']}  
            ),
            dcc.Graph(id='agrinputs', className='graph-container')
        ], className='graph-container'),
        
        html.Div([
            html.P('GRAPH OF AGRICULTURE AREA'),
            dcc.Dropdown(
                id='finputs1',
                options=[{'label': col, 'value': col} for col in valid],
                value=valid[3],
                style={'width': '100%', 'color': current_theme['font_color']} 
            ),
            dcc.Graph(id='agriarea', className='graph-container'),
        ], className='graph-container'),


        html.Div([
            html.P('GRAPH OF CULTIVATED AREA BY CROPPING SYSTEM'),
            dcc.Dropdown(
                id='finputs3',
                options=[
                    {'label': col, 'value': col} for col in valid2
                ],
                value='Percentage of area by Pure cropping system',
                style={'width': '100%', 'color': current_theme['font_color']}  
            ),
            dcc.Graph(id='agricul', className='graph-container'),
        ], className='graph-container'),

        html.Div([
            html.P('GRAPH OF AGRICULTURE PRACTICE'),
            dcc.Dropdown(
                id='finputs4',
                options=[
                    {'label': col, 'value': col} for col in valid3
                ],
                value='Percentage of farmers who practiced irrigation',
                style={'width': '100%', 'color': current_theme['font_color']}  
            ),
            dcc.Graph(id='agripractice', className='graph-container')
        ], className='graph-container'),
    ], className='right-column')
], id='main-container')


# callback for theme switcher and agriculture area
@app.callback(
    [Output('main-container', 'style'),
     Output('left-column', 'style'),
     Output('agriarea', 'figure'),
     Output('agrinputs', 'figure'),
     Output('agricul', 'figure'),
     Output('agripractice', 'figure')],
    [Input('year', 'value'),
     Input('finputs1', "value"),
     Input('finputs2', 'value'),
     Input('finputs3', 'value'),
     Input('finputs4', 'value'),
     Input('theme-switcher', 'value')]
)
def update_layout_and_graphs(year, drop1, drop2, drop3, drop4, selected_theme):
    global current_theme
    if selected_theme == 'light':
        current_theme = light_theme
    elif selected_theme == 'dark':
        current_theme = dark_theme

    # Update the style for the main container
    main_container_style = {'backgroundColor': current_theme['background_color'], 'color': current_theme['font_color']}
    left_style = {'backgroundColor': current_theme['background_color'], 'color': current_theme['font_color']}

    data1 = df[df['years'] == int(year)]
    chart1 = px.bar(data1, x='Seasonal', y=drop1, color='Seasonal', color_discrete_sequence=['blue', 'skyblue'],text=drop1)
    chart1.update_layout(transition_duration=500, plot_bgcolor=current_theme['background_color'],
                          paper_bgcolor=current_theme['background_color'], font=dict(color=current_theme['font_color']))
    chart1.update_layout(annotations=[dict(text=str(val), x=season, y=value, showarrow=False)
                                  for season, value, val in zip(chart1.data[0].x, chart1.data[0].y, chart1.data[0].text)])
    chart1.update_layout(title_text=drop1,xaxis_title=None)  
    chart1.update_xaxes(showgrid=False)
    chart1.update_yaxes(showgrid=False)
    



    data2 = df1[df1['years'] == int(year)]
    chart2 = px.bar(data2, x='seasons', y=drop2, color='seasons', text= drop2, color_discrete_sequence=['#03045e', '#0077b6', '#90e0ef'])
    chart2.update_layout(transition_duration=500, plot_bgcolor=current_theme['background_color'],
                          paper_bgcolor=current_theme['background_color'], font=dict(color=current_theme['font_color']),xaxis_title=None)
    chart2.update_layout(annotations=[dict(text=str(val), x=season, y=value, showarrow=False)
                                  for season, value, val in zip(chart2.data[0].x, chart2.data[0].y, chart2.data[0].text)])

    chart2.update_layout(title_text=drop2)  
    chart2.update_xaxes(showgrid=False)
    chart2.update_yaxes(showgrid=False)
    line_chart = px.line(data2, x='seasons', y=drop2, color='seasons', line_group='seasons', markers=True)
    line_chart.update_layout(showlegend=False)

    chart2.update_traces(line=dict(width=2), selector=dict(type='scatter', mode='lines'),line_dash='solid')


    chart2.add_traces(line_chart.data)



    data3 = df2[df2['years'] == int(year)]
    chart3 = px.pie(data3, names='Seasonal', values=drop3, hole=0.5,color_discrete_sequence=['#03045e', '#0077b6', '#90e0ef'])
    chart3.update_layout(transition_duration=500, plot_bgcolor=current_theme['background_color'],
                          paper_bgcolor=current_theme['background_color'], font=dict(color=current_theme['font_color']))
    chart3.update_layout(title_text=drop3)  




    data4 = df3[df3['years'] == int(year)]
    drop4_cleaned = drop4.strip()
    chart4 = px.pie(data4, names='Seasonal', values=drop4_cleaned,color_discrete_sequence=['#03045e', '#0077b6', '#90e0ef'],labels={'Seasonal': ''})
    chart4.update_layout(transition_duration=500, plot_bgcolor=current_theme['background_color'],
                          paper_bgcolor=current_theme['background_color'], font=dict(color=current_theme['font_color']))
    chart4.update_layout(title_text=drop4) 

    return main_container_style, left_style, chart1, chart2, chart3, chart4


if __name__ == '__main__':
    app.run_server(debug=True, port=8054)
