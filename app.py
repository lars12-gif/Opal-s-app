import math
import sqlite3
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 1. كلمة السر الخاصة بالإدارة
ADMIN_PASSWORD = "iraq2026"

# 2. إعدادات الصفحة
st.set_page_config(
    page_title="BELLONA | نظام نقاط Opal's", page_icon="🌸", layout="centered"
)

# 3. محرك الصوت والبارتكلز والتفاعل المباشر عبر components.html
components.html(
    """
    <script>
    (function() {
        const pDoc = window.parent.document;
        
        // إنشاء الصوت برمجياً (UI Pop Sound)
        let audioCtx = null;
        function playPopSound() {
            try {
                if (!audioCtx) {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                }
                if (audioCtx.state === 'suspended') {
                    audioCtx.resume();
                }
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                
                osc.type = 'sine';
                osc.frequency.setValueAtTime(700, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1400, audioCtx.currentTime + 0.08);
                
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.08);
                
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                
                osc.start();
                osc.stop(audioCtx.currentTime + 0.08);
            } catch(e) {}
        }

        // إضافة تأثير البارتكلز الملونة
        if (!window.parent.particleListenerAdded) {
            window.parent.particleListenerAdded = true;
            
            pDoc.addEventListener('click', function(e) {
                playPopSound();
                
                const symbols = ['🌸', '✨', '🌺', '💖', '⭐'];
                for (let i = 0; i < 6; i++) {
                    const particle = pDoc.createElement('div');
                    particle.innerText = symbols[Math.floor(Math.random() * symbols.length)];
                    
                    particle.style.position = 'fixed';
                    particle.style.pointerEvents = 'none';
                    particle.style.zIndex = '999999';
                    particle.style.fontSize = '20px';
                    particle.style.left = e.clientX + 'px';
                    particle.style.top = e.clientY + 'px';
                    particle.style.transition = 'all 0.6s cubic-bezier(0.1, 0.8, 0.3, 1)';
                    particle.style.opacity = '1';
                    
                    pDoc.body.appendChild(particle);
                    
                    const dx = (Math.random() - 0.5) * 140;
                    const dy = (Math.random() - 0.5) * 140 - 20;
                    const rot = (Math.random() - 0.5) * 360;
                    
                    requestAnimationFrame(() => {
                        particle.style.transform = `translate(${dx}px, ${dy}px) rotate(${rot}deg) scale(1.3)`;
                        particle.style.opacity = '0';
                    });
                    
                    setTimeout(() => particle.remove(), 650);
                }
            });
        }
    })();
    </script>
""",
    height=0,
)

# 4. تنسيقات الـ CSS وتصاميم الواجهة الخرافية
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }

    /* خلفية الموقع بأسلوب بيبي بينك مريح */
    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF0F5 50%, #FFE4E1 100%) !important;
        direction: rtl;
        text-align: right;
    }

    /* أنيميشن تساقط أوراق الساكورا */
    @keyframes sakura-fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0.9; }
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
    
    .p1 { left: 8%; width: 14px; height: 18px; animation-duration: 7s; animation-delay: 0s; }
    .p2 { left: 22%; width: 10px; height: 14px; animation-duration: 9s; animation-delay: 2s; background: #FFC0CB; }
    .p3 { left: 45%; width: 16px; height: 20px; animation-duration: 6.5s; animation-delay: 1s; }
    .p4 { left: 68%; width: 12px; height: 15px; animation-duration: 8.5s; animation-delay: 3s; background: #FFB6C1; }
    .p5 { left: 85%; width: 15px; height: 18px; animation-duration: 10s; animation-delay: 0.5s; }

    /* العناوين والبطاقات الرئيسية */
    .main-title {
        text-align: center;
        color: #D81B60;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 2px;
        text-shadow: 0px 3px 12px rgba(216, 27, 96, 0.2);
    }
    .bellona-sub {
        text-align: center;
        color: #C2185B;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }
    .admin-info {
        text-align: center;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 12px;
        margin-bottom: 25px;
        border: 2px solid #FFB7C5;
        box-shadow: 0 6px 20px rgba(255, 183, 197, 0.35);
    }
    .admin-badge {
        display: inline-block;
        margin: 0 10px;
        font-size: 1.05rem;
        color: #880E4F;
        font-weight: 800;
    }

    /* 🌸 خلفيات وقوائم التبويبات الفخمة 🌸 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        background: #FFE4E1 !important;
        padding: 12px 14px !important;
        border-radius: 22px !important;
        border: 2px solid #FF80AB !important;
        box-shadow: 0 8px 25px rgba(216, 27, 96, 0.15) !important;
        justify-content: center !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 14px !important;
        background-color: #FFFFFF !important;
        color: #C2185B !important;
        font-weight: 800 !important;
        border: 2px solid #FFC1E3 !important;
        padding: 10px 22px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.25s ease-in-out !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #FFF0F5 !important;
        border-color: #D81B60 !important;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #D81B60 !important;
        box-shadow: 0 6px 18px rgba(216, 27, 96, 0.4) !important;
        transform: translateY(-2px);
    }

    /* خلفية كارت بيضاء بارزة لمحتوى كل تبويب لمنع أي شكل نشاز */
    div[data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #FFC1E3 !important;
        border-radius: 24px !important;
        padding: 25px !important;
        margin-top: 15px !important;
        box-shadow: 0 10px 30px rgba(216, 27, 96, 0.1) !important;
    }
    </style>
    
    <!-- عناصر تساقط الساكورا -->
    <div class="sakura-container">
        <div class="petal p1"></div>
        <div class="petal p2"></div>
        <div class="petal p3"></div>
        <div class="petal p4"></div>
        <div class="petal p5"></div>
    </div>
""",
    unsafe_allow_html=True,
)

# 5. إدارة قاعدة البيانات
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


# 6. حساب الرتب
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


# 7. تصميم بطاقات الترتيب
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
          background: rgba(255, 255, 255, 0.95);
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
        }}
        .b-1 {{ background: #FFD700; color: #5D4037; }}
        .b-2 {{ background: #E1BEE7; color: #4A148C; }}
        .b-3 {{ background: #F8BBD0; color: #880E4F; }}
        
        .name-box {{ display: flex; flex-direction: column; gap: 2px; }}
        .member-name {{ font-size: 15px; font-weight: 700; color: #37474F; }}
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
        }}

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
          html2canvas(card, {{ scale: 2, backgroundColor: '#FFFFFF', useCORS: true }}).then(canvas => {{
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


# 8. الواجهة الرئيسية
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
    "⚙️ إدارة الأعضاء",
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

  pwd_tab2 = st.text_input(
      "🔑 أدخل كلمة سر الإدارة للتعديل:", type="password", key="pwd_tab2"
  )

  if pwd_tab2 == ADMIN_PASSWORD:
    st.success("🔓 تم التحقق بنجاح! يمكنك الآن تسجيل النقاط.")

    mode = st.radio(
        "طريقة الإضافة:",
        [
            "إضافة Opal's مباشرة 💎",
            "تحويل نقاط تفاعل (كل 50 نقطة = 1 Opal's) 🪙",
        ],
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
  else:
    if pwd_tab2:
      st.error("❌ كلمة السر غير صحيحة!")
    else:
      st.warning(
          "🔒 هذه المنطقة محمية. يرجى إدخال كلمة سر الإدارة للوصول لخيار"
          " الإضافة."
      )

# --- التبويب الثالث ---
with tab3:
  st.subheader("⚙️ إدارة وتعديل حسابات الأعضاء")

  pwd_tab3 = st.text_input(
      "🔑 أدخل كلمة سر الإدارة للتعديل:", type="password", key="pwd_tab3"
  )

  if pwd_tab3 == ADMIN_PASSWORD:
    st.success("🔓 تم التحقق بنجاح!")

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
              "UPDATE members SET oplz = ? WHERE name = ?",
              (new_val, selected),
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
    else:
      st.info("💡 لا يوجد أعضاء مسجلين للحذف أو التعديل.")
  else:
    if pwd_tab3:
     
