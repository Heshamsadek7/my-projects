# export_pdf.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import arabic_reshaper
from bidi.algorithm import get_display

def create_pdf_report():
    # تحميل وتنظيف البيانات (نفس الكود السابق)
    df = pd.read_csv('/media/hesham/Y/my ubntu inv/work/NMG/NMG12-09-2025Home/8-25/new/work_permations.csv', encoding='utf-8')
    
    def clean_work_hours(value):
        try:
            value = str(value).strip()
            value = value.replace('_(* ', '').replace('_)_', '').replace('_', '')
            value = value.replace(':', '.').replace('٫', '.').replace(',', '.')
            return float(value) if value else 0.0
        except:
            return 0.0
    
    df['إجمالي ساعات العمل'] = df['إجمالي ساعات العمل'].apply(clean_work_hours)
    
    with PdfPages('تقرير_المقاولين.pdf') as pdf:
        # الصفحة 1: الغلاف
        plt.figure(figsize=(11, 8))
        plt.text(0.5, 0.7, 'تقرير تصاريح عمل المقاولين', 
                ha='center', va='center', fontsize=20, fontweight='bold')
        plt.text(0.5, 0.5, f'تاريخ التصدير: {pd.Timestamp.now().strftime("%Y-%m-%d")}', 
                ha='center', va='center', fontsize=14)
        plt.axis('off')
        pdf.savefig()
        plt.close()
        
        # الصفحة 2: الإحصائيات
        plt.figure(figsize=(11, 8))
        stats_text = f"""
        الإحصائيات العامة:
        
        إجمالي ساعات العمل: {df['إجمالي ساعات العمل'].sum():.1f}
        عدد المهام: {len(df):,}
        متوسط الساعات للمهمة: {df['إجمالي ساعات العمل'].mean():.1f}
        عدد الشركات: {df['إسم الشركة'].nunique()}
        عدد المواقع: {df['الموقع'].nunique()}
        """
        plt.text(0.1, 0.8, stats_text, fontsize=14, va='top')
        plt.axis('off')
        pdf.savefig()
        plt.close()
        
        # الصفحة 3: أفضل المواقع
        plt.figure(figsize=(11, 8))
        locations_data = df.groupby('الموقع')['إجمالي ساعات العمل'].sum().nlargest(8)
        plt.bar(range(len(locations_data)), locations_data.values)
        plt.title('أفضل المواقع حسب ساعات العمل')
        plt.xticks(range(len(locations_data)), locations_data.index, rotation=45)
        plt.tight_layout()
        pdf.savefig()
        plt.close()
        
        # الصفحة 4: أفضل الشركات
        plt.figure(figsize=(11, 8))
        companies_data = df.groupby('إسم الشركة')['إجمالي ساعات العمل'].sum().nlargest(10)
        plt.barh(range(len(companies_data)), companies_data.values)
        plt.title('أفضل 10 شركات حسب ساعات العمل')
        plt.yticks(range(len(companies_data)), companies_data.index)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

if __name__ == "__main__":
    create_pdf_report()
    print("✅ تم إنشاء التقرير كملف PDF")