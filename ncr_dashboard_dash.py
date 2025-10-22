import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# تحميل البيانات
def load_data():
    ncr = pd.read_excel('/media/hesham/Y/my ubntu inv/projects/data/NCR_8_25.xlsx')
    ncr['شهر'] = pd.to_datetime(ncr['شهر'], errors='coerce')
    return ncr

ncr = load_data()

# إنشاء تطبيق Dash
app = dash.Dash(__name__, external_stylesheets=[
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap'
])

# تخصيص CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NCR Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                font-family: 'Tajawal', sans-serif;
            }
            .main-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .card {
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                padding: 20px;
                margin: 10px;
                transition: transform 0.3s ease;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .metric-card {
                text-align: center;
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                color: white;
                border-radius: 15px;
                padding: 20px;
            }
            .header {
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                border-radius: 0 0 20px 20px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# تخطيط الداشبورد
app.layout = html.Div(className='main-container', children=[
    # الهيدر
    html.Div(className='header', children=[
        html.Div(className='container-fluid', children=[
            html.Div(className='row align-items-center', children=[
                html.Div(className='col-md-6', children=[
                    html.H1("📊 لوحة تحليل حالات عدم المطابقة (NCR)", 
                           style={'color': '#2c3e50', 'marginBottom': '20px'}),
                    html.P("تحليل شامل لحالات عدم المطابقة عبر الإدارات والموظفين", 
                          style={'color': '#7f8c8d'})
                ]),
                html.Div(className='col-md-6 text-end', children=[
                    html.Div(className='card', style={'display': 'inline-block', 'margin': '5px'}, children=[
                        html.Span("🔄 آخر تحديث: ", style={'fontWeight': 'bold'}),
                        html.Span(datetime.now().strftime("%Y-%m-%d %H:%M"))
                    ])
                ])
            ])
        ])
    ]),
    
    # الفلاتر
    html.Div(className='container-fluid mt-4', children=[
        html.Div(className='card', children=[
            html.Div(className='row', children=[
                html.Div(className='col-md-6', children=[
                    html.Label("📅 اختر الشهر:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                    dcc.Dropdown(
                        id='month-filter',
                        options=[{'label': 'جميع الأشهر', 'value': 'all'}] + 
                               [{'label': f"{m} 2024", 'value': m} for m in ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']],
                        value='all',
                        className='dropdown'
                    )
                ]),
                html.Div(className='col-md-6', children=[
                    html.Label("🏢 اختر الإدارة:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                    dcc.Dropdown(
                        id='department-filter',
                        options=[{'label': 'جميع الإدارات', 'value': 'all'}] + 
                               [{'label': dept, 'value': dept} for dept in ncr['الإدارة المتواجد بها الحالة'].unique()],
                        value='all',
                        className='dropdown'
                    )
                ])
            ])
        ])
    ]),
    
    # بطاقات الإحصائيات
    html.Div(className='container-fluid mt-4', children=[
        html.Div(className='row', children=[
            html.Div(className='col-md-3', children=[
                html.Div(className='metric-card', style={'background': 'linear-gradient(45deg, #FF6B6B, #EE5A24)'}, children=[
                    html.H3(id='total-cases', children="0", style={'fontSize': '2.5em', 'margin': '0'}),
                    html.P("إجمالي الحالات", style={'margin': '0', 'fontSize': '1.2em'})
                ])
            ]),
            html.Div(className='col-md-3', children=[
                html.Div(className='metric-card', style={'background': 'linear-gradient(45deg, #4ECDC4, #44A08D)'}, children=[
                    html.H3(id='closed-cases', children="0", style={'fontSize': '2.5em', 'margin': '0'}),
                    html.P("الحالات المغلقة", style={'margin': '0', 'fontSize': '1.2em'})
                ])
            ]),
            html.Div(className='col-md-3', children=[
                html.Div(className='metric-card', style={'background': 'linear-gradient(45deg, #45B7D1, #96C93D)'}, children=[
                    html.H3(id='opened-cases', children="0", style={'fontSize': '2.5em', 'margin': '0'}),
                    html.P("الحالات المفتوحة", style={'margin': '0', 'fontSize': '1.2em'})
                ])
            ]),
            html.Div(className='col-md-3', children=[
                html.Div(className='metric-card', style={'background': 'linear-gradient(45deg, #F3904F, #3B4371)'}, children=[
                    html.H3(id='closure-rate', children="0%", style={'fontSize': '2.5em', 'margin': '0'}),
                    html.P("نسبة الإغلاق", style={'margin': '0', 'fontSize': '1.2em'})
                ])
            ])
        ])
    ]),
    
    # الرسوم البيانية
    html.Div(className='container-fluid mt-4', children=[
        html.Div(className='row', children=[
            html.Div(className='col-md-8', children=[
                html.Div(className='card', children=[
                    html.H4("📈 توزيع الحالات حسب الإدارة", style={'color': '#2c3e50'}),
                    dcc.Graph(id='department-chart')
                ])
            ]),
            html.Div(className='col-md-4', children=[
                html.Div(className='card', children=[
                    html.H4("👥 تقييم الموظفين", style={'color': '#2c3e50'}),
                    dcc.Graph(id='employee-chart')
                ])
            ])
        ]),
        
        html.Div(className='row mt-4', children=[
            html.Div(className='col-md-6', children=[
                html.Div(className='card', children=[
                    html.H4("📊 مقارنة بين الأشهر", style={'color': '#2c3e50'}),
                    dcc.Graph(id='monthly-comparison')
                ])
            ]),
            html.Div(className='col-md-6', children=[
                html.Div(className='card', children=[
                    html.H4("🎯 مؤشر الأداء", style={'color': '#2c3e50'}),
                    dcc.Graph(id='kpi-gauge')
                ])
            ])
        ])
    ]),
    
    # البيانات التفصيلية
    html.Div(className='container-fluid mt-4', children=[
        html.Div(className='card', children=[
            html.H4("📋 البيانات التفصيلية", style={'color': '#2c3e50'}),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in ncr.columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'right',
                    'padding': '10px',
                    'fontFamily': 'Tajawal'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ])
    ])
])

# Callbacks للتفاعل
@app.callback(
    [Output('total-cases', 'children'),
     Output('closed-cases', 'children'),
     Output('opened-cases', 'children'),
     Output('closure-rate', 'children'),
     Output('department-chart', 'figure'),
     Output('employee-chart', 'figure'),
     Output('monthly-comparison', 'figure'),
     Output('kpi-gauge', 'figure'),
     Output('data-table', 'data')],
    [Input('month-filter', 'value'),
     Input('department-filter', 'value')]
)
def update_dashboard(selected_month, selected_department):
    # تصفية البيانات
    filtered_data = ncr.copy()
    
    if selected_month != 'all':
        month_mapping = {'يناير': 1, 'فبراير': 2, 'مارس': 3, 'أبريل': 4, 'مايو': 5, 'يونيو': 6,
                        'يوليو': 7, 'أغسطس': 8, 'سبتمبر': 9, 'أكتوبر': 10, 'نوفمبر': 11, 'ديسمبر': 12}
        month_num = month_mapping.get(selected_month, 1)
        filtered_data = filtered_data[filtered_data['شهر'].dt.month == month_num]
    
    if selected_department != 'all':
        filtered_data = filtered_data[filtered_data['الإدارة المتواجد بها الحالة'] == selected_department]
    
    # الإحصائيات
    total_cases = len(filtered_data)
    closed_cases = len(filtered_data[filtered_data['المتابعة\nFollow Up'] == 'Closed'])
    opened_cases = len(filtered_data[filtered_data['المتابعة\nFollow Up'] == 'Opened'])
    closure_rate = (closed_cases / total_cases * 100) if total_cases > 0 else 0
    
    # رسم الإدارات
    dept_data = filtered_data.groupby(['الإدارة المتواجد بها الحالة', 'المتابعة\nFollow Up']).size().unstack(fill_value=0)
    fig_department = px.bar(
        dept_data.reset_index(), 
        x='الإدارة المتواجد بها الحالة',
        y=['Closed', 'Opened'] if 'Closed' in dept_data.columns and 'Opened' in dept_data.columns else dept_data.columns,
        barmode='group',
        title="توزيع الحالات حسب الإدارة"
    )
    
    # رسم الموظفين
    emp_data = filtered_data.groupby('إسم الشخص القائم بالتبليغ').size().sort_values(ascending=False).head(10)
    fig_employee = px.pie(
        names=emp_data.index,
        values=emp_data.values,
        title="أفضل 10 موظفين بالإبلاغ"
    )
    
    # المقارنة الشهرية
    monthly_data = ncr.groupby(ncr['شهر'].dt.month).size()
    fig_monthly = px.line(
        x=list(monthly_data.index),
        y=monthly_data.values,
        title="توزيع الحالات على الأشهر",
        labels={'x': 'الشهر', 'y': 'عدد الحالات'}
    )
    
    # مقياس الأداء
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = closure_rate,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "نسبة إغلاق الحالات"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}
    ))
    
    return (
        total_cases,
        closed_cases,
        opened_cases,
        f"{closure_rate:.1f}%",
        fig_department,
        fig_employee,
        fig_monthly,
        fig_gauge,
        filtered_data.to_dict('records')
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8053)