import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

# establish order of subjects in analysis
order = ["Astronomy","Art","3D Design","English Lang.","English Lit.","Maths","Further Maths","Biology","Chemistry","Physics","Combined Science","Economics","Geography","History","Drama","Film Studies","PE","Food Prep. & Nut.","French","Spanish","Computer Science", "Music"]
order_copy = order[:]

# Lists subjects without baseline data
Exclude = ["Astronomy","Further Maths","Economics"]
order_Yell_diff = [e for e in order_copy if e not in Exclude]

# establish dataframe
merged_yellis_diff_with_exams = pd.read_csv('/Users/colinknight/Documents/Data Files/Results_App/merged_yellis_diff_with_exams.csv')

# convert exam series to categorical dtype and specify order of the exam series to helpn with graphing
merged_yellis_diff_with_exams["Exam_Series"] = pd.Categorical(merged_yellis_diff_with_exams["Exam_Series"],["MOCK 1", "MOCK 2", "GCSE", "BASELINE"])

#establish chart layouts
box_layout = go.Layout(autosize=True, margin=go.layout.Margin(l=25,r=25,b=25,t=80), plot_bgcolor='white', yaxis_range=[0,9.5])
scatter_layout = go.Layout(autosize=True, margin=go.layout.Margin(l=25,r=25,b=25,t=80), plot_bgcolor='white', yaxis_range=[0,9.5])


box_app_fig = go.Figure(layout=box_layout)
scatter_fig = go.Figure(layout=scatter_layout)
student_fig = go.Figure(layout=scatter_layout)

options = [{'label':i,'value':i} for i in order]

#school logo
logo_link = 'https://ibb.co/Y0Q8BF8'

#establish plots

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
colors = {'background':'white','header_background':'rgb(1,39,1)','header_text':'rgb(223,188,106)'}

app.layout = dbc.Container(style={'backgroundColor': colors['header_background']}, children = [
  dbc.Row([
      dbc.Col(html.Img(src=logo_link), width = 4, style={'margin':'10px 0px 10px 0px','height':'8%','width':'8%'}),
      dbc.Col(html.H1('Results breakdown', style={'color':colors['header_text']}), width = 8, align = 'center')
  ]),
  dbc.Row(      
        html.H3('Subject Tracking', style={'color':colors['header_text']})
        ),
  dbc.Row(     
        dcc.Dropdown(id='sub_select', options = options)
  ),
  dbc.Row(
    [dbc.Col(dcc.Graph(id='box_fig', figure=box_app_fig, config={"displayModeBar": False}), width = 8, style={'margin-top':'10px'}),
    dbc.Col(dcc.Graph(id='student_scatters', figure=scatter_fig, config={"displayModeBar": False}), width = 4, style={'margin-top':'10px'})
  ],className="g-0"),
  dbc.Row(
    html.H3('Subject comparison for selected student', style={'margin-top':'20px','color':colors['header_text']})),
  dbc.Row(
    dbc.Col(dcc.Graph(id='student_focus', figure=student_fig, config={"displayModeBar": False}), style={'margin-top':'0px', 'border':'1px solid black'})
        )
], fluid=True)


@app.callback(
    Output('box_fig','figure'),
    Input('sub_select','value')
)
def box_plot(value):

  comp_subset_GCSE = merged_yellis_diff_with_exams.loc[(merged_yellis_diff_with_exams["Subject"]==value) & (merged_yellis_diff_with_exams["Exam_Series"]=="GCSE")]
  comp_subset_Y10 = merged_yellis_diff_with_exams.loc[(merged_yellis_diff_with_exams["Subject"]==value) & (merged_yellis_diff_with_exams["Exam_Series"]=="MOCK 1")]
  comp_subset_Y11 = merged_yellis_diff_with_exams.loc[(merged_yellis_diff_with_exams["Subject"]==value) & (merged_yellis_diff_with_exams["Exam_Series"]=="MOCK 2")]
  comp_subset_YELLIS = merged_yellis_diff_with_exams.loc[(merged_yellis_diff_with_exams["Subject"]==value) & (merged_yellis_diff_with_exams["Exam_Series"]=="BASELINE")]
  box_app_fig = go.Figure(layout=box_layout)

  box_app_fig.add_trace(go.Box(y=comp_subset_Y10["Score"], name="MOCK 1", fillcolor='rgba(93, 164, 214, 0.5)', boxpoints='all', jitter=0.6, customdata=np.stack((comp_subset_Y10["Student"],comp_subset_Y10["Score"]),axis=-1), hovertemplate='<b>%{customdata[0]}<b><br>' + '<b>Mock 1:<b> %{customdata[1]}'))
  box_app_fig.add_trace(go.Box(y=comp_subset_Y11["Score"], name="MOCK 2", fillcolor='rgba(255, 144, 14, 0.5)', boxpoints='all', jitter=0.6, customdata=np.stack((comp_subset_Y11["Student"],comp_subset_Y11["Score"]),axis=-1), hovertemplate='<b>%{customdata[0]}<b><br>' + '<b>Mock 2:<b> %{customdata[1]}'))
  box_app_fig.add_trace(go.Box(y=comp_subset_GCSE["Score"], name="GCSE", fillcolor='rgba(44, 160, 101, 0.5)', boxpoints='all', jitter=0.6, customdata=np.stack((comp_subset_GCSE["Student"],comp_subset_GCSE["Score"]),axis=-1), hovertemplate='<b>%{customdata[0]}<b><br>' + '<b>GCSE:<b> %{customdata[1]}'))
  box_app_fig.add_trace(go.Box(y=comp_subset_YELLIS["Score"], name="BASELINE", fillcolor='rgba(255, 65, 54, 0.5)', boxpoints='all', jitter=0.6, customdata=np.stack((comp_subset_YELLIS["Student"],comp_subset_YELLIS["Score"]),axis=-1), hovertemplate='<b>%{customdata[0]}<b><br>' + '<b>BASELINE:<b> %{customdata[1]}'))
  box_app_fig.update_yaxes(labelalias={0:"U"}, dtick=1, gridcolor='lightgrey', griddash='dash')
  box_app_fig.update_xaxes(showline=True, linewidth=2, linecolor='lightgrey')
     
  box_app_fig.update_layout(yaxis_range=[0,9.5], yaxis_title=f'<b>Grade</b>', xaxis_title=f"<b>Exam Series</b>")
  box_app_fig.update_layout(title=f'<b>{value}: </b>'+ str(len(comp_subset_GCSE)) + ' students', yaxis_range=[0,9.5], showlegend=False)

  return box_app_fig

@app.callback(
    Output('student_scatters','figure'),
    [Input('sub_select','value'),Input('box_fig','hoverData')]
)

def scatter_plot(value, hoverData):
  scatter_fig = go.Figure(layout=scatter_layout)
  Progress_Exam_subset = merged_yellis_diff_with_exams.loc[merged_yellis_diff_with_exams["Subject"]==value].sort_values(by=["Student","Exam_Series"]).copy()
  student_list_progress = Progress_Exam_subset["Student"][Progress_Exam_subset["Exam_Series"]=="GCSE"].unique().tolist()

  if hoverData:
    if hoverData['points'][0]['customdata'][0] in student_list_progress and value in order_Yell_diff:
      hover_student = hoverData['points'][0]['customdata'][0]
      trace_subset = Progress_Exam_subset[Progress_Exam_subset["Student"]==hover_student].sort_values(by=["Student","Exam_Series"]).copy()
      yellis_target = float(trace_subset["Score"].loc[trace_subset["Exam_Series"]=="BASELINE"].iloc[0])
      trace_color= [colour for colour in trace_subset.colour.loc[:]]
      tracking_subset = trace_subset.loc[trace_subset["Exam_Series"]!="BASELINE"].copy()
      yellis_subset = trace_subset.loc[trace_subset["Exam_Series"]=="BASELINE"].copy()
      max_result = tracking_subset.loc[:,"Score"].max()
      min_result = tracking_subset.loc[:,"Score"].min()
      diff = pd.Series(max_result - min_result)
      yellis_subset.loc[:,"max_score"] = max_result
      yellis_subset.loc[:,"low_score"] = min_result
      
      scatter_fig.add_trace(go.Scatter(name=f'GCSE vs. Yellis: ' + str(trace_subset["Yellis_GCSE_Diff"].tolist()[0]), y=tracking_subset["Score"], x=tracking_subset["Exam_Series"], mode="lines+markers",customdata=np.stack((tracking_subset["Student"],tracking_subset["Exam_Series"],tracking_subset["Score"]),axis=-1), hovertemplate='<b>%{customdata[0]}<b><br>' + '<b>%{customdata[1]} Grade:<b> %{customdata[2]}', marker=dict(color='white',size=8,symbol='circle',line=dict(color=trace_color,width=2)), line=dict(color=trace_color[0])))
      scatter_fig.add_trace(go.Scatter(name='', y=yellis_subset["Score"], x=yellis_subset["Exam_Series"], mode="lines+markers",customdata=np.stack((yellis_subset["Student"],yellis_subset["Exam_Series"],yellis_subset["Score"]),axis=-1), hovertemplate='<b>%{customdata[0]}<b><br>' + '<b>%{customdata[1]} Grade:<b> %{customdata[2]}', marker=dict(color=trace_color[0],size=8,symbol='circle',line=dict(color='black',width=2)), line=dict(color=trace_color[0])))
      scatter_fig.update_xaxes(categoryorder='array', categoryarray=["MOCK 1","MOCK 2","GCSE","BASELINE"], showline=True, linewidth=2, linecolor='lightgrey')
      scatter_fig.add_hline(y=yellis_target, line_width=1.5, line_dash='dash', line_color=trace_color[0])
      scatter_fig.add_trace(go.Bar(name='', x=yellis_subset["Exam_Series"], y=diff, base=min_result, width=0.02, marker_color='black', showlegend=False, hoverinfo='skip'))
      scatter_fig.add_trace(go.Scatter(name="", mode="lines+markers", y=yellis_subset["max_score"], x=yellis_subset["Exam_Series"], marker=dict(symbol='triangle-down',color='black',size=8), hoverinfo='skip'))
      scatter_fig.add_trace(go.Scatter(name="", mode="lines+markers", y=yellis_subset["low_score"], x=yellis_subset["Exam_Series"], marker=dict(symbol='triangle-up',color='black',size=8), hoverinfo='skip'))

      scatter_fig.update_layout(title=f'<b>{hover_student}: </b><br>' + str(value))
      scatter_fig.update_layout(xaxis_title=f'<b>Exam Series</b>')
      scatter_fig.update(layout_showlegend=False)
      scatter_fig.update_yaxes(labelalias={0:"U"}, dtick=1, gridcolor='lightgrey', griddash='dash')

    else:
      scatter_fig = go.Figure(layout=scatter_layout)
 
  return scatter_fig

@app.callback(
    Output('student_focus','figure'),
    Input('box_fig','clickData')
)
def student_highlight(clickData):
  student_fig = go.Figure(layout=scatter_layout)

  if clickData:
    student_lookup = clickData['points'][0]['customdata'][0]
    student_subset = merged_yellis_diff_with_exams[merged_yellis_diff_with_exams["Student"]==student_lookup].sort_values(by=["Subject","Exam_Series"])
    GCSE_Student = student_subset[student_subset["Exam_Series"]=="GCSE"]
    Yellis_Student = student_subset[student_subset["Exam_Series"]=="BASELINE"]

    student_fig.add_trace(go.Scatter(name='GCSE Outcome', x=GCSE_Student["Subject"],y=GCSE_Student["Score"], mode='lines+markers', marker=dict(color='white',size=10,symbol='circle',line=dict(color='blue',width=2)),line=dict(color='blue',width=2)))
    student_fig.add_trace(go.Scatter(name='Baseline Data', x=Yellis_Student["Subject"],y=Yellis_Student["Score"], mode='lines+markers',marker=dict(color='white',size=10,symbol='circle',line=dict(color='black',width=2)),line=dict(color='black',width=2)))

    student_fig.update_layout(title=f'<b>{student_lookup}: </b>Subject comparison')
    student_fig.update_yaxes(labelalias={0:"U"}, dtick=1, gridcolor='lightgrey', griddash='dash')
    student_fig.update_xaxes(showline=True, linewidth=2, linecolor='lightgrey', gridcolor='lightgrey', griddash='dash')
    student_fig.update_layout(yaxis_range=[0,9.5])

  return student_fig
                        

if __name__ == '__main__':
    app.run_server(debug=False)