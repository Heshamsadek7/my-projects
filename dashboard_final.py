# dashboard_final.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# إعداد صفحة Streamlit
st.set_page_config(
    page_title="لوحة تحكم تصاريح المقاولين",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .month-card {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="main-header">📊 لوحة تحكم تصاريح عمل المقاولين</div>', unsafe_allow_html=True)

# دالة لتحميل وتنظيف البيانات
@st.cache_data
def load_data():
    try:
        # استخدام المسار الكامل للفايل
        df = pd.read_csv('/media/hesham/Y/my ubntu inv/projects/data/work permations.csv', encoding='utf-8')
        
        # تنظيف بيانات ساعات العمل
        def clean_work_hours(value):
            try:
                value = str(value).strip()
                value = value.replace('_(* ', '').replace('_)_', '').replace('_', '')
                value = value.replace(':', '.').replace('٫', '.').replace(',', '.')
                value = value.replace('AM', '').replace('PM', '').strip()
                
                if ' ' in value:
                    parts = value.split()
                    value = parts[0] if parts else '0'
                
                result = float(value) if value else 0.0
                return max(0.0, result)
            except:
                return 0.0
        
        df['إجمالي ساعات العمل'] = df['إجمالي ساعات العمل'].apply(clean_work_hours)
        
        # استخدام عمود "الشهر" مباشرة بدلاً من "التاريخ"
        # تنظيف عمود الشهر وإزالة السنة
        def clean_month_name(month_str):
            if pd.isna(month_str):
                return None
            month_str = str(month_str).strip()
            # إزالة السنة وأي نص إضافي
            if '-' in month_str:
                return month_str.split('-')[0].strip()
            return month_str
        
        df['الشهر_مفصل'] = df['الشهر'].apply(clean_month_name)
        
        # إزالة أي صفوف تحتوي على قيم فارغة في الشهر
        df = df.dropna(subset=['الشهر_مفصل'])
        
        # تصفية فقط الأشهر الموجودة فعلياً في البيانات
        valid_months = ['يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر']  # الأشهر الموجودة في بياناتك
        df = df[df['الشهر_مفصل'].isin(valid_months)]
        
        return df
    except Exception as e:
        st.error(f"❌ خطأ في تحميل البيانات: {e}")
        return None

# تحميل البيانات
df = load_data()

if df is not None:
    # ============================================================================
    # الشريط الجانبي
    # ============================================================================
    with st.sidebar:
        st.markdown("## 🗓️ إعدادات التقرير")
        
        # اختيار الشهر - استخدام الأشهر الفعلية من البيانات فقط
        try:
            # الحصول على الأشهر المتاحة من البيانات بعد التنظيف
            available_months = [month for month in df['الشهر_مفصل'].unique() if pd.notna(month)]
            
            # ترتيب الأشهر حسب السنة المالية
            fiscal_month_order ={1:'يوليو',2:'أغسطس',3:'سبتمبر',4:'أكتوبر'}
            
            # ترتيب الأشهر المتاحة حسب السنة المالية
            available_months_sorted = sorted(
                available_months, 
                key=lambda x: fiscal_month_order.get(x, 99)
            )
            
            st.write(f"📅 الأشهر المتاحة: {', '.join(available_months_sorted)}")
            
            selected_month = st.selectbox(
                "اختر الشهر:",
                options=["الكل"] + available_months_sorted,
                index=0
            )
        except Exception as e:
            st.error(f"خطأ في تحميل قائمة الأشهر: {e}")
            selected_month = "الكل"
        
        st.markdown("---")
        st.markdown("## 📈 الإجماليات")
        
        # الإحصائيات العامة
        total_hours = df['إجمالي ساعات العمل'].sum()
        total_tasks = len(df)
        avg_hours = df['إجمالي ساعات العمل'].mean()
        
        st.metric("🕒 إجمالي الساعات", f"{total_hours:,.1f}")
        st.metric("📋 إجمالي المهام", f"{total_tasks:,}")
        st.metric("📊 متوسط الساعات", f"{avg_hours:.1f}")
        
        st.markdown("---")
        
        # إحصائيات الأشهر
        st.markdown("### 📅 إجماليات الأشهر")
        monthly_summary = df.groupby('الشهر_مفصل').agg({
            'إجمالي ساعات العمل': 'sum',
            'إسم الشركة': 'count'
        }).rename(columns={'إسم الشركة': 'عدد المهام'})
        
        # ترتيب الأشهر حسب السنة المالية
        fiscal_month_order = {
            'يوليو': 1, 'أغسطس': 2, 'سبتمبر': 3
        }
        
        for month in sorted(monthly_summary.index, key=lambda x: fiscal_month_order.get(x, 99)):
            data = monthly_summary.loc[month]
            with st.container():
                st.markdown(f'<div class="month-card">', unsafe_allow_html=True)
                st.write(f"**{month}**")
                st.write(f"الساعات: {data['إجمالي ساعات العمل']:,.1f}")
                st.write(f"المهام: {data['عدد المهام']:,}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================================
    # المنطقة الرئيسية
    # ============================================================================
    
    # تصفية البيانات حسب الشهر المختار
    if selected_month != "الكل":
        filtered_df = df[df['الشهر_مفصل'] == selected_month]
        title_suffix = f" - {selected_month}"
    else:
        filtered_df = df
        title_suffix = " - جميع البيانات"
    
    # عرض معلومات عن البيانات
    st.info(f"📊 عرض بيانات: {len(filtered_df)} مهمة | {filtered_df['إجمالي ساعات العمل'].sum():.1f} ساعة")
    
    # الصف الأول: المخططات الرئيسية
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📍 ساعات العمل حسب الموقع{title_suffix}")
        
        # تجميع بيانات المواقع
        locations_data = filtered_df.groupby('الموقع')['إجمالي ساعات العمل'].sum().sort_values(ascending=False)
        
        if len(locations_data) > 0:
            fig_locations = px.bar(
                x=locations_data.index,
                y=locations_data.values,
                title=f"توزيع الساعات على المواقع{title_suffix}",
                labels={'x': 'الموقع', 'y': 'ساعات العمل'},
                color=locations_data.values,
                color_continuous_scale='viridis',
                text=locations_data.values  # إضافة القيم على الأعمدة
            )
            fig_locations.update_layout(
                xaxis_tickangle=-45,
                height=400,
                showlegend=False
            )
            fig_locations.update_traces(
                texttemplate='%{text:.1f}',  # تنسيق الأرقام
                textposition='inside'  # وضع القيم داخل الأعمدة
            )
            st.plotly_chart(fig_locations, use_container_width=True)
        else:
            st.info("⚠️ لا توجد بيانات للمواقع في الفترة المحددة")
    
    with col2:
        st.markdown(f"### 👷 ساعات العمل لمشرفي السلامة{title_suffix}")
        
        # تجميع بيانات مشرفي السلامة
        safety_data = filtered_df.groupby('مشرف السلامة')['إجمالي ساعات العمل'].sum().nlargest(15)
        
        if len(safety_data) > 0:
            fig_safety = px.bar(
                x=safety_data.index,
                y=safety_data.values,
                title=f"أفضل 15 مشرف سلامة{title_suffix}",
                labels={'x': 'مشرف السلامة', 'y': 'ساعات العمل'},
                color=safety_data.values,
                color_continuous_scale='plasma',
                text=safety_data.values  # إضافة القيم على الأعمدة
            )
            fig_safety.update_layout(
                xaxis_tickangle=-45,
                height=400,
                showlegend=False
            )
            fig_safety.update_traces(
                texttemplate='%{text:.1f}',  # تنسيق الأرقام
                textposition='inside'  # وضع القيم داخل الأعمدة
            )
            st.plotly_chart(fig_safety, use_container_width=True)
        else:
            st.info("⚠️ لا توجد بيانات لمشرفي السلامة في الفترة المحددة")
    
    # الصف الثاني: مخطط الشركات
    st.markdown(f"### 🏢 ساعات العمل حسب الشركة{title_suffix}")
    
    companies_data = filtered_df.groupby('إسم الشركة')['إجمالي ساعات العمل'].sum().nlargest(20)
    
    if len(companies_data) > 0:
        fig_companies = px.bar(
            x=companies_data.index,
            y=companies_data.values,
            title=f"أفضل 20 شركة حسب ساعات العمل{title_suffix}",
            labels={'x': 'الشركة', 'y': 'ساعات العمل'},
            color=companies_data.values,
            color_continuous_scale='reds',
            text=companies_data.values  # إضافة القيم على الأعمدة
        )
        fig_companies.update_layout(
            xaxis_tickangle=-45,
            height=500,
            showlegend=False
        )
        fig_companies.update_traces(
            texttemplate='%{text:.1f}',  # تنسيق الأرقام
            textposition='inside'  # وضع القيم داخل الأعمدة
        )
        st.plotly_chart(fig_companies, use_container_width=True)
    else:
        st.info("⚠️ لا توجد بيانات للشركات في الفترة المحددة")
    
    # ============================================================================
    # قسم المقارنة بين الأشهر
    # ============================================================================
    st.markdown("---")
    st.markdown("## 📊 مقارنة بين الأشهر")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        # مقارنة ساعات العمل الشهرية
        monthly_hours = df.groupby('الشهر_مفصل')['إجمالي ساعات العمل'].sum()
        
        # ترتيب الأشهر حسب السنة المالية
        fiscal_month_order = {
            'يوليو': 1, 'أغسطس': 2, 'سبتمبر': 3
        }
        
        monthly_hours = monthly_hours.reindex(
            sorted(monthly_hours.index, key=lambda x: fiscal_month_order.get(x, 99))
        )
        
        fig_monthly_hours = px.bar(
            x=monthly_hours.index,
            y=monthly_hours.values,
            title="مقارنة ساعات العمل بين الأشهر",
            labels={'x': 'الشهر', 'y': 'ساعات العمل'},
            color=monthly_hours.values,
            color_continuous_scale='blues',
            text=monthly_hours.values  # إضافة القيم على الأعمدة
        )
        fig_monthly_hours.update_layout(height=300)
        fig_monthly_hours.update_traces(
            texttemplate='%{text:.1f}',
            textposition='inside'
        )
        st.plotly_chart(fig_monthly_hours, use_container_width=True)
    
    with col4:
        # مقارنة عدد المهام الشهرية
        monthly_tasks = df.groupby('الشهر_مفصل')['إسم الشركة'].count()
        monthly_tasks = monthly_tasks.reindex(
            sorted(monthly_tasks.index, key=lambda x: fiscal_month_order.get(x, 99))
        )
        
        fig_monthly_tasks = px.bar(
            x=monthly_tasks.index,
            y=monthly_tasks.values,
            title="مقارنة عدد المهام بين الأشهر",
            labels={'x': 'الشهر', 'y': 'عدد المهام'},
            color=monthly_tasks.values,
            color_continuous_scale='greens',
            text=monthly_tasks.values  # إضافة القيم على الأعمدة
        )
        fig_monthly_tasks.update_layout(height=300)
        fig_monthly_tasks.update_traces(
            texttemplate='%{text}',
            textposition='inside'
        )
        st.plotly_chart(fig_monthly_tasks, use_container_width=True)
    
    with col5:
        # متوسط الساعات الشهري
        monthly_avg = df.groupby('الشهر_مفصل')['إجمالي ساعات العمل'].mean()
        monthly_avg = monthly_avg.reindex(
            sorted(monthly_avg.index, key=lambda x: fiscal_month_order.get(x, 99))
        )
        
        fig_monthly_avg = px.bar(
            x=monthly_avg.index,
            y=monthly_avg.values,
            title="متوسط ساعات العمل الشهري",
            labels={'x': 'الشهر', 'y': 'متوسط الساعات'},
            color=monthly_avg.values,
            color_continuous_scale='purples',
            text=monthly_avg.values  # إضافة القيم على الأعمدة
        )
        fig_monthly_avg.update_layout(height=300)
        fig_monthly_avg.update_traces(
            texttemplate='%{text:.1f}',
            textposition='inside'
        )
        st.plotly_chart(fig_monthly_avg, use_container_width=True)
    
    # ============================================================================
    # قسم البيانات التفصيلية
    # ============================================================================
    st.markdown("---")
    st.markdown("## 📋 البيانات التفصيلية")
    
    tab1, tab2, tab3 = st.tabs(["البيانات الخام", "التلخيص حسب الشهر", "أفضل الأداء"])
    
    with tab1:
        # عرض الأعمدة المهمة فقط
        columns_to_show = ['الشهر', 'التاريخ', 'اليوم', 'إسم الشركة', 'المشرف التنفيزى', 
                          'نوع العمل', 'مواقف التصريح', 'الموقع', 'إجمالي ساعات العمل', 
                          'مشرف السلامة']
        
        # تصفية الأعمدة الموجودة فعلياً في البيانات
        available_columns = [col for col in columns_to_show if col in filtered_df.columns]
        
        st.dataframe(filtered_df[available_columns], use_container_width=True)
        
        # زر تحميل البيانات
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 تحميل البيانات كـ CSV",
            data=csv,
            file_name=f"تصاريح_المقاولين_{selected_month}.csv",
            mime="text/csv"
        )
    
    with tab2:
        monthly_detail = df.groupby('الشهر_مفصل').agg({
            'إجمالي ساعات العمل': ['sum', 'mean', 'count', 'max'],
            'إسم الشركة': 'nunique',
            'الموقع': 'nunique',
            'مشرف السلامة': 'nunique'
        }).round(2)
        
        monthly_detail.columns = [
            'إجمالي الساعات', 'متوسط الساعات', 'عدد المهام', 'أعلى ساعات',
            'عدد الشركات', 'عدد المواقع', 'عدد المشرفين'
        ]
        
        # ترتيب الأشهر حسب السنة المالية
        monthly_detail = monthly_detail.reindex(
            sorted(monthly_detail.index, key=lambda x: fiscal_month_order.get(x, 99))
        )
        
        st.dataframe(monthly_detail, use_container_width=True)
    
    with tab3:
        col6, col7, col8 = st.columns(3)
        
        with col6:
            st.markdown("### 🥇 أفضل الشركات")
            top_companies = df.groupby('إسم الشركة')['إجمالي ساعات العمل'].sum().nlargest(5)
            for company, hours in top_companies.items():
                st.write(f"**{company}**: {hours:,.1f} ساعة")
        
        with col7:
            st.markdown("### 🥇 أفضل المواقع")
            top_locations = df.groupby('الموقع')['إجمالي ساعات العمل'].sum().nlargest(5)
            for location, hours in top_locations.items():
                st.write(f"**{location}**: {hours:,.1f} ساعة")
        
        with col8:
            st.markdown("### 🥇 أفضل مشرفي السلامة")
            top_safety = df.groupby('مشرف السلامة')['إجمالي ساعات العمل'].sum().nlargest(5)
            for supervisor, hours in top_safety.items():
                st.write(f"**{supervisor}**: {hours:,.1f} ساعة")

else:
    st.error("❌ تعذر تحميل البيانات. يرجى التأكد من وجود ملف 'work_permations.csv' في المسار المحدد.")

# معلومات إضافية للتصحيح
if df is not None:
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔍 معلومات التصحيح")
        st.write(f"إجمالي الصفوف: {len(df)}")
        st.write(f"الأشهر الموجودة: {df['الشهر_مفصل'].unique()}")