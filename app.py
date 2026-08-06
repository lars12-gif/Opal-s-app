import io
import os
import sqlite3
import arabic_reshaper
from bidi.algorithm import get_display
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import requests
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="نظام Opal's | حسبة النقاط", page_icon="💎", layout="centered"
)

st.markdown(
    """
    <style>
    .stApp { direction: rtl; text-align: right; }
    .main-title { text-align: center; color: #4DEF8E; font-weight: bold; font-size: 2rem; margin-bottom: 5px; }
    .admin-info { text-align: center; background-color: #1E2638; border-radius: 10px; padding: 10px; margin-bottom: 20px; border: 1px solid #2E3A52; }
    .admin-badge { display: inline-block; margin: 0 10px; font-size: 1rem; color: #E2E8F0; }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. قاعدة البيانات
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
  conn.commit()
  conn.close()


init_db()


# 3. حساب الرتب
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
    if oplz >= 500:
      return "🏆 LEGEND (الأسطورة)"
    elif oplz >= 200:
      return "🌟 ELITE (النخبة)"
    elif oplz >= 50:
      return "🔥 ACTIVE (المتفاعل)"
    else:
      return "🌱 ROOKIE (الوافد)"


# 4. دالة الخط العربي وتنسيق النصوص
def get_font(size):
  font_path = "Tajawal-Bold.ttf"
  if not os.path.exists(font_path):
    url = "https://github.com/google/fonts/raw/main/ofl/tajawal/Tajawal-Bold.ttf"
    r = requests.get(url)
    with open(font_path, "wb") as f:
      f.write(r.content)
  return ImageFont.truetype(font_path, size)


def fix_arabic(text):
  reshaped = arabic_reshaper.reshape(str(text))
  return get_display(reshaped)


# 5. دالة رسم بطاقة الحسبة مباشرة كصورة
def generate_leaderboard_image(df):
  width = 850
  height = 150 + (len(df) * 80)
  height = max(height, 450)

  img = Image.new("RGB", (width, height), color="#0F172A")
  draw = ImageDraw.Draw(img)

  font_title = get_font(36)
  font_sub = get_font(20)
  font_card = get_font(22)

  # الهيدر العلوي
  draw.rectangle([0, 0, width, 110], fill="#1E293B")
  draw.text(
      (width / 2, 35),
      fix_arabic("✨ Opal's System | حسبة الترتيب ✨"),
      fill="#4DEF8E",
      font=font_title,
      anchor="mm",
  )
  draw.text(
      (width / 2, 80),
      fix_arabic("👑 Aurther  |  🤝 Lamino"),
      fill="#94A3B8",
      font=font_sub,
      anchor="mm",
  )

  # رسم صفوف الأعضاء
  y_offset = 130
  for rank, row in enumerate(df.itertuples(index=False), start=1):
    name, oplz, role = row[0], row[1], row[2]
    rank_title = get_rank(oplz, role)

    # ألوان مراكز الصدارة
    bg_color = "#1E293B"
    text_color = "#FFFFFF"
    rank_icon = f"#{rank}"

    if rank == 1:
      bg_color = "#3B270C"
      text_color = "#FFD700"
      rank_icon = "🥇 #1"
    elif rank == 2:
      bg_color = "#28303D"
      text_color = "#C0C0C0"
      rank_icon = "🥈 #2"
    elif rank == 3:
      bg_color = "#33221A"
      text_color = "#CD7F32"
      rank_icon = "🥉 #3"

    draw.rounded_rectangle(
        [30, y_offset, width - 30, y_offset + 65],
        radius=10,
        fill=bg_color,
        outline="#334155",
        width=1,
    )

    tag_str = "[إداري]" if role == "إداري" else "[عضو]"
    name_str = f"{name} {tag_str}"
    score_str = f"{oplz:g} Opal's  |  {rank_title}"

    # كتابة المركز والاسم على اليمين والنقاط على اليسار
    draw.text(
        (width - 50, y_offset + 32),
        rank_icon,
        fill=text_color,
        font=font_card,
        anchor="rm",
    )
    draw.text(
        (width - 150, y_offset + 32),
        fix_arabic(name_str),
        fill="#F8FAFC",
        font=font_card,
        anchor="rm",
    )
    draw.text(
        (50, y_offset + 32),
        fix_arabic(score_str),
        fill=text_color,
        font=font_card,
        anchor="lm",
    )

    y_offset += 75

  img_byte_arr = io.BytesIO()
  img.save(img_byte_arr, format="PNG")
  return img_byte_arr.getvalue()


# 6. واجهة المستخدم
st.markdown(
    '<p class="main-title">✨ نظام نقاط Opal\'s | حسبة الترتيب ✨</p>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="admin-info">
        <span class="admin-badge">👑 <b>المشرف:</b> Aurther</span>
        <span style="color: #4A5568;">|</span>
        <span class="admin-badge">🤝 <b>المساعد:</b> Lamino</span>
    </div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(
    ["📸 صورة الحسبة والترتيب", "➕ إضافة / تعديل نقاط", "⚙️ إدارة الأعضاء"]
)

# --- التبويب الأول: الصورة الجاهزة مباشرة للحفظ ---
with tab1:
  conn = get_connection()
  df = pd.read_sql_query(
      "SELECT name, oplz, role FROM members ORDER BY oplz DESC", conn
  )
  conn.close()

  if not df.empty:
    st.subheader("🖼️ بطاقة الحسبة جاهزة للحفظ:")

    # توليد الصورة فوراً
    img_bytes = generate_leaderboard_image(df)

    # عرض الصورة بحجم متوافق مع كافة الشاشات
    st.image(img_bytes, use_container_width=True)

    # زر التحميل السريع
    st.download_button(
        label="📥 ضغطة واحدة لحفظ الصورة على جهازك",
        data=img_bytes,
        file_name="opals_leaderboard.png",
        mime="image/png",
        use_container_width=True,
    )
  else:
    st.info("💡 لا يوجد أعضاء مسجلين حتى الآن. قم بفيض النقاط من التبويب الثاني.")

# --- التبويب الثاني: إضافة وتعديل النقاط ---
with tab2:
  st.subheader("تسجيل النقاط")

  mode = st.radio(
      "طريقة الإضافة:",
      ["إضافة Opal's مباشرة 💎", "تحويل نقاط تفاعل (كل 50 نقطة = 1 Opal's) 🪙"],
      horizontal=True,
  )

  with st.form("add_form", clear_on_submit=True):
    name_input = st.text_input("اسم العضو / الإداري:")
    role_input = st.radio(
        "نوع الحساب:", ["عضو متفاعل 👥", "إداري 🛡️"], horizontal=True
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

    if st.form_submit_button("🚀 حفظ وزيادة النقاط"):
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

        st.success(f"✅ تم إضافة {val_input:g} Opal's لـ {clean_name}")
        st.rerun()

# --- التبويب الثالث: تعديل وحذف ---
with tab3:
  conn = get_connection()
  df_m = pd.read_sql_query("SELECT name, role, oplz FROM members", conn)
  conn.close()

  if not df_m.empty:
    selected = st.selectbox("اختر عضواً للتعديل أو الحذف:", df_m["name"])
    curr = df_m[df_m["name"] == selected].iloc[0]

    col_a, col_b = st.columns(2)
    with col_a:
      new_val = st.number_input(
          "تعديل الرصيد:", value=float(curr["oplz"]), step=0.5
      )
      if st.button("✏️ تحديث الرصيد"):
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "UPDATE members SET oplz = ? WHERE name = ?", (new_val, selected)
        )
        conn.commit()
        conn.close()
        st.success("تم التحديث!")
        st.rerun()

    with col_b:
      if st.button(f"❌ حذف {selected}"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM members WHERE name = ?", (selected,))
        conn.commit()
        conn.close()
        st.rerun()
      
