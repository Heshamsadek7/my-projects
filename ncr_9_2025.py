import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

pd.set_option('display.max_rows',999)
pd.set_option('display.max_columns',999)

ncr=pd.read_excel('/media/hesham/Y/my ubntu inv/myenv/NMG13-09-2025assending/8-25/new/NCR_8_25.xlsx')

ncr.head(2)

# حاول تحويل العمود إلى datetime
ncr['شهر'] = pd.to_datetime(ncr['شهر'], errors='coerce')

# تحقق مرة أخرى من النوع
print(ncr['شهر'].dtype)

# الآن يمكنك استخدام .dt
august_cases = ncr[ncr['شهر'].dt.month == 8]
july_cases = ncr[ncr['شهر'].dt.month == 7]
sept_cases = ncr[ncr['شهر'].dt.month == 9]

print(f"يوليو: {july_cases.shape}")
print(f"أغسطس: {august_cases.shape}")
print(f"سبتمبر: {sept_cases.shape}")

# عدد الحالات في كل شهر
print(f"عدد حالات يوليو: {len(july_cases)}")
print(f"عدد حالات أغسطس: {len(august_cases)}")
print(f"عدد حالات سبتمبر: {len(sept_cases)}")

ncr_department = ncr.groupby(['الإدارة المتواجد بها الحالة', 'المتابعة\nFollow Up'])\
    ['المتابعة\nFollow Up'].count()\
    .unstack().fillna(0).astype(int)\
    .reset_index()

# حساب مجموع كل صف وإضافة عمود جديد
ncr_department['المجموع'] = ncr_department.sum(axis=1, numeric_only=True)

# ترتيب البيانات تنازلياً حسب المجموع
ncr_department = ncr_department.sort_values('المجموع', ascending=False).reset_index(drop=True)

ncr_department

px.bar(data_frame=ncr_department,
       x='الإدارة المتواجد بها الحالة',
       y=['Closed', 'Opened'],
       barmode='group',text_auto=True,
       title='حالات عدم مطابقة الستراطاتNCR')



px.bar(data_frame=ncr_department,
       x='الإدارة المتواجد بها الحالة',
       y=['Closed', 'Opened'],
       barmode='group',text_auto=True,
       title='حالات عدم مطابقة الستراطاتNCR')

ncr_hse = ncr.groupby(['إسم الشخص القائم بالتبليغ', 'المتابعة\nFollow Up'])['المتابعة\nFollow Up']\
    .count().unstack().fillna(0).astype(int).reset_index()

# إضافة عمود للمجموع
ncr_hse['المجموع'] = ncr_hse.sum(axis=1, numeric_only=True)

# إضافة عمود للترتيب من الأكثر للأقل
ncr_hse['الترتيب'] = ncr_hse['المجموع'].rank(ascending=False, method='dense').astype(int)

# ترتيب البيانات تنازلياً حسب المجموع
ncr_hse = ncr_hse.sort_values('المجموع', ascending=False).reset_index(drop=True)

ncr_hse

px.bar(data_frame=ncr_hse,x='إسم الشخص القائم بالتبليغ',y=['Closed', 'Opened'],
       barmode='group',text_auto=True,title='تقييم العاملين باﻹدارة')

px.bar(data_frame=ncr_hse,x='إسم الشخص القائم بالتبليغ',
       y=['Closed', 'Opened'], barmode='group',\
       text_auto=True,color='إسم الشخص القائم بالتبليغ',\
       title='تقييم العاملين باﻹدارة')



ncr_department7 = july_cases.groupby(['الإدارة المتواجد بها الحالة', 'المتابعة\nFollow Up'])\
    ['المتابعة\nFollow Up'].count()\
    .unstack().fillna(0).astype(int)\
    .reset_index()

# حساب مجموع كل صف وإضافة عمود جديد
ncr_department7['المجموع'] = ncr_department7.sum(axis=1, numeric_only=True)

# ترتيب البيانات تنازلياً حسب المجموع
ncr_department7 = ncr_department7.sort_values('المجموع', ascending=False).reset_index(drop=True)

ncr_department7

px.bar(data_frame=ncr_department7,x='الإدارة المتواجد بها الحالة',y=['Closed', 'Opened'], barmode='group',text_auto=True,title='حالات عدم مطابقة الستراطاتNCRيوليو2025')

ncr_hse7 = july_cases.groupby(['إسم الشخص القائم بالتبليغ', 'المتابعة\nFollow Up'])['المتابعة\nFollow Up']\
    .count().unstack().fillna(0).astype(int).reset_index()

# إضافة عمود للمجموع
ncr_hse7['المجموع'] = ncr_hse7.sum(axis=1, numeric_only=True)

# إضافة عمود للترتيب من الأكثر للأقل
ncr_hse7['الترتيب'] = ncr_hse7['المجموع'].rank(ascending=False, method='dense').astype(int)

# ترتيب البيانات تنازلياً حسب المجموع
ncr_hse7 = ncr_hse7.sort_values('المجموع', ascending=False).reset_index(drop=True)

ncr_hse7

px.bar(data_frame=ncr_hse7,x='إسم الشخص القائم بالتبليغ',y=['Closed', 'Opened'], barmode='group',text_auto=True,title=' تقييم العاملين باﻹدارةيوليو2025')

px.bar(data_frame=ncr_hse7,x='إسم الشخص القائم بالتبليغ',y=['Closed', 'Opened'], barmode='group',\
       text_auto=True,color='إسم الشخص القائم بالتبليغ',\
       title='شهر يوليو 2025تقييم العاملين باﻹدارة')

ncr_department8 = august_cases.groupby(['الإدارة المتواجد بها الحالة', 'المتابعة\nFollow Up'])\
    ['المتابعة\nFollow Up'].count()\
    .unstack().fillna(0).astype(int)\
    .reset_index()

# حساب مجموع كل صف وإضافة عمود جديد
ncr_department8['المجموع'] = ncr_department8.sum(axis=1, numeric_only=True)

# ترتيب البيانات تنازلياً حسب المجموع
ncr_department8 = ncr_department8.sort_values('المجموع', ascending=False).reset_index(drop=True)

ncr_department8

px.bar(data_frame=ncr_department8,x='الإدارة المتواجد بها الحالة',y=['Closed', 'Opened'], barmode='group',text_auto=True,title='حالات عدم مطابقة لشهر أغسطس 2025')

ncr_hse8 = august_cases.groupby(['إسم الشخص القائم بالتبليغ', 'المتابعة\nFollow Up'])['المتابعة\nFollow Up']\
    .count().unstack().fillna(0).astype(int).reset_index()

# إضافة عمود للمجموع
ncr_hse8['المجموع'] = ncr_hse8.sum(axis=1, numeric_only=True)

# إضافة عمود للترتيب من الأكثر للأقل
ncr_hse8['الترتيب'] = ncr_hse8['المجموع'].rank(ascending=False, method='dense').astype(int)

# ترتيب البيانات تنازلياً حسب المجموع
ncr_hse8 = ncr_hse8.sort_values('المجموع', ascending=False).reset_index(drop=True)

ncr_hse8

px.bar(data_frame=ncr_hse8,x='إسم الشخص القائم بالتبليغ',y=['Closed', 'Opened'], barmode='group',text_auto=True,title="تقييم العاملين بالادارة أغسطس 2025")

px.bar(data_frame=ncr_hse8,x='إسم الشخص القائم بالتبليغ',y=['Closed', 'Opened'], barmode='group',\
       text_auto=True,color='إسم الشخص القائم بالتبليغ',\
       title='8/2025تقييم العاملين باﻹدارة')

ncr_department9 = sept_cases.groupby(['الإدارة المتواجد بها الحالة', 'المتابعة\nFollow Up'])\
    ['المتابعة\nFollow Up'].count()\
    .unstack().fillna(0).astype(int)\
    .reset_index()

# حساب مجموع كل صف وإضافة عمود جديد
ncr_department9['المجموع'] = ncr_department7.sum(axis=1, numeric_only=True)

# ترتيب البيانات تنازلياً حسب المجموع
ncr_department9 = ncr_department7.sort_values('المجموع', ascending=False).reset_index(drop=True)

ncr_department9

px.bar(data_frame=ncr_department7,x='الإدارة المتواجد بها الحالة',y=['Closed', 'Opened'],
       barmode='group',text_auto=True,title='حالات عدم مطابقة الستراطاتNCRسبتمبر2025')

ncr_hse9 = sept_cases.groupby(['إسم الشخص القائم بالتبليغ', 'المتابعة\nFollow Up'])['المتابعة\nFollow Up']\
    .count().unstack().fillna(0).astype(int).reset_index()

# إضافة عمود للمجموع
ncr_hse9['المجموع'] = ncr_hse9.sum(axis=1, numeric_only=True)

# إضافة عمود للترتيب من الأكثر للأقل
ncr_hse9['الترتيب'] = ncr_hse9['المجموع'].rank(ascending=False, method='dense').astype(int)

# ترتيب البيانات تنازلياً حسب المجموع
ncr_hse9 = ncr_hse9.sort_values('المجموع', ascending=False).reset_index(drop=True)

ncr_hse9

px.bar(data_frame=ncr_hse9,x='إسم الشخص القائم بالتبليغ',y=['Closed', 'Opened'], barmode='group',text_auto=True,title=' تقييم العاملين باﻹدارة سبتمبر 2025')

px.bar(data_frame=ncr_hse9,x='إسم الشخص القائم بالتبليغ',y=['Closed', 'Opened'], barmode='group',\
       text_auto=True,color='إسم الشخص القائم بالتبليغ',\
       title='شهر سبتمبر 2025تقييم العاملين باﻹدارة')