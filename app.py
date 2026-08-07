import math
import sqlite3
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات الصفحة والواجهة بنمط أنمي ساكورا (Bellona Group Theme)
st.set_page_config(
    page_title="BELLONA | نظام نقاط Opal's", page_icon="🌸", layout="centered"
)

# تخصيص التصميم والأنيميشن الخاص بتساقط أوراق الساكورا والألوان الزهرية
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* خلفية الموقع بأسلوب بيبي بينك وأبيض لطيف */
    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF0F5 50%, #FFE4E1 100%);
        direction: rtl;
        text-align: right;
    }

    /* أنيميشن تساقط أوراق الساكورا في خلفية الموقع */
    @keyframes sakura-fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(105vh) rotate(360deg); opacity: 0; }
    }
    
    .sakura-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    .petal {
        position: absolute;
        background: #FFB7C5;
        border-radius: 15px 0px 15px 0px;
        opacity: 0.7;
        animation: sakura-fall 8s linear infinite;
    }
    
    .p1 { left: 10%; width: 12px; height: 16px; animation-duration: 7s; animation-delay: 0s; }
    .p2 { left: 25%; width: 10px; height: 14px; animation-duration: 9s; animation-delay: 2s; background: #FFC0CB; }
    .p3 { left: 40%; width: 15px; height: 18px; animation-duration: 6s; animation-delay: 1s; }
    .p4 { left: 60%; width: 11px; height: 15px; animation-duration: 8s; animation-delay: 3s; background: #FFB6C1; }
    .p5 { left: 75%; width: 14px; height: 17px; animation-duration: 10s; animation-delay: 0.5s; }
    .p6 { left: 90%; width: 9px; height: 13px; animation-duration: 7.5s; animation-delay: 2.5s; }

    /* العناوين والبطاقات */
    .main-title {
        text-align: center;
        color: #D81B60;
        font-weight: 900;
        font-size: 2.3rem;
        margin-bottom: 5px;
        text-shadow: 0px 2px 10px rgba(216, 27, 96, 0.15);
    }
    .bellona-sub {
        text-align: center;
        color: #C2185B;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 15px;
        letter-spacing: 2px;
    }
    .admin-info {
        text-align: center;
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 25px;
        border: 2px solid #FFB7C5;
        box-shadow: 0 4px 15px rgba(255, 183, 197, 0.3);
    }
    .admin-badge {
        display: inline-block;
        margin: 0 10px;
        font-size: 1.05rem;
        color: #880E4F;
        font-weight: 700;
    }
    
    /* تخصيص التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.6);
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #C2185B;
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D81B60 !important;
        color: white !important;
    }
    </style>
    
    <!-- عناصر تساقط الساكورا -->
    <div class="sakura-container">
        <div class="petal p1"></div>
        <div class="petal p2"></div>
        <div class="petal p3"></div>
        <div class="petal p4"></div>
        <div class="petal p5"></div>
        <div class="petal p6"></div>
    </div>
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


# 4. تصميم بطاقة أنمي الساكورا لـ BELLONA GROUP
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
      badge_text = "👑 #1"
    elif rank == 2:
      rank_class = "rank-2"
      badge_class = "b-2"
      badge_text = "🌸 #2"
    elif rank == 3:
      rank_class = "rank-3"
      badge_class = "b-3"
      badge_text = "✨ #3"

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
        body {{ background-color: transparent; color: #4A0E17; padding: 10px; direction: rtl; text-align: right; }}
        
        #card-container {{
          background: linear-gradient(135deg, #FFFFFF 0%, #FFF0F5 50%, #FFE4E1 100%);
          border: 3px solid #FF80AB;
          border-radius: 24px;
          padding: 25px;
          max-width: 950px;
          margin: 0 auto;
          box-shadow: 0 12px 35px rgba(216, 27, 96, 0.15);
          position: relative;
          overflow: hidden;
        }}
        
        /* تأثير أغصان أزهار ساكورا خفيفة على الأطراف */
        #card-container::before {{
          content: '🌸';
          position: absolute;
          top: -10px;
          left: -10px;
          font-size: 70px;
          opacity: 0.2;
        }}
        #card-container::after {{
          content: '🌺';
          position: absolute;
          bottom: -10px;
          right: -10px;
          font-size: 70px;
          opacity: 0.2;
        }}

        .header {{ 
          display: flex; 
          justify-content: space-between; 
          align-items: center; 
          border-bottom: 2px dashed #FFB7C5; 
          padding-bottom: 15px; 
          margin-bottom: 20px; 
        }}
        .logo-title {{
          color: #D81B60;
          font-size: 26px;
          font-weight: 900;
          letter-spacing: 1px;
          text-shadow: 1px 1px 2px rgba(255, 182, 193, 0.5);
        }}
        .sub-logo {{
          font-size: 13px;
          color: #C2185B;
          font-weight: 700;
          display: block;
        }}
        .admin-box {{
          background: #FFFFFF;
          border: 2px solid #FFC1E3;
          padding: 6px 18px;
          border-radius: 25px;
          font-size: 13px;
          color: #880E4F;
          font-weight: 700;
          box-shadow: 0 2px 8px rgba(255, 193, 227, 0.4);
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
          background: rgba(255, 255, 255, 0.9);
          border: 1.5px solid #FFD1DC;
          border-radius: 16px;
          padding: 10px 16px;
          box-shadow: 0 2px 8px rgba(255, 183, 197, 0.2);
        }}
        
        .rank-1 {{ background: linear-gradient(90deg, #FFF8E1 0%, #FFFFFF 100%); border-color: #FFD700; }}
        .rank-2 {{ background: linear-gradient(90deg, #F3E5F5 0%, #FFFFFF 100%); border-color: #CE93D8; }}
        .rank-3 {{ background: linear-gradient(90deg, #FCE4EC 0%, #FFFFFF 100%); border-color: #F48FB1; }}
        
        .right-section {{ display: flex; align-items: center; gap: 10px; }}
        .badge {{
          font-weight: 900;
          font-size: 13px;
          padding: 4px 10px;
          border-radius: 10px;
          background: #FFE4E1;
          color: #C2185B;
          white-space: nowrap;
        }}
        .b-1 {{ background: #FFD700; color: #5D4037; }}
        .b-2 {{ background: #E1BEE7; color: #4A148C; }}
        .b-3 {{ background: #F8BBD0; color: #880E4F; }}
        
        .name-box {{ display: flex; flex-direction: column; gap: 2px; }}
        .member-name {{ font-size: 15px; font-weight: 700; color: #37474F; line-height: 1.2; }}
        .role-tag {{ font-size: 10px; padding: 2px 8px; border-radius: 6px; width: fit-content; font-weight: 700; }}
        .tag-admin {{ background: #EC407A; color: #FFF; }}
        .tag-user {{ background: #F48FB1; color: #FFF; }}
        
        .left-section {{ display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }}
        .points {{ color: #D81B60; font-weight: 900; font-size: 15px; }}
        .rank-title {{ color: #880E4F; font-size: 11px; font-weight: 600; }}
        
        .btn-container {{ text-align: center; margin-top: 22px; }}
        .dl-btn {{
          background: linear-gradient(90deg, #EC407A 0%, #D81B60 100%);
          color: #FFFFFF;
          font-weight: 900;
          font-size: 16px;
          border: none;
          padding: 14px 28px;
          border-radius: 16px;
          cursor: pointer;
          box-shadow: 0 4px 18px rgba(216, 27, 96, 0.35);
          width: 100%;
          max-width: 420px;
          transition: transform 0.2s;
        }}
        .dl-btn:active {{ transform: scale(0.98); }}

        @media (max-width: 600px) {{
          .grid-container {{ grid-template-columns: 1fr; }}
          .header {{ flex-direction: column; gap: 10px; }}
        }}
      </style>
    </head>
    <body>
      <div id="card-container">
        <div class="header">
          <div>
            <div class="logo-title">🌸 BELLONA GROUP 🌸</div>
            <span class="sub-logo">✨ نظام ونقاط أوبلز | Opal's System ✨</span>
          </div>
          <div class="admin-box">👑 <b>المشرف:</b> Aurther &nbsp;|&nbsp; 🤝 <b>المساعد:</b> Lamino</div>
        </div>
        <div class="grid-container">
            {rows_html}
        </div>
      </div>

      <div class="btn-container">
        <button class="dl-btn" onclick="downloadCard()">🌸 تحميل بطاقة BELLONA كصورة (PNG)</button>
      </div>

      <script>
        function downloadCard() {{
          const card = document.getElementById('card-container');
          html2canvas(card, {{
            scale: 2,
            backgroundColor: '#FFFFFF',
            useCORS: true
          }}).then(canvas => {{
            const link = document.createElement('a');
            link.download = 'bellona_opals_leaderboard.png';
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
    '<p class="main-title">🌸 BELLONA GROUP 🌸</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="bellona-sub">✨ نظام وقائمة ترتيب نقاط Opal\'s ✨</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="admin-info">
        <span class="admin-badge">👑 <b>المشرف العام:</b> Aurther</span>
        <span style="color: #FFB7C5;">|</span>
        <span class="admin-badge">🤝 <b>المساعد:</b> Lamino</span>
    </div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs([
    "📸 بطاقة الترتيب (Bellona)",
    "➕ إضافة / تعديل نقاط",
    "⚙️ إدارة الاعضاء",
])

# --- التبويب الأول ---
with tab1:
  conn = get_connection()
  df = pd.read_sql_query(
      "SELECT name, oplz, role FROM members ORDER BY oplz DESC", conn
  )
  conn.close()

  if not df.empty:
    html_content = create_html_card(df)
    card_height = 220 + (math.ceil(len(df) / 2) * 85)
    components.html(html_content, height=card_height, scrolling=True)
  else:
    st.info("💡 لا يوجد أعضاء مسجلين حتى الآن.")

# --- التبويب الثاني ---
with tab2:
  st.subheader("🌸 تسجيل وزيادة النقاط")

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
          
