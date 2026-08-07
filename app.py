import math
import sqlite3
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

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


# 4. تصميم بطاقة أفقية عريضة (Landscape Mode)
def create_html_card(df):
  rows_html = ""

  for rank, row in enumerate(df.itertuples(index=False), start=1):
    name, oplz, role = str(row[0]), float(row[1]), str(row[2])
    rank_title = get_rank(oplz, role)

    rank_class = "rank-normal"
    badge_class = "b-normal"
    badge_text = f"#{rank}"

    if rank == 1:
      rank_class = "rank-1"
      badge_class = "b-1"
      badge_text = "🥇 #1"
    elif rank == 2:
      rank_class = "rank-2"
      badge_class = "b-2"
      badge_text = "🥈 #2"
    elif rank == 3:
      rank_class = "rank-3"
      badge_class = "b-3"
      badge_text = "🥉 #3"

    role_tag = (
        '<span class="role-tag tag-admin">🛡️ إداري</span>'
        if role == "إداري"
        else '<span class="role-tag tag-user">👥 عضو</span>'
    )

    rows_html += f"""
        <div class="member-card {rank_class}">
            <div class="right-section">
                <span class="badge {badge_class}">{badge_text}</span>
                <div class="name-box">
                    <span class="member-name">{name}</span>
                    {role_tag}
                </div>
            </div>
            <div class="left-section">
                <span class="points">{oplz:g} Opal's</span>
                <span class="rank-title">{rank_title}</span>
            </div>
        </div>
        """

  html_code = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
      <meta charset="UTF-8">
      <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
      <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
      <style>
        * {{ box-sizing: border-box; font-family: 'Cairo', sans-serif; margin: 0; padding: 0; }}
        body {{ background-color: transparent; color: #FFFFFF; padding: 10px; direction: rtl; text-align: right; }}
        
        #card-container {{
          background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
          border: 2px solid #334155;
          border-radius: 20px;
          padding: 25px;
          max-width: 950px;
          margin: 0 auto;
          box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        .header {{ 
          display: flex; 
          justify-content: space-between; 
          align-items: center; 
          border-bottom: 2px solid #334155; 
          padding-bottom: 15px; 
          margin-bottom: 20px; 
        }}
        .title {{ color: #4DEF8E; font-size: 22px; font-weight: 900; }}
        .admin-box {{
          background: #1E293B;
          border: 1px solid #334155;
          padding: 6px 18px;
          border-radius: 25px;
          font-size: 13px;
          color: #CBD5E1;
        }}
        .grid-container {{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 12px;
        }}
        .member-card {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          background: #1E293B;
          border: 1px solid #334155;
          border-radius: 12px;
          padding: 10px 16px;
        }}
        .rank-1 {{ background: linear-gradient(90deg, #3B270C 0%, #1E293B 100%); border-color: #FFD700; }}
        .rank-2 {{ background: linear-gradient(90deg, #28303D 0%, #1E293B 100%); border-color: #C0C0C0; }}
        .rank-3 {{ background: linear-gradient(90deg, #33221A 0%, #1E293B 100%); border-color: #CD7F32; }}
        
        .right-section {{ display: flex; align-items: center; gap: 10px; }}
        .badge {{
          font-weight: 900;
          font-size: 13px;
          padding: 4px 8px;
          border-radius: 6px;
          background: #334155;
          color: #FFF;
          white-space: nowrap;
        }}
        .b-1 {{ background: #FFD700; color: #000; }}
        .b-2 {{ background: #C0C0C0; color: #000; }}
        .b-3 {{ background: #CD7F32; color: #FFF; }}
        
        .name-box {{ display: flex; flex-direction: column; gap: 2px; }}
        .member-name {{ font-size: 15px; font-weight: 700; color: #F8FAFC; line-height: 1.2; }}
        .role-tag {{ font-size: 10px; padding: 1px 6px; border-radius: 4px; width: fit-content; }}
        .tag-admin {{ background: #0284C7; color: #FFF; }}
        .tag-user {{ background: #334155; color: #94A3B8; }}
        
        .left-section {{ display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }}
        .points {{ color: #4DEF8E; font-weight: 700; font-size: 14px; }}
        .rank-title {{ color: #CBD5E1; font-size: 11px; }}
        
        .btn-container {{ text-align: center; margin-top: 20px; }}
        .dl-btn {{
          background: #4DEF8E;
          color: #0F172A;
          font-weight: 900;
          font-size: 16px;
          border: none;
          padding: 14px 28px;
          border-radius: 12px;
          cursor: pointer;
          box-shadow: 0 4px 15px rgba(77, 239, 142, 0.3);
          width: 100%;
          max-width: 400px;
        }}
        .dl-btn:hover {{ background: #3be07d; }}

        @media (max-width: 600px) {{
          .grid-container {{ grid-template-columns: 1fr; }}
          .header {{ flex-direction: column; gap: 10px; }}
        }}
      </style>
    </head>
    <body>
      <div id="card-container">
        <div class="header">
          <div class="title">✨ حسبة ونقاط نظام Opal's System ✨</div>
          <div class="admin-box">👑 <b>المشرف:</b> Aurther &nbsp;|&nbsp; 🤝 <b>المساعد:</b> Lamino</div>
        </div>
        <div class="grid-container">
            {rows_html}
        </div>
      </div>

      <div class="btn-container">
        <button class="dl-btn" onclick="downloadCard()">📥 اضغط هنا لتحميل بطاقة الصورة (PNG)</button>
      </div>

      <script>
        function downloadCard() {{
          const card = document.getElementById('card-container');
          html2canvas(card, {{
            scale: 2,
            backgroundColor: '#0F172A',
            useCORS: true
          }}).then(canvas => {{
            const link = document.createElement('a');
            link.download = 'opals_leaderboard.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
          }});
        }}
      </script>
    </body>
    </html>
    """
  return html_code


# 5. الواجهة الرئيسية
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

# --- التبويب الأول ---
with tab1:
  conn = get_connection()
  df = pd.read_sql_query(
      "SELECT name, oplz, role FROM members ORDER BY oplz DESC", conn
  )
  conn.close()

  if not df.empty:
    html_content = create_html_card(df)
    card_height = 200 + (math.ceil(len(df) / 2) * 85)
    components.html(html_content, height=card_height, scrolling=True)
  else:
    st.info("💡 لا يوجد أعضاء مسجلين حتى الآن. قم بإضافة النقاط من التبويب الثاني.")

# --- التبويب الثاني ---
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

# --- التبويب الثالث ---
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
    
