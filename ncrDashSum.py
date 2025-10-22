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

# تخطيط جديد مع Dark Mode
app.layout = html.Div([
    html.H1("📊 لوحة تحليل حالات عدم المطابقة (NCR)", 
            style={'textAlign': 'center', 'color': 'white', 'marginBottom': '20px', 'padding': '10px'}),
    
    html.Div([
        # المحتوى الرئيسي (80%)
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
            
            # الرسم البياني للإدارات (كامل العرض)
            html.Div([
                html.Div([
                    dcc.Graph(id='department-chart')
                ], style={'width': '100%', 'padding': '10px'})
            ]),
            
            # صف الرسوم البيانية للموظفين والمقارنة الشهرية
            html.Div([
                html.Div([
                    dcc.Graph(id='employee-chart')
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
                html.Div([
                    dcc.Graph(id='monthly-comparison')
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'float': 'right'})
            ]),
            
            # البيانات التفصيلية
            html.Div([
                html.H3("📋 البيانات التفصيلية", style={'textAlign': 'center', 'marginBottom': '15px', 'color': 'white'}),
                dash_table.DataTable(
                    id='data-table',
                    page_size=8,
                    style_table={'overflowX': 'auto', 'border': '1px solid #444', 'fontSize': '12px', 'backgroundColor': '#1e1e1e'},
                    style_cell={
                        'textAlign': 'right',
                        'padding': '8px',
                        'fontFamily': 'Arial',
                        'minWidth': '100px',
                        'backgroundColor': '#2d2d2d',
                        'color': 'white',
                        'border': '1px solid #444'
                    },
                    style_header={
                        'backgroundColor': '#1a1a1a',
                        'fontWeight': 'bold',
                        'border': '1px solid #444',
                        'color': 'white'
                    },
                    style_data={
                        'border': '1px solid #444'
                    }
                )
            ], style={'marginTop': '20px', 'padding': '15px'})
        ], style={'width': '77%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # الشريط الجانبي (23%)
        html.Div([
            html.Div([
                html.H3("🔍 عوامل التصفية", style={'textAlign': 'center', 'color': 'white', 'marginBottom': '20px'}),
                
                html.Hr(style={'borderColor': '#555'}),
                
                html.Label("📅 اختر الشهر:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block', 'color': 'white'}),
                dcc.Dropdown(
                    id='month-filter',
                    options=[{'label': 'جميع الأشهر', 'value': 'all'}] + 
                           [{'label': month, 'value': month} for month in ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 
                                                                          'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']],
                    value='all',
                    style={'marginBottom': '25px', 'width': '100%'}
                ),
                
                html.Label("🏢 اختر الإدارة:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block', 'color': 'white'}),
                dcc.Dropdown(
                    id='department-filter',
                    options=[{'label': 'جميع الإدارات', 'value': 'all'}] + 
                           [{'label': dept, 'value': dept} for dept in ncr['الإدارة المتواجد بها الحالة'].unique()],
                    value='all',
                    style={'marginBottom': '25px', 'width': '100%'}
                ),
                
                html.Hr(style={'borderColor': '#555'}),
                
                # معلومات سريعة
                html.Div([
                    html.H4("📈 معلومات سريعة", style={'textAlign': 'center', 'color': 'white'}),
                    html.P(f"إجمالي الحالات: {len(ncr):,}", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#4ECDC4'}),
                    html.P(f"عدد الإدارات: {ncr['الإدارة المتواجد بها الحالة'].nunique()}", style={'textAlign': 'center', 'color': 'white'}),
                    html.P(f"عدد الموظفين: {ncr['إسم الشخص القائم بالتبليغ'].nunique()}", style={'textAlign': 'center', 'color': 'white'})
                ], style={'marginTop': '20px'})
                
            ], className='sidebar-card')
        ], style={'width': '21%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px', 'float': 'right'})
    ])
], style={'backgroundColor': '#121212', 'minHeight': '100vh', 'padding': '15px'})

# CSS مع Dark Mode
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
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
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
                background: #1e1e1e;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                border: 1px solid #333;
            }
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background: #121212;
                color: white;
            }
            h1, h2, h3, h4 {
                color: white;
            }
            .dropdown {
                margin-bottom: 20px;
            }
            .Select-control {
                background-color: #2d2d2d !important;
                color: white !important;
            }
            .Select-menu-outer {
                background-color: #2d2d2d !important;
                color: white !important;
            }
            .Select-value-label {
                color: white !important;
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
        
        # 1. رسم الإدارات (مجمعة بشكل صحيح)
        if not filtered_data.empty and 'الإدارة المتواجد بها الحالة' in filtered_data.columns:
            # تجميع البيانات بشكل صحيح
            dept_summary = filtered_data.groupby('الإدارة المتواجد بها الحالة').agg({
                'المتابعة\nFollow Up': [
                    ('مغلقة', lambda x: (x == 'Closed').sum()),
                    ('مفتوحة', lambda x: (x == 'Opened').sum()),
                    ('المجموع', 'count')
                ]
            }).round(0).astype(int)
            
            # تسطيح الأعمدة المتعددة
            dept_summary.columns = ['مغلقة', 'مفتوحة', 'المجموع']
            dept_summary = dept_summary.reset_index()
            dept_summary = dept_summary.sort_values('المجموع', ascending=False)
            
            # إعادة تشكيل البيانات للرسم البياني
            dept_melted = pd.melt(
                dept_summary, 
                id_vars=['الإدارة المتواجد بها الحالة'],
                value_vars=['مغلقة', 'مفتوحة'],
                var_name='الحالة',
                value_name='عدد الحالات'
            )
            
            fig_department = px.bar(
                dept_melted, 
                x='الإدارة المتواجد بها الحالة', 
                y='عدد الحالات', 
                color='الحالة',
                title="📊 توزيع الحالات حسب الإدارة",
                color_discrete_map={'مغلقة': '#00b894', 'مفتوحة': '#ff7675'},
                barmode='group'
            )
            
            # إضافة القيم داخل الأعمدة
            fig_department.update_traces(
                texttemplate='%{y}', 
                textposition='inside',
                textfont=dict(color='white', size=12)
            )
            
            fig_department.update_layout(
                height=500,
                xaxis_tickangle=-45,
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font_color='white',
                legend_title_text='حالة التقرير',
                xaxis_title="الإدارة",
                yaxis_title="عدد الحالات",
                showlegend=True
            )
        else:
            fig_department = px.bar(title="لا توجد بيانات")
            fig_department.update_layout(plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e', font_color='white')
        
        # 2. رسم الموظفين (مجمعة بشكل صحيح)
        if not filtered_data.empty and 'إسم الشخص القائم بالتبليغ' in filtered_data.columns:
            # تجميع بيانات الموظفين
            emp_summary = filtered_data.groupby('إسم الشخص القائم بالتبليغ').agg({
                'المتابعة\nFollow Up': [
                    ('مغلقة', lambda x: (x == 'Closed').sum()),
                    ('مفتوحة', lambda x: (x == 'Opened').sum()),
                    ('المجموع', 'count')
                ]
            }).round(0).astype(int)
            
            emp_summary.columns = ['مغلقة', 'مفتوحة', 'المجموع']
            emp_summary = emp_summary.reset_index()
            emp_summary = emp_summary.sort_values('المجموع', ascending=False).head(10)
            
            # إعادة تشكيل البيانات
            emp_melted = pd.melt(
                emp_summary,
                id_vars=['إسم الشخص القائم بالتبليغ'],
                value_vars=['مغلقة', 'مفتوحة'],
                var_name='الحالة',
                value_name='عدد البلاغات'
            )
            
            fig_employee = px.bar(
                emp_melted,
                x='إسم الشخص القائم بالتبليغ',
                y='عدد البلاغات',
                color='الحالة',
                title="👥 أداء الموظفين",
                color_discrete_map={'مغلقة': '#00b894', 'مفتوحة': '#ff7675'},
                barmode='group'
            )
            
            fig_employee.update_traces(
                texttemplate='%{y}',
                textposition='inside',
                textfont=dict(color='white', size=10)
            )
            
            fig_employee.update_layout(
                height=400,
                xaxis_tickangle=-45,
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font_color='white',
                legend_title_text='حالة التقرير',
                xaxis_title="الموظف",
                yaxis_title="عدد البلاغات"
            )
        else:
            fig_employee = px.bar(title="لا توجد بيانات")
            fig_employee.update_layout(plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e', font_color='white')
        
        # 3. المقارنة الشهرية (مجمعة بشكل صحيح)
        if not ncr.empty and 'شهر' in ncr.columns:
            # تجميع البيانات الشهرية
            monthly_summary = ncr.groupby(ncr['شهر'].dt.month).agg({
                'المتابعة\nFollow Up': [
                    ('مغلقة', lambda x: (x == 'Closed').sum()),
                    ('مفتوحة', lambda x: (x == 'Opened').sum()),
                    ('المجموع', 'count')
                ]
            }).round(0).astype(int)
            
            monthly_summary.columns = ['مغلقة', 'مفتوحة', 'المجموع']
            monthly_summary = monthly_summary.reset_index()
            monthly_summary['شهر'] = monthly_summary['شهر'].map({
                1: 'يناير', 2: 'فبراير', 3: 'مارس', 4: 'أبريل', 5: 'مايو', 6: 'يونيو',
                7: 'يوليو', 8: 'أغسطس', 9: 'سبتمبر', 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر'
            })
            
            # إعادة تشكيل البيانات
            monthly_melted = pd.melt(
                monthly_summary,
                id_vars=['شهر'],
                value_vars=['مغلقة', 'مفتوحة'],
                var_name='الحالة',
                value_name='عدد الحالات'
            )
            
            fig_monthly = px.bar(
                monthly_melted,
                x='شهر',
                y='عدد الحالات',
                color='الحالة',
                title="📈 المقارنة الشهرية للحالات",
                color_discrete_map={'مغلقة': '#00b894', 'مفتوحة': '#ff7675'},
                barmode='group'
            )
            
            fig_monthly.update_traces(
                texttemplate='%{y}',
                textposition='inside',
                textfont=dict(color='white', size=10)
            )
            
            fig_monthly.update_layout(
                height=400,
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font_color='white',
                legend_title_text='حالة التقرير',
                xaxis_title="الشهر",
                yaxis_title="عدد الحالات"
            )
        else:
            fig_monthly = px.bar(title="لا توجد بيانات")
            fig_monthly.update_layout(plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e', font_color='white')
        
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
    print("📊 افتح المتصفح على: http://localhost:8055")
    app.run(debug=True, host='0.0.0.0', port=8055)