import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# تحميل البيانات
def load_data():
    try:
        ncr = pd.read_excel('/media/hesham/Y/my ubntu inv/projects/data/NCR_8_25.xlsx')
        ncr['شهر'] = pd.to_datetime(ncr['شهر'], errors='coerce')
        print("✅ تم تحميل البيانات بنجاح!")
        return ncr
    except Exception as e:
        print(f"❌ خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

ncr = load_data()

# إنشاء تطبيق Dash
app = dash.Dash(__name__)

# تخطيط جديد مع الفلاتر على اليمين
app.layout = html.Div([
    html.H1("📊 لوحة تحليل حالات عدم المطابقة (NCR)", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
    
    html.Div([
        # المحتوى الرئيسي (70%)
        html.Div([
            # بطاقات الإحصائيات المصغرة
            html.Div([
                html.Div([
                    html.Div(id='total-cases', className='metric-card'),
                ], style={'width': '23%', 'display': 'inline-block', 'padding': '5px'}),
                html.Div([
                    html.Div(id='closed-cases', className='metric-card'),
                ], style={'width': '23%', 'display': 'inline-block', 'padding': '5px'}),
                html.Div([
                    html.Div(id='opened-cases', className='metric-card'),
                ], style={'width': '23%', 'display': 'inline-block', 'padding': '5px'}),
                html.Div([
                    html.Div(id='closure-rate', className='metric-card'),
                ], style={'width': '23%', 'display': 'inline-block', 'padding': '5px'})
            ], style={'marginTop': '10px', 'marginBottom': '20px'}),
            
            # الرسوم البيانية
            html.Div([
                html.Div([
                    dcc.Graph(id='department-chart')
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
                html.Div([
                    dcc.Graph(id='employee-chart')
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'float': 'right'})
            ]),
            
            html.Div([
                html.Div([
                    dcc.Graph(id='monthly-comparison')
                ], style={'width': '100%', 'padding': '10px'})
            ]),
            
            # البيانات التفصيلية
            html.Div([
                html.H3("📋 البيانات التفصيلية", style={'textAlign': 'center', 'marginBottom': '15px'}),
                dash_table.DataTable(
                    id='data-table',
                    page_size=8,
                    style_table={'overflowX': 'auto', 'border': '1px solid #ddd', 'fontSize': '12px'},
                    style_cell={
                        'textAlign': 'right',
                        'padding': '8px',
                        'fontFamily': 'Arial',
                        'minWidth': '100px'
                    },
                    style_header={
                        'backgroundColor': '#f8f9fa',
                        'fontWeight': 'bold',
                        'border': '1px solid #ddd'
                    }
                )
            ], style={'marginTop': '20px', 'padding': '15px'})
        ], style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # الشريط الجانبي (25%)
        html.Div([
            html.Div([
                html.H3("🔍 عوامل التصفية", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
                
                html.Hr(),
                
                html.Label("📅 اختر الشهر:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.Dropdown(
                    id='month-filter',
                    options=[{'label': 'جميع الأشهر', 'value': 'all'}] + 
                           [{'label': month, 'value': month} for month in ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 
                                                                          'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']],
                    value='all',
                    style={'marginBottom': '25px', 'width': '100%'}
                ),
                
                html.Label("🏢 اختر الإدارة:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.Dropdown(
                    id='department-filter',
                    options=[{'label': 'جميع الإدارات', 'value': 'all'}] + 
                           [{'label': dept, 'value': dept} for dept in ncr['الإدارة المتواجد بها الحالة'].unique()],
                    value='all',
                    style={'marginBottom': '25px', 'width': '100%'}
                ),
                
                html.Hr(),
                
                # معلومات سريعة
                html.Div([
                    html.H4("📈 معلومات سريعة", style={'textAlign': 'center', 'color': '#2c3e50'}),
                    html.P(f"إجمالي الحالات: {len(ncr):,}", style={'textAlign': 'center', 'fontWeight': 'bold'}),
                    html.P(f"عدد الإدارات: {ncr['الإدارة المتواجد بها الحالة'].nunique()}", style={'textAlign': 'center'}),
                    html.P(f"عدد الموظفين: {ncr['إسم الشخص القائم بالتبليغ'].nunique()}", style={'textAlign': 'center'})
                ], style={'marginTop': '20px'})
                
            ], className='sidebar-card')
        ], style={'width': '23%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px', 'float': 'right'})
    ])
])

# CSS محسن
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>NCR Dashboard</title>
        <style>
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transition: transform 0.2s ease;
                height: 80px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .metric-card:hover {
                transform: translateY(-2px);
            }
            .sidebar-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;
            }
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 15px;
                background: #f8f9fa;
            }
            h1, h2, h3 {
                color: #2c3e50;
            }
            .dropdown {
                margin-bottom: 20px;
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

# Callback functions
@app.callback(
    [Output('total-cases', 'children'),
     Output('closed-cases', 'children'),
     Output('opened-cases', 'children'),
     Output('closure-rate', 'children'),
     Output('department-chart', 'figure'),
     Output('employee-chart', 'figure'),
     Output('monthly-comparison', 'figure'),
     Output('data-table', 'data')],
    [Input('month-filter', 'value'),
     Input('department-filter', 'value')]
)
def update_dashboard(selected_month, selected_department):
    try:
        # تصفية البيانات
        filtered_data = ncr.copy()
        
        # تطبيق الفلاتر
        if selected_month != 'all':
            month_mapping = {'يناير': 1, 'فبراير': 2, 'مارس': 3, 'أبريل': 4, 'مايو': 5, 'يونيو': 6,
                            'يوليو': 7, 'أغسطس': 8, 'سبتمبر': 9, 'أكتوبر': 10, 'نوفمبر': 11, 'ديسمبر': 12}
            month_num = month_mapping.get(selected_month)
            if month_num:
                filtered_data = filtered_data[filtered_data['شهر'].dt.month == month_num]
        
        if selected_department != 'all':
            filtered_data = filtered_data[filtered_data['الإدارة المتواجد بها الحالة'] == selected_department]
        
        # الإحصائيات
        total_cases = len(filtered_data)
        closed_cases = len(filtered_data[filtered_data['المتابعة\nFollow Up'] == 'Closed']) if 'المتابعة\nFollow Up' in filtered_data.columns else 0
        opened_cases = len(filtered_data[filtered_data['المتابعة\nFollow Up'] == 'Opened']) if 'المتابعة\nFollow Up' in filtered_data.columns else 0
        closure_rate = (closed_cases / total_cases * 100) if total_cases > 0 else 0
        
        # الرسوم البيانية
        
        # 1. رسم الإدارات (عمودي مع القيم)
        if not filtered_data.empty and 'الإدارة المتواجد بها الحالة' in filtered_data.columns:
            dept_data = filtered_data['الإدارة المتواجد بها الحالة'].value_counts().reset_index()
            dept_data.columns = ['الإدارة', 'عدد الحالات']
            fig_department = px.bar(dept_data, x='الإدارة', y='عدد الحالات', 
                                  title="📊 توزيع الحالات حسب الإدارة",
                                  color='عدد الحالات',
                                  color_continuous_scale='viridis',
                                  text='عدد الحالات')
            fig_department.update_traces(texttemplate='%{text}', textposition='inside')
            fig_department.update_layout(
                height=400,
                xaxis_tickangle=-45,
                showlegend=False
            )
        else:
            fig_department = px.bar(title="لا توجد بيانات")
        
        # 2. رسم الموظفين (عمودي بدلاً من دائري مع القيم)
        if not filtered_data.empty and 'إسم الشخص القائم بالتبليغ' in filtered_data.columns:
            emp_data = filtered_data['إسم الشخص القائم بالتبليغ'].value_counts().head(10).reset_index()
            emp_data.columns = ['الموظف', 'عدد البلاغات']
            fig_employee = px.bar(emp_data, x='الموظف', y='عدد البلاغات',
                                title="👥 أعلى 10 موظفين في عدد البلاغات",
                                color='عدد البلاغات',
                                color_continuous_scale='plasma',
                                text='عدد البلاغات')
            fig_employee.update_traces(texttemplate='%{text}', textposition='outside')
            fig_employee.update_layout(
                height=400,
                xaxis_tickangle=-45,
                showlegend=False
            )
        else:
            fig_employee = px.bar(title="لا توجد بيانات")
        
        # 3. المقارنة الشهرية (عمودي بدلاً من خطي مع القيم)
        if not ncr.empty and 'شهر' in ncr.columns:
            monthly_data = ncr.groupby(ncr['شهر'].dt.month).size().reset_index()
            monthly_data.columns = ['شهر', 'عدد الحالات']
            monthly_data['اسم_الشهر'] = monthly_data['شهر'].map({
                1: 'يناير', 2: 'فبراير', 3: 'مارس', 4: 'أبريل', 5: 'مايو', 6: 'يونيو',
                7: 'يوليو', 8: 'أغسطس', 9: 'سبتمبر', 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر'
            })
            fig_monthly = px.bar(monthly_data, x='اسم_الشهر', y='عدد الحالات', 
                               title="📈 المقارنة الشهرية للحالات",
                               color='عدد الحالات',
                               color_continuous_scale='tealrose',
                               text='عدد الحالات')
            fig_monthly.update_traces(texttemplate='%{text}', textposition='inside')
            fig_monthly.update_layout(
                height=400,
                xaxis_tickangle=0,
                showlegend=False
            )
        else:
            fig_monthly = px.bar(title="لا توجد بيانات")
        
        return (
            [html.H4(f"{total_cases:,}", style={'margin': '0', 'fontSize': '1.5em', 'fontWeight': 'bold'}), 
             html.P("إجمالي الحالات", style={'margin': '0', 'fontSize': '0.9em'})],
            
            [html.H4(f"{closed_cases:,}", style={'margin': '0', 'fontSize': '1.5em', 'fontWeight': 'bold'}), 
             html.P("مغلقة", style={'margin': '0', 'fontSize': '0.9em'})],
            
            [html.H4(f"{opened_cases:,}", style={'margin': '0', 'fontSize': '1.5em', 'fontWeight': 'bold'}), 
             html.P("مفتوحة", style={'margin': '0', 'fontSize': '0.9em'})],
            
            [html.H4(f"{closure_rate:.1f}%", style={'margin': '0', 'fontSize': '1.5em', 'fontWeight': 'bold'}), 
             html.P("نسبة الإغلاق", style={'margin': '0', 'fontSize': '0.9em'})],
            
            fig_department,
            fig_employee,
            fig_monthly,
            filtered_data.to_dict('records')
        )
    
    except Exception as e:
        print(f"Error: {e}")
        return [], [], [], [], {}, {}, {}, []

if __name__ == '__main__':
    print("🚀 تشغيل الداشبورد...")
    print("📊 افتح المتصفح على: http://localhost:8053")
    app.run(debug=True, host='0.0.0.0', port=8053) 
