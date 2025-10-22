# export_pdf_improved.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime
import numpy as np

# إعداد الخطوط للعربية
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def arabic_text(text):
    """تحويل النص العربي للعرض الصحيح"""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def create_pdf_report():
    try:
        # تحميل البيانات
        df = pd.read_csv('/media/hesham/Y/my ubntu inv/work/NMG/NMG12-09-2025Home/8-25/new/work permations.csv', encoding='utf-8')
        
        print(f"✅ تم تحميل {len(df)} سجل")
        
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
        
        # تنظيف عمود الشهر
        def clean_month_name(month_str):
            if pd.isna(month_str):
                return None
            month_str = str(month_str).strip()
            if '-' in month_str:
                return month_str.split('-')[0].strip()
            return month_str
        
        df['الشهر_مفصل'] = df['الشهر'].apply(clean_month_name)
        df = df.dropna(subset=['الشهر_مفصل'])
        
        # إنشاء ملف PDF
        with PdfPages('تقرير_المقاولين.pdf') as pdf:
            
            # الصفحة 1: الغلاف
            fig, ax = plt.subplots(figsize=(11, 8))
            ax.text(0.5, 0.7, arabic_text('تقرير تصاريح عمل المقاولين'), 
                   ha='center', va='center', fontsize=24, fontweight='bold', color='#1f77b4')
            ax.text(0.5, 0.5, arabic_text(f'تاريخ التصدير: {datetime.now().strftime("%Y-%m-%d")}'), 
                   ha='center', va='center', fontsize=16, color='#666666')
            ax.text(0.5, 0.3, arabic_text(f'إجمالي الساعات: {df["إجمالي ساعات العمل"].sum():.1f}'), 
                   ha='center', va='center', fontsize=14, color='#2ca02c')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # الصفحة 2: الإحصائيات العامة
            fig, ax = plt.subplots(figsize=(11, 8))
            
            stats = [
                f'إجمالي ساعات العمل: {df["إجمالي ساعات العمل"].sum():.1f}',
                f'عدد المهام: {len(df):,}',
                f'متوسط الساعات للمهمة: {df["إجمالي ساعات العمل"].mean():.1f}',
                f'عدد الشركات: {df["إسم الشركة"].nunique()}',
                f'عدد المواقع: {df["الموقع"].nunique()}',
                f'عدد مشرفي السلامة: {df["مشرف السلامة"].nunique()}'
            ]
            
            ax.text(0.1, 0.9, arabic_text('الإحصائيات العامة'), 
                   fontsize=20, fontweight='bold', color='#1f77b4')
            
            for i, stat in enumerate(stats):
                ax.text(0.1, 0.7 - i*0.1, arabic_text(stat), 
                       fontsize=14, va='top')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # الصفحة 3: أفضل المواقع
            fig, ax = plt.subplots(figsize=(11, 8))
            locations_data = df.groupby('الموقع')['إجمالي ساعات العمل'].sum().nlargest(8)
            
            bars = ax.bar(range(len(locations_data)), locations_data.values, color='skyblue')
            ax.set_title(arabic_text('أفضل المواقع حسب ساعات العمل'), fontsize=16, fontweight='bold')
            
            # إضافة القيم على الأعمدة
            for i, (bar, value) in enumerate(zip(bars, locations_data.values)):
                ax.text(i, bar.get_height() + 5, f'{value:.1f}', 
                       ha='center', va='bottom', fontsize=10)
            
            # تحويل أسماء المواقع للعربية
            locations_names = [arabic_text(str(name)) for name in locations_data.index]
            ax.set_xticks(range(len(locations_data)))
            ax.set_xticklabels(locations_names, rotation=45, ha='right')
            ax.set_ylabel(arabic_text('ساعات العمل'))
            
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # الصفحة 4: أفضل الشركات
            fig, ax = plt.subplots(figsize=(11, 8))
            companies_data = df.groupby('إسم الشركة')['إجمالي ساعات العمل'].sum().nlargest(10)
            
            bars = ax.barh(range(len(companies_data)), companies_data.values, color='lightgreen')
            ax.set_title(arabic_text('أفضل 10 شركات حسب ساعات العمل'), fontsize=16, fontweight='bold')
            
            # إضافة القيم على الأعمدة
            for i, (bar, value) in enumerate(zip(bars, companies_data.values)):
                ax.text(bar.get_width() + 5, i, f'{value:.1f}', 
                       va='center', fontsize=10)
            
            # تحويل أسماء الشركات للعربية
            companies_names = [arabic_text(str(name)) for name in companies_data.index]
            ax.set_yticks(range(len(companies_data)))
            ax.set_yticklabels(companies_names)
            ax.set_xlabel(arabic_text('ساعات العمل'))
            
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # الصفحة 5: أفضل مشرفي السلامة
            fig, ax = plt.subplots(figsize=(11, 8))
            safety_data = df.groupby('مشرف السلامة')['إجمالي ساعات العمل'].sum().nlargest(8)
            
            colors = plt.cm.Set3(np.linspace(0, 1, len(safety_data)))
            wedges, texts, autotexts = ax.pie(safety_data.values, labels=None, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
            
            ax.set_title(arabic_text('توزيع ساعات العمل لمشرفي السلامة'), fontsize=16, fontweight='bold')
            
            # إضافة وسيلة إيضاح
            safety_names = [arabic_text(str(name)) for name in safety_data.index]
            ax.legend(wedges, safety_names, title=arabic_text("المشرفين"), 
                     loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
        print("✅ تم إنشاء التقرير بنجاح: تقرير_المقاولين.pdf")
        print(f"📊 إجمالي الساعات: {df['إجمالي ساعات العمل'].sum():.1f}")
        print(f"📋 عدد المهام: {len(df)}")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء التقرير: {e}")

if __name__ == "__main__":
    create_pdf_report()