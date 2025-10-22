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

# إنشاء قائمة الأشهر ديناميكياً
available_months = ncr['شهر'].dt.month.dropna().unique()
month_names = {
    1: 'يناير', 2: 'فبراير', 3: 'مارس', 4: 'أبريل', 
    5: 'مايو', 6: 'يونيو', 7: 'يوليو', 8: 'أغسطس',
    9: 'سبتمبر', 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر'
}

# إعداد قائمة الأشهر المتاحة
month_list = ['جميع الأشهر']
for month_num in sorted(available_months):
    month_name = month_names.get(month_num, f'شهر {month_num}')
    month_list.append(f"{month_name} {ncr['شهر'].dt.year.iloc[0]}")

# فلتر الشهر
selected_month_filter = st.sidebar.selectbox('اختر الشهر:', month_list)

# فلتر الإدارة
all_departments = ['جميع الإدارات'] + sorted(ncr['الإدارة المتواجد بها الحالة'].dropna().unique().tolist())
selected_department = st.sidebar.selectbox('اختر الإدارة:', all_departments)

# تطبيق الفلتر على البيانات
filtered_data = ncr.copy()

# فلتر الشهر
if selected_month_filter != 'جميع الأشهر':
    selected_month_name = selected_month_filter.split()[0]
    month_number = [key for key, value in month_names.items() if value == selected_month_name][0]
    filtered_data = filtered_data[filtered_data['شهر'].dt.month == month_number]

# فلتر الإدارة
if selected_department != 'جميع الإدارات':
    filtered_data = filtered_data[filtered_data['الإدارة المتواجد بها الحالة'] == selected_department]

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

# معلومات التصفية الحالية
st.info(f"📋 **البيانات المعروضة:** {selected_month_filter} - {selected_department}")

st.markdown("---")

# قسم تحليل الإدارات
st.header("🏢 تحليل الحالات حسب الإدارة")

if not filtered_data.empty:
    # تجميع بيانات الإدارات
    ncr_department = filtered_data.groupby(['الإدارة المتواجد بها الحالة', 'المتابعة\nFollow Up'])\
        ['المتابعة\nFollow Up'].count()\
        .unstack().fillna(0).astype(int)\
        .reset_index()

    if not ncr_department.empty:
        ncr_department['المجموع'] = ncr_department.sum(axis=1, numeric_only=True)
        ncr_department = ncr_department.sort_values('المجموع', ascending=False).reset_index(drop=True)

        # عرض البيانات والرسم البياني جنباً إلى جنب
        col1, col2 = st.columns([2, 1])

        with col1:
            # إصلاح المشكلة: التأكد من وجود الأعمدة المطلوبة
            available_columns = ncr_department.columns.tolist()
            y_columns = []
            
            if 'Closed' in available_columns:
                y_columns.append('Closed')
            if 'Opened' in available_columns:
                y_columns.append('Opened')
            
            if y_columns:
                fig_department = px.bar(
                    data_frame=ncr_department,
                    x='الإدارة المتواجد بها الحالة',
                    y=y_columns,
                    barmode='group',
                    text_auto=True,
                    title=f'توزيع الحالات حسب الإدارة - {selected_month_filter}',
                    labels={'value': 'عدد الحالات', 'الإدارة المتواجد بها الحالة': 'الإدارة'}
                )
                fig_department.update_layout(height=500)
                st.plotly_chart(fig_department, use_container_width=True)
            else:
                st.warning("لا توجد بيانات عن الحالات المغلقة أو المفتوحة للعرض")
        with col2:
            st.subheader("بيانات الإدارات")
            st.dataframe(ncr_department, use_container_width=True)
    else:
        st.warning("لا توجد بيانات متاحة للعرض في هذا القسم")
else:
    st.warning("لا توجد بيانات بعد التصفية")

st.markdown("---")

# قسم تحليل الموظفين
st.header("👥 تقييم الموظفين")

if not filtered_data.empty:
    # تجميع بيانات الموظفين
    ncr_hse = filtered_data.groupby(['إسم الشخص القائم بالتبليغ', 'المتابعة\nFollow Up'])['المتابعة\nFollow Up']\
        .count().unstack().fillna(0).astype(int).reset_index()

    if not ncr_hse.empty:
        # إصلاح المشكلة: التأكد من وجود الأعمدة المطلوبة
        available_columns = ncr_hse.columns.tolist()
        if 'Closed' not in available_columns:
            ncr_hse['Closed'] = 0
        if 'Opened' not in available_columns:
            ncr_hse['Opened'] = 0
            
        ncr_hse['المجموع'] = ncr_hse[['Closed', 'Opened']].sum(axis=1)
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
                title=f'تقييم الموظفين - {selected_month_filter}',
                labels={'value': 'عدد الحالات', 'إسم الشخص القائم بالتبليغ': 'اسم الموظف'}
            )
            fig_hse.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_hse, use_container_width=True)

        with col2:
            st.subheader("بيانات الموظفين")
            st.dataframe(ncr_hse, use_container_width=True)
    else:
        st.warning("لا توجد بيانات متاحة للعرض في هذا القسم")
else:
    st.warning("لا توجد بيانات بعد التصفية")

st.markdown("---")

# قسم المقارنة بين الأشهر
st.header("📅 مقارنة بين الأشهر")

# إنشاء بيانات للمقارنة لجميع الأشهر المتاحة
monthly_data = []
for month_num in sorted(available_months):
    month_data = ncr[ncr['شهر'].dt.month == month_num]
    month_name = month_names.get(month_num, f'شهر {month_num}')
    
    monthly_data.append({
        'الشهر': month_name,
        'إجمالي الحالات': len(month_data),
        'مغلقة': len(month_data[month_data['المتابعة\nFollow Up'] == 'Closed']),
        'مفتوحة': len(month_data[month_data['المتابعة\nFollow Up'] == 'Opened'])
    })

monthly_comparison = pd.DataFrame(monthly_data)

if not monthly_comparison.empty:
    # رسم بياني للمقارنة
    fig_comparison = px.bar(
        monthly_comparison,
        x='الشهر',
        y=['مغلقة', 'مفتوحة'],
        barmode='group',
        text_auto=True,
        title='مقارنة الحالات بين جميع الأشهر',
        labels={'value': 'عدد الحالات', 'variable': 'حالة التقرير'}
    )

    st.plotly_chart(fig_comparison, use_container_width=True)

    # عرض بيانات المقارنة
    st.subheader("بيانات المقارنة الشهرية")
    st.dataframe(monthly_comparison, use_container_width=True)
else:
    st.warning("لا توجد بيانات للمقارنة بين الأشهر")

# قسم البيانات الخام
st.markdown("---")
st.header("📋 البيانات الخام")

with st.expander("عرض البيانات الخام"):
    if not filtered_data.empty:
        st.dataframe(filtered_data, use_container_width=True)
    else:
        st.warning("لا توجد بيانات للعرض")

# معلومات إضافية في الشريط الجانبي
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ معلومات")
st.sidebar.info(
    """
    **NCR Dashboard**
    
    هذه اللوحة تعرض تحليلات حالات عدم المطابقة (NCR)
    
    **الميزات:**
    - تصفية البيانات حسب الشهر والإدارة
    - إحصائيات عامة
    - تحليل حسب الإدارة
    - تقييم الموظفين
    - مقارنة بين الأشهر
    """
)

# زر لمسح الفلتر
if st.sidebar.button("🔄 مسح الفلتر"):
    st.rerun()

# إحصائيات سريعة في الشريط الجانبي
st.sidebar.markdown("---")
st.sidebar.header("📊 إحصائيات سريعة")
st.sidebar.metric("إجمالي الحالات في النظام", len(ncr))
st.sidebar.metric("عدد الإدارات", len(ncr['الإدارة المتواجد بها الحالة'].unique()))
st.sidebar.metric("عدد الموظفين", len(ncr['إسم الشخص القائم بالتبليغ'].unique()))