import sqlite3
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة والواجهة العصرية
st.set_page_config(
    page_title="نظام نقاط Opal's | Opal's System",
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
    .admin-info {
        text-align: center;
        background-color: #1E2638;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 25px;
        border: 1px solid #2E3A52;
    }
    .admin-badge {
        display: inline-block;
        margin: 0 10px;
        font-size: 1.05rem;
        color: #E2E8F0;
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
      " DEFAULT 0, role TEXT DEFAULT 'عضو')"
  )

  # إضافة عمود role في حال كانت قاعدة البيانات قديمة
  try:
    c.execute("ALTER TABLE members ADD COLUMN role TEXT DEFAULT 'عضو'")
  except sqlite3.OperationalError:
    pass

  conn.commit()
  conn.close()


init_db()


# 3. حساب الرتبة بناءً على النقاط والصفة (عضو / إداري)
def get_rank(oplz, role="عضو"):
  if role == "إداري":
    if oplz >= 800:
      return "⚔️ LEADER (القائد)"
    elif oplz >= 500:
      return "📊 OPAL'S MANAGER (مسؤول النقاط)"
    elif oplz >= 300:
      return "🔰 MODERATOR (المشرف العام)"
    elif oplz >= 150:
      return "🎭 HOST (المضيف)"
    elif oplz >= 75:
      return "⚡ ADMIN (الإداري)"
    else:
      return "❇️ NEW ADMIN (إداري مستجد)"
  else:
    # رتب الأعضاء
    if oplz >= 500:
      return "🏆 LEGEND (الأسطورة)"
    elif oplz >= 200:
      return "🌟 ELITE (النخبة)"
    elif oplz >= 50:
      return "🔥 ACTIVE (المتفاعل)"
    else:
      return "🌱 ROOKIE (الوافد)"


# 4. الواجهة الرئيسية
st.markdown(
    '<p class="main-title">✨ نظام نقاط Opal\'s | Opal\'s System ✨</p>',
    unsafe_allow_html=True,
)

# عرض معلومات الإدارة (المشرف والمساعد)
st.markdown(
    """
    <div class="admin-info">
        <span class="admin-badge">👑 <b>المشرف العام:</b> Aurther</span>
        <span style="color: #4A5568;">|</span>
        <span class="admin-badge">🤝 <b>المساعد:</b> Lamino</span>
    </div>
""",
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
      "SELECT name, oplz, role FROM members ORDER BY oplz DESC", conn
  )
  conn.close()

  if not df.empty:
    df.columns = ["العضو", "Opal's", "الصفة"]
    df["الرتبة"] = df.apply(
        lambda r: get_rank(r["Opal's"], r["الصفة"]), axis=1
    )

    col1, col2, col3 = st.columns(3)
    if len(df) >= 1:
      col1.metric(
          "🥇 المركز الأول",
          df.iloc[0]["العضو"],
          f"{df.iloc[0]['Opal\'s']:g} Opal's",
      )
    if len(df) >= 2:
      col2.metric(
          "🥈 المركز الثاني",
          df.iloc[1]["العضو"],
          f"{df.iloc[1]['Opal\'s']:g} Opal's",
      )
    if len(df) >= 3:
      col3.metric(
          "🥉 المركز الثالث",
          df.iloc[2]["العضو"],
          f"{df.iloc[2]['Opal\'s']:g} Opal's",
      )

    st.divider()

    df.index = range(1, len(df) + 1)
    st.dataframe(
        df,
        column_config={
            "العضو": st.column_config.TextColumn("اسم العضو"),
            "الصفة": st.column_config.TextColumn("نوع الحساب"),
            "Opal's": st.column_config.NumberColumn(
                "رصيد Opal's", format="%.1f 🪙"
            ),
            "الرتبة": st.column_config.TextColumn("الرتبة المستحقة"),
        },
        use_container_width=True,
    )
  else:
    st.info("💡 لا يوجد أعضاء مسجلين حتى الآن. ابدأ بإضافة النقاط من التبويب المالي.")

  # دليل متطلبات الرتب في أسفل الصفحة
  with st.expander("📜 دليل ومتطلبات رتب الأوبلز (Opal System)"):
    st.markdown("""
        ### 👥 **رتب الأعضاء (التفاعل والفعاليات):**
        * 🌱 **ROOKIE (الوافد):** 0 - 20 أوبلز
        * 🔥 **ACTIVE (المتفاعل):** 50 أوبلز
        * 🌟 **ELITE (النخبة):** 200 أوبلز
        * 🏆 **LEGEND (الأسطورة):** 500 أوبلز

        ---

        ### 🛡️ **رتب الإدارة (الإنجازات والمهام):**
        * ❇️ **NEW ADMIN (إداري مستجد):** 30 أوبلز
        * ⚡ **ADMIN (الإداري):** 75 أوبلز
        * 🎭 **HOST (المضيف):** 150 أوبلز
        * 🔰 **MODERATOR (المشرف العام):** 300 أوبلز
        * 📊 **OPAL'S MANAGER (مسؤول النقاط):** 500 أوبلز
        * ⚔️ **LEADER (القائد):** 800 أوبلز
        """)

# --- التبويب الثاني: تصدير الرسالة جاهزة للمجموعة ---
with tab2:
  st.subheader("📋 تصدير الحسبة كنص جاهز للمجموعة")
  st.write("يمكنك نسخ النص أدناه بلمسة زر وإرساله مباشرة إلى سيرفر المجموعة:")

  conn = get_connection()
  df_export = pd.read_sql_query(
      "SELECT name, oplz, role FROM members ORDER BY oplz DESC", conn
  )
  conn.close()

  if not df_export.empty:
    msg_lines = [
        "✨ **دليل ونظام رتب الأوبلز | Opal's System** ✨",
        "👑 **المشرف العام:** Aurther | 🤝 **المساعد:** Lamino\n",
        "📊 **حسبة الترتيب العام للأعضاء والإدارة:**\n",
    ]

    for rank, row in enumerate(df_export.itertuples(), start=1):
      name = row.name
      oplz = row.oplz
      role = getattr(row, "role", "عضو")
      user_rank = get_rank(oplz, role)

      prefix = "▫️"
      if rank == 1:
        prefix = "🥇"
      elif rank == 2:
        prefix = "🥈"
      elif rank == 3:
        prefix = "🥉"

      tag = "🛡️" if role == "إداري" else "👥"
      msg_lines.append(
          f"{prefix} **#{rank} {name}** [{tag}] ➔ {oplz:g} Opal's | {user_rank}"
      )

    msg_lines.append("\n🚀 *استمروا في التفاعل والمشاركة لزيادة رصيد Opal's!*")
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
      [
          "إضافة Opal's مباشرة 💎",
          "تحويل نقاط تفاعل (كل 50 نقطة = 1 Opal's) 🪙",
      ],
      horizontal=True,
  )

  with st.form("add_form", clear_on_submit=True):
    name_input = st.text_input("اسم العضو / الإداري:")
    role_input = st.radio(
        "نوع الحساب / الصفة:", ["عضو متفاعل 👥", "إداري 🛡️"], horizontal=True
    )

    if "مباشرة" in mode:
      val_input = st.number_input(
          "عدد Opal's المُضافة:", min_value=0.1, value=1.0, step=0.5
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
        clean_role = "إداري" if "إداري" in role_input else "عضو"

        conn = get_connection()
        c = conn.cursor()
        c.execute(
            """
                    INSERT INTO members (name, oplz, role) VALUES (?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET 
                        oplz = oplz + ?,
                        role = ?
                """,
            (clean_name, val_input, clean_role, val_input, clean_role),
        )
        conn.commit()
        conn.close()

        st.success(
            f"✅ تم إضافة {val_input:g} Opal's بنجاح لـ ({clean_name}) بصفة"
            f" {clean_role}"
        )
        st.rerun()
      else:
        st.warning("⚠️ يرجى كتابة اسم العضو أولاً!")

# --- التبويب الرابع: إدارة الأعضاء ---
with tab4:
  st.subheader("⚙️ تعديل البيانات")

  conn = get_connection()
  df_members = pd.read_sql_query(
      "SELECT name, role, oplz FROM members ORDER BY name", conn
  )
  conn.close()

  if not df_members.empty:
    member_list = df_members["name"].tolist()
    selected_member = st.selectbox("اختر عضواً للتعديل:", member_list)

    # جلب معلومات العضو المختار
    current_info = df_members[df_members["name"] == selected_member].iloc[0]

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
      new_val = st.number_input(
          "تحديد رصيد Opal's جديد كلياً:",
          min_value=0.0,
          value=float(current_info["oplz"]),
          step=0.5,
      )
      new_role_sel = st.radio(
          "تعديل الصفة:",
          ["عضو متفاعل 👥", "إداري 🛡️"],
          index=1 if current_info["role"] == "إداري" else 0,
          horizontal=True,
      )

      if st.button("✏️ حفظ التعديلات"):
        clean_new_role = "إداري" if "إداري" in new_role_sel else "عضو"
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "UPDATE members SET oplz = ?, role = ? WHERE name = ?",
            (new_val, clean_new_role, selected_member),
        )
        conn.commit()
        conn.close()
        st.success(f"تم تحديث بيانات {selected_member} بنجاح.")
        st.rerun()

    with col_btn2:
      st.write("---")
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
      
