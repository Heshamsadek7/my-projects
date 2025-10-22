# test_arabic.py
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt

print("🔍 اختبار المكتبات...")

# نص عربي للاختبار
arabic_text = "تقرير تصاريح المقاولين - يوليو 2025"

try:
    # تعديل النص للعرض الصحيح
    reshaped_text = arabic_reshaper.reshape(arabic_text)
    bidi_text = get_display(reshaped_text)
    
    print("✅ النص الأصلي:", arabic_text)
    print("✅ بعد المعالجة:", bidi_text)
    
    # اختبار الرسم
    plt.figure(figsize=(10, 6))
    plt.text(0.5, 0.6, bidi_text, fontsize=20, ha='center', va='center', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    plt.title(bidi_text, fontsize=16)
    plt.axis('off')
    plt.savefig('test_arabic.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ تم حفظ الصورة الاختبارية: test_arabic.png")
    
except Exception as e:
    print(f"❌ خطأ في الاختبار: {e}")