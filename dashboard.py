import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px

# Load Data
file_path = "/media/hesham/Y/my ubntu inv/personal/data/NCR_8_25h.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    # Create dummy data for demonstration if file is missing
    df = pd.DataFrame({
        'تاريخ الرصد\nRecord Date': ['Jul 7, 2025', 'Aug 1, 2025'],
        'الإدارة المتواجد بها الحالة': ['Admin', 'IT'],
        'إسم الشخص القائم بالتبليغ': ['User A', 'User B'],
        'المتابعة\nFollow Up': ['Closed', 'Open']
    })

# Data Preprocessing
# Rename columns for easier access
df = df.rename(columns={
    'كود الشخص القائم بالتبليغ': "code",
    'الإدارة المتواجد بها الحالة': "department",
    'تاريخ الرصد\nRecord Date': "month",
    'م': "n",
    'إسم الشخص القائم بالتبليغ': "name",
    'وصف حالة عدم التطابق\nDescription of non conformance': "description",
    'المتابعة\nFollow Up': "followUp"
})

# Standardize followUp values
df['followUp'] = df['followUp'].replace('Opened', 'Open')

# Convert month to datetime and extract month number
df['month'] = pd.to_datetime(df['month'], errors='coerce')
df['month_num'] = df['month'].dt.month.astype('Int64')

# Initialize Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("N.C.R-25/26", style={"textAlign": "center", "color": "#579B20"}),
    
    html.Div([
        html.Label("Select Month:"),
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "الإجمالي", "value": "all"},
                {"label": "يوليو 25", "value": 7},
                {"label": "أغسطس 25", "value": 8},
                {"label": "سبتمبر 25", "value": 9},
                {"label": "أكتوبر 25", "value": 10},
                {"label": "نوفمبر 25", "value": 11},
                {"label": "ديسمبر 25", "value": 12},
                {"label": "يناير 26", "value": 1},
                {"label": "فبراير 26", "value": 2},
                {"label": "مارس 26", "value": 3},
                {"label": "أبريل 26", "value": 4},
                {"label": "مايو 26", "value": 5},
                {"label": "يونيو 26", "value": 6}
            ],
            value=7,  # Default value
            clearable=False
        ),
    ], style={'width': '50%', 'margin': 'auto', 'padding': '20px'}),

    html.Div([
        html.Div([
            html.H3("Status by Department", style={"textAlign": "center"}),
            dcc.Graph(id="dept-graph")
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.H3("Status by Reporter", style={"textAlign": "center"}),
            dcc.Graph(id="person-graph")
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ]),

    html.Div([
        html.H3("Detailed Data", style={"textAlign": "center"}),
        dash_table.DataTable(
            id="data-table",
            columns=[{"name": i, "id": i} for i in ['department', 'name', 'description', 'followUp']],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            page_size=10
        )
    ], style={'padding': '20px'})
],style={'backgroundColor': '#FAFDFDE5'})

@app.callback(
    [Output("dept-graph", "figure"),
     Output("person-graph", "figure"),
     Output("data-table", "data")],
    [Input("dropdown", "value")]
)
def update_dashboard(selected_month):
    # Filter by month
    if selected_month and selected_month != 'all':
        filtered_df = df[df['month_num'] == int(selected_month)]
    else:
        filtered_df = df.copy()

    # Define color map
    color_map = {'Open': '#A71313', 'Closed': '#2D0D77'}

    # Prepare Department Data
    df_dept = filtered_df.groupby(['department', 'followUp']).size().reset_index(name='count')
    fig_dept = px.bar(df_dept, x='department', y='count', color='followUp', 
                      title="Follow Up Status by Department", barmode='group',
                      text_auto=True, color_discrete_map=color_map)

    # Prepare Person Data
    df_person = filtered_df.groupby(['name', 'followUp']).size().reset_index(name='count')
    fig_person = px.bar(df_person, x='name', y='count', color='followUp', 
                        title="Follow Up Status by Person", barmode='group',
                        text_auto=True, color_discrete_map=color_map)

    # Prepare Table Data
    table_data = filtered_df[filtered_df['followUp'] == 'Open'][['department', 'name', 'description', 'followUp']].to_dict('records')

    return fig_dept, fig_person, table_data

if __name__ == "__main__":
    app.run(debug=True, port=8070)
