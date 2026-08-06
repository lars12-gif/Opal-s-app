import streamlit as st
import sqlite3
import pandas as pd

# الاتصال بقاعدة البيانات لتخزين النقاط دائمياً
conn = sqlite3.connect('oplz_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS members (
        name TEXT PRIMARY KEY,
        oplz REAL DEFAULT 0
    )
''')
conn.commit()

# إعدادات الواجهة
st.set_page_config(page_title="نظام الأوبلز", page_icon="✨")
st.title("✨ نظام نقاط الأوبلز | Oplz System")

# نموذج إضافة النقاط
st.subheader("➕ إضافة / تحديث نقاط")
with st.form("add_points_form", clear_on_submit=True):
    member_name = st.text_input("اسم العضو / الإداري:")
    added_oplz = st.number_input("عدد الأوبلز المُضافة:", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("حفظ النقاط")

    if submitted and member_name:
        clean_name = member_name.strip()
        c.execute('''
            INSERT INTO members (name, oplz) VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET oplz = oplz + ?
        '', (clean_name, added_oplz, added_oplz))
        conn.commit()
        st.success(f"تم إضافة {added_oplz} أوبلز لـ {clean_name}")
        st.rerun()

st.divider()

# جدول الحسبة
st.subheader("🏆 حسبة الترتيب (Top Leaderboard)")
df = pd.read_sql_query("SELECT name AS 'العضو', oplz AS 'الأوبلز' FROM members ORDER BY oplz DESC", conn)

if not df.empty:
    df.index = range(1, len(df) + 1)
    st.dataframe(df, use_container_width=True)
else:
    st.info("لا يوجد أعضاء مسجلين حتى الآن.")
