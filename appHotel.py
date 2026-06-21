import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="نظام حجز الفنادق ", page_icon="🏨", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700&display=swap');
    
    /* الخط العام */
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif !important; }

    /* تنسيق الـ Metrics (توسيط في الأعمدة) */
    [data-testid="stMetric"] { 
        text-align: center !important; 
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    [data-testid="stMetricLabel"] p { font-size: 20px !important; font-weight: bold !important; color: #555 !important; }
    [data-testid="stMetricValue"] { font-size: 40px !important; font-weight: 900 !important; color: #1a2a3a !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: right; font-family: 'Tajawal', sans-serif;">
        <h1 style="font-weight: bold; font-size: 70px;">🏨 نظام حجز الفنادق</h1>
        <p style="font-weight: bold; font-size: 22px;"> نظام ذكي لاستعراض ومقارنة خيارات الإقامة الفندقية في المملكة العربية السعودية بدقة وسهولة.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()



# مثال لمسار ويندوز (عدليه حسب مكان ملفك الحقيقي)
file_name = "final_hotels_clean.csv"
df = pd.read_csv(file_name)

# 3. عنوان "فلاتر البحث" (يُوضع في الـ Sidebar)
st.sidebar.markdown('<div style="text-align: right; font-family: \'Tajawal\', sans-serif; font-size: 26px; font-weight: bold; margin-bottom: 20px;">🔍 فلاتر البحث</div>', unsafe_allow_html=True)

st.sidebar.markdown("---") # فاصل بين الفلاتر
selected_city = st.sidebar.selectbox("اختر المدينة", sorted(df['location'].unique()))

st.sidebar.markdown("---") # فاصل بين الفلاتر


all_types = sorted(df['property_type'].unique())
selected_type = st.sidebar.multiselect("نوع السكن", options=all_types, default=all_types)

st.sidebar.markdown("---") # فاصل بين الفلاتر

price_range = st.sidebar.slider("نطاق السعر", int(df['price'].min()), int(df['price'].max()))

st.sidebar.markdown("---") # فاصل بين الفلاتر


# 1. تعريف المتغير (هذا السطر مهم جداً قبل الـ multiselect)
all_room_types = list(df['room_type'].unique())

# 2. الفلتر الخاص بنوع الغرفة
selected_rooms = st.sidebar.multiselect("نوع الغرفة ", options=all_room_types, default=all_room_types)

st.sidebar.markdown("---") # فاصل بين الفلاتر

selected_rating = st.sidebar.slider(
     "التقييم", 
    min_value=0.0, 
    max_value=10.0, 
    value=0.0, 
    step=0.1
)

st.sidebar.markdown("---") # فاصل بين الفلاتر

# 4. تنفيذ الفلترة
filtered_df = df[
    (df['location'] == selected_city) & 
    (df['property_type'].isin(selected_type)) & 
    (df['price'] <= price_range) &
    (df['rating'] >= selected_rating)&
    (df['room_type'].isin(selected_rooms))
]

st.markdown('<h2 style="text-align: right; margin-bottom: 20px;">📊 مؤشرات الأداء الرئيسية</h2>', unsafe_allow_html=True)

count = len(filtered_df)
avg_price = filtered_df['price'].mean() if count > 0 else 0
avg_rating = filtered_df['rating'].mean() if count > 0 else 0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.markdown(f"""
    <div style="background-color: #262730; padding: 20px; border-radius: 15px; border: 1px solid #e6e6e6; text-align: center;">
        <div style="font-size: 24px;">🏨</div>
        <div style="color: #6c757d; font-size: 16px;">عدد الأماكن</div>
        <div style="font-size: 28px; font-weight: bold; color: #636EFA;">{count}</div>
    </div>
""", unsafe_allow_html=True)
kpi2.markdown(f"""
    <div style="background-color: #262730; padding: 20px; border-radius: 15px; border: 1px solid #e6e6e6; text-align: center;">
        <div style="font-size: 24px;">💰</div>
        <div style="color: #6c757d; font-size: 16px;">متوسط السعر</div>
        <div style="font-size: 28px; font-weight: bold; color: #EF553B;">{avg_price:,.0f} ر.س</div>
    </div>
""", unsafe_allow_html=True)
kpi3.markdown(f"""
    <div style="background-color: #262730; padding: 20px; border-radius: 15px; border: 1px solid #e6e6e6; text-align: center;">
        <div style="font-size: 24px;">⭐</div>
        <div style="color: #6c757d; font-size: 16px;">متوسط التقييم</div>
        <div style="font-size: 28px; font-weight: bold; color: #00CC96;">{avg_rating:.1f} / 10</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider() 

# 4. عنوان "تفاصيل البيانات" (يُوضع قبل الجدول)
st.markdown('<div style="text-align: right; font-family: \'Tajawal\', sans-serif; font-size: 28px; font-weight: bold; margin-top: 40px; margin-bottom: 20px; border-right: 5px solid #1a2a3a; padding-right: 15px;">تفاصيل البيانات</div>', unsafe_allow_html=True)

st.dataframe(filtered_df, use_container_width=True)
 

st.divider()

# تعريف ألوان الباستيل لاستخدامها في كل الرسومات
pastel_colors = px.colors.qualitative.Plotly

st.markdown('<div style="text-align: right; font-size: 28px; font-weight: bold;">📊 لوحة تحليل البيانات</div>', unsafe_allow_html=True)

# تقسيم الصفحة لصفين
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# شرط الحماية لضمان عدم ظهور أخطاء أو رسائل تحذيرية مزعجة
if not filtered_df.empty:
    
    with row1_col1:
        st.markdown('<div style="text-align: right; font-family: \'Tajawal\', sans-serif; font-size: 28px; font-weight: bold; margin-top: 40px; margin-bottom: 20px; border-right: 5px solid #1a2a3a; padding-right: 15px;">متوسط السعر حسب النوع</div>', unsafe_allow_html=True)
        avg_price_df = filtered_df.groupby('property_type')['price'].mean().reset_index()
        
        fig1 = px.bar(avg_price_df, x='property_type', y='price', color='property_type', 
                      text_auto='.1f', color_discrete_sequence=pastel_colors)
        st.plotly_chart(fig1, use_container_width=True)

    with row1_col2:
        st.markdown('<div style="text-align: right; font-family: \'Tajawal\', sans-serif; font-size: 28px; font-weight: bold; margin-top: 40px; margin-bottom: 20px; border-right: 5px solid #1a2a3a; padding-right: 15px;"> أنواع السكن</div>', unsafe_allow_html=True)
        fig2 = px.pie(filtered_df, names='property_type', hole=0.4, 
                      color_discrete_sequence=pastel_colors)
        fig2.update_traces(textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)

    with row2_col1:
        st.markdown('<div style="text-align: right; font-family: \'Tajawal\', sans-serif; font-size: 28px; font-weight: bold; margin-top: 40px; margin-bottom: 20px; border-right: 5px solid #1a2a3a; padding-right: 15px;">السعر مقابل التقييم</div>', unsafe_allow_html=True)
        fig3 = px.scatter(filtered_df, x='price', y='rating', color='property_type', 
                          size='rating', hover_data=['name'], template="plotly_white",
                          color_discrete_sequence=pastel_colors)
        st.plotly_chart(fig3, use_container_width=True)

    with row2_col2:
        st.markdown('<div style="text-align: right; font-family: \'Tajawal\', sans-serif; font-size: 28px; font-weight: bold; margin-top: 40px; margin-bottom: 20px; border-right: 5px solid #1a2a3a; padding-right: 15px;">تفاوت وتوزيع التقييم</div>', unsafe_allow_html=True)
        fig4 = px.box(filtered_df, x='property_type', y='rating', color='property_type',
                      color_discrete_sequence=pastel_colors)
        st.plotly_chart(fig4, use_container_width=True)