import sqlite3
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة والواجهة العصرية
st.set_page_config(
    page_title="نظام نقاط الأوبلز | Oplz System",
    page_icon="💎",
    layout="centered",
)

# تخصيص التصميم والاتجاه (RTL)
st.markdown(
    """
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .main-title {
        text-align: center;
        color: #4DEF8E;
        font-weight: bold;
        font-size: 2.2rem;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #A0AAB8;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. إدارة قاعدة البيانات
DB_NAME = "oplz_data.db"


def get_connection():
  return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
  conn = get_connection()
  c = conn.cursor()
  c.execute(
      "CREATE TABLE IF NOT EXISTS members (name TEXT PRIMARY KEY, oplz REAL"
      " DEFAULT 0)"
  )
  conn.commit()
  conn.close()


init_db()


# 3. حساب الرتبة بناءً على النقاط
def get_rank(oplz):
  if oplz >= 100:
    return "🏆 LEGEND (الأسطورة)"
  elif oplz >= 50:
    return "🌟 ELITE (النخبة)"
  elif oplz >= 10:
    return "🔥 ACTIVE (المتفاعل)"
  else:
    return "🌱 ROOKIE (الوافد)"


# 4. الواجهة الرئيسية
st.markdown(
    '<p class="main-title">✨ نظام نقاط الأوبلز | Oplz System ✨</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">لوحة تحكم إدارية لتتبع النقاط وترتيب الأعضاء</p>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 الحسبة والترتيب",
    "📋 تصدير الرسالة",
    "➕ إضافة / تعديل نقاط",
    "⚙️ إدارة الأعضاء",
])

# --- التبويب الأول: جدول الحسبة والترتيب ---
with tab1:
  conn = get_connection()
  df = pd.read_sql_query(
      "SELECT name AS 'العضو', oplz AS 'الأوبلز' FROM members ORDER BY oplz DESC",
      conn,
  )
  conn.close()

  if not df.empty:
    df["الرتبة"] = df["الأوبلز"].apply(get_rank)

    col1, col2, col3 = st.columns(3)
    if len(df) >= 1:
      col1.metric(
          "🥇 المركز الأول",
          df.iloc[0]["العضو"],
          f"{df.iloc[0]['الأوبلز']:g} أوبلز",
      )
    if len(df) >= 2:
      col2.metric(
          "🥈 المركز الثاني",
          df.iloc[1]["العضو"],
          f"{df.iloc[1]['الأوبلز']:g} أوبلز",
      )
    if len(df) >= 3:
      col3.metric(
          "🥉 المركز الثالث",
          df.iloc[2]["العضو"],
          f"{df.iloc[2]['الأوبلز']:g} أوبلز",
      )

    st.divider()

    df.index = range(1, len(df) + 1)
    st.dataframe(
        df,
        column_config={
            "العضو": st.column_config.TextColumn("اسم العضو"),
            "الأوبلز": st.column_config.NumberColumn(
                "رصيد الأوبلز", format="%.1f 🪙"
            ),
            "الرتبة": st.column_config.TextColumn("الرتبة المستحقة"),
        },
        use_container_width=True,
    )
  else:
    st.info("💡 لا يوجد أعضاء مسجلين حتى الآن. ابدأ بإضافة النقاط من التبويب المالي.")

# --- التبويب الثاني: تصدير الرسالة جاهزة للمجموعة ---
with tab2:
  st.subheader("📋 تصدير الحسبة كنص جاهز للمجموعة")
  st.write("يمكنك نسخ النص أدناه بلمسة زر وإرساله مباشرة إلى سيرفر المجموعة:")

  conn = get_connection()
  df_export = pd.read_sql_query(
      "SELECT name, oplz FROM members ORDER BY oplz DESC", conn
  )
  conn.close()

  if not df_export.empty:
    msg_lines = [
        "✨ **دليل نظام نقاط الأوبلز | Oplz System** ✨\n",
        "📊 **حسبة الترتيب العام للأعضاء (Top Leaderboard):**\n",
    ]

    for rank, row in enumerate(df_export.itertuples(), start=1):
      name = row.name
      oplz = row.oplz
      user_rank = get_rank(oplz)

      prefix = "▫️"
      if rank == 1:
        prefix = "🥇"
      elif rank == 2:
        prefix = "🥈"
      elif rank == 3:
        prefix = "🥉"

      msg_lines.append(
          f"{prefix} **#{rank} {name}** ➔ {oplz:g} أوبلز | {user_rank}"
      )

    msg_lines.append("\n🚀 *استمروا في التفاعل والمشاركة لزيادة رصيد الأوبلز!*")
    full_message = "\n".join(msg_lines)

    st.code(full_message, language="markdown")
    st.caption("💡 اضغط على أيقونة النسخ المجهزة أعلى مربع النص لأخذه حافظتك مباشرة.")
  else:
    st.info("لا توجد بيانات حالياً لتصديرها.")

# --- التبويب الثالث: إضافة وتعديل النقاط ---
with tab3:
  st.subheader("تسجيل النقاط")

  mode = st.radio(
      "اختر طريقة الإضافة:",
      ["إضافة أوبلز مباشرة 💎", "تحويل نقاط تفاعل (كل 50 نقطة = 1 أوبلز) 🪙"],
      horizontal=True,
  )

  with st.form("add_form", clear_on_submit=True):
    name_input = st.text_input("اسم العضو / الإداري:")

    if "مباشرة" in mode:
      val_input = st.number_input(
          "عدد الأوبلز المُضافة:", min_value=0.1, value=1.0, step=0.5
      )
    else:
      act_input = st.number_input(
          "عدد نقاط التفاعل:", min_value=1, value=50, step=10
      )
      val_input = act_input / 50.0

    btn_submit = st.form_submit_button("🚀 حفظ النقاط")

    if btn_submit:
      if name_input.strip():
        clean_name = name_input.strip()
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO members (name, oplz) VALUES (?, ?) ON CONFLICT(name)"
            " DO UPDATE SET oplz = oplz + ?",
            (clean_name, val_input, val_input),
        )
        conn.commit()
        conn.close()

        st.success(f"✅ تم إضافة {val_input:g} أوبلز بنجاح لـ ({clean_name})")
        st.rerun()
      else:
        st.warning("⚠️ يرجى كتابة اسم العضو أولاً!")

# --- التبويب الرابع: إدارة الأعضاء ---
with tab4:
  st.subheader("⚙️ تعديل البيانات")

  conn = get_connection()
  df_members = pd.read_sql_query("SELECT name FROM members ORDER BY name", conn)
  conn.close()

  if not df_members.empty:
    member_list = df_members["name"].tolist()
    selected_member = st.selectbox("اختر عضواً للتعديل:", member_list)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
      new_val = st.number_input(
          "تحديد رصيد جديد كلياً:", min_value=0.0, step=0.5
      )
      if st.button("✏️ حفظ الرصيد الجديد"):
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "UPDATE members SET oplz = ? WHERE name = ?",
            (new_val, selected_member),
        )
        conn.commit()
        conn.close()
        st.success(f"تم تغيير رصيد {selected_member} إلى {new_val:g} أوبلز.")
        st.rerun()

    with col_btn2:
      if st.button(f"❌ حذف {selected_member} نهائياً"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM members WHERE name = ?", (selected_member,))
        conn.commit()
        conn.close()
        st.warning(f"تم حذف العضو {selected_member}.")
        st.rerun()
  else:
    st.info("لا يوجد أعضاء في القائمة حالياً.")
          
