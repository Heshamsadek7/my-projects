import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="NCR Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحميل البيانات
@st.cache_data
def load_data():
    ncr = pd.read_excel('/media/hesham/Y/my ubntu inv/projects/data/NCR_8_25.xlsx')
    
    # تحويل العمود إلى datetime
    ncr['شهر'] = pd.to_datetime(ncr['شهر'], errors='coerce')
    
    return ncr

ncr = load_data()

# العنوان الرئيسي
st.title('📊 لوحة تحليل حالات عدم المطابقة (NCR)')
st.markdown("---")

# الشريط الجانبي للتصفية
st.sidebar.header("🔍 خيارات التصفية")

# اختيار الشهر
months = ['جميع الأشهر', 'يوليو', 'أغسطس', 'سبتمبر']
selected_month = st.sidebar.selectbox('اختر الشهر:', months)

# تصفية البيانات حسب الشهر المختار
if selected_month == 'يوليو':
    filtered_data = ncr[ncr['شهر'].dt.month == 7]
elif selected_month == 'أغسطس':
    filtered_data = ncr[ncr['شهر'].dt.month == 8]
elif selected_month == 'سبتمبر':
    filtered_data = ncr[ncr['شهر'].dt.month == 9]
else:
    filtered_data = ncr

# قسم الإحصائيات العامة
st.header("📈 الإحصائيات العامة")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_cases = len(filtered_data)
    st.metric("إجمالي الحالات", total_cases)

with col2:
    closed_cases = len(filtered_data[filtered_data['المتابعة\nFollow Up'] == 'Closed'])
    st.metric("الحالات المغلقة", closed_cases)

with col3:
    opened_cases = len(filtered_data[filtered_data['المتابعة\nFollow Up'] == 'Opened'])
    st.metric("الحالات المفتوحة", opened_cases)

with col4:
    if total_cases > 0:
        closure_rate = (closed_cases / total_cases) * 100
        st.metric("نسبة الإغلاق", f"{closure_rate:.1f}%")
    else:
        st.metric("نسبة الإغلاق", "0%")

st.markdown("---")

# قسم تحليل الإدارات
st.header("🏢 تحليل الحالات حسب الإدارة")

# تجميع بيانات الإدارات
ncr_department = filtered_data.groupby(['الإدارة المتواجد بها الحالة', 'المتابعة\nFollow Up'])\
    ['المتابعة\nFollow Up'].count()\
    .unstack().fillna(0).astype(int)\
    .reset_index()

ncr_department['المجموع'] = ncr_department.sum(axis=1, numeric_only=True)
ncr_department = ncr_department.sort_values('المجموع', ascending=False).reset_index(drop=True)

# عرض البيانات والرسم البياني جنباً إلى جنب
col1, col2 = st.columns([2, 1])

with col1:
    fig_department = px.bar(
        data_frame=ncr_department,
        x='الإدارة المتواجد بها الحالة',
        y=['Closed', 'Opened'],
        barmode='group',
        text_auto=True,
        title=f'توزيع الحالات حسب الإدارة - {selected_month}',
        labels={'value': 'عدد الحالات', 'الإدارة المتواجد بها الحالة': 'الإدارة'}
    )
    fig_department.update_layout(height=500)
    st.plotly_chart(fig_department, use_container_width=True)

with col2:
    st.subheader("بيانات الإدارات")
    st.dataframe(ncr_department, use_container_width=True)

st.markdown("---")

# قسم تحليل الموظفين
st.header("👥 تقييم الموظفين")

# تجميع بيانات الموظفين
ncr_hse = filtered_data.groupby(['إسم الشخص القائم بالتبليغ', 'المتابعة\nFollow Up'])['المتابعة\nFollow Up']\
    .count().unstack().fillna(0).astype(int).reset_index()

ncr_hse['المجموع'] = ncr_hse.sum(axis=1, numeric_only=True)
ncr_hse['الترتيب'] = ncr_hse['المجموع'].rank(ascending=False, method='dense').astype(int)
ncr_hse = ncr_hse.sort_values('المجموع', ascending=False).reset_index(drop=True)

# عرض البيانات والرسم البياني جنباً إلى جنب
col1, col2 = st.columns([2, 1])

with col1:
    fig_hse = px.bar(
        data_frame=ncr_hse,
        x='إسم الشخص القائم بالتبليغ',
        y=['Closed', 'Opened'],
        barmode='group',
        text_auto=True,
        color='إسم الشخص القائم بالتبليغ',
        title=f'تقييم الموظفين - {selected_month}',
        labels={'value': 'عدد الحالات', 'إسم الشخص القائم بالتبليغ': 'اسم الموظف'}
    )
    fig_hse.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_hse, use_container_width=True)

with col2:
    st.subheader("بيانات الموظفين")
    st.dataframe(ncr_hse, use_container_width=True)

st.markdown("---")

# قسم المقارنة بين الأشهر
st.header("📅 مقارنة بين الأشهر")

# بيانات الأشهر
july_cases = ncr[ncr['شهر'].dt.month == 7]
august_cases = ncr[ncr['شهر'].dt.month == 8]
sept_cases = ncr[ncr['شهر'].dt.month == 9]

# إنشاء بيانات للمقارنة
monthly_comparison = pd.DataFrame({
    'الشهر': ['يوليو', 'أغسطس', 'سبتمبر'],
    'إجمالي الحالات': [len(july_cases), len(august_cases), len(sept_cases)],
    'مغلقة': [
        len(july_cases[july_cases['المتابعة\nFollow Up'] == 'Closed']),
        len(august_cases[august_cases['المتابعة\nFollow Up'] == 'Closed']),
        len(sept_cases[sept_cases['المتابعة\nFollow Up'] == 'Closed'])
    ],
    'مفتوحة': [
        len(july_cases[july_cases['المتابعة\nFollow Up'] == 'Opened']),
        len(august_cases[august_cases['المتابعة\nFollow Up'] == 'Opened']),
        len(sept_cases[sept_cases['المتابعة\nFollow Up'] == 'Opened'])
    ]
})

# رسم بياني للمقارنة
fig_comparison = px.bar(
    monthly_comparison,
    x='الشهر',
    y=['مغلقة', 'مفتوحة'],
    barmode='group',
    text_auto=True,
    title='مقارنة الحالات بين الأشهر',
    labels={'value': 'عدد الحالات', 'variable': 'حالة التقرير'}
)

st.plotly_chart(fig_comparison, use_container_width=True)

# عرض بيانات المقارنة
st.subheader("بيانات المقارنة الشهرية")
st.dataframe(monthly_comparison, use_container_width=True)

# قسم البيانات الخام
st.markdown("---")
st.header("📋 البيانات الخام")

with st.expander("عرض البيانات الخام"):
    st.dataframe(filtered_data, use_container_width=True)

# معلومات إضافية في الشريط الجانبي
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ معلومات")
st.sidebar.info(
    """
    **NCR Dashboard**
    
    هذه اللوحة تعرض تحليلات حالات عدم المطابقة (NCR)
    across different departments and employees.
    
    **الميزات:**
    - تصفية البيانات حسب الشهر
    - إحصائيات عامة
    - تحليل حسب الإدارة
    - تقييم الموظفين
    - مقارنة بين الأشهر
    """
)