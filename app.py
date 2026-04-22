import streamlit as st
from datetime import datetime
import math

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Astro AI Pro", layout="centered")

# =========================
# CSS (MOBİL TASARIM)
# =========================
st.markdown("""
<style>
.card {
    padding:15px;
    border-radius:20px;
    background:#111;
    color:white;
    margin-bottom:12px;
    box-shadow:0 0 10px rgba(255,255,255,0.1);
}
.title {
    font-size:24px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# ZODIAC
# =========================
def zodiac(lon):
    signs = ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak",
             "Terazi","Akrep","Yay","Oğlak","Kova","Balık"]
    return signs[int((lon % 360) / 30)]

# =========================
# ASTRO ENGINE (STABİL MODEL)
# =========================
def get_planets(day, month, year):
    d = datetime(year, month, day).timetuple().tm_yday

    sun = (d / 365.25) * 360
    moon = (d % 29.53) * 12.2
    mercury = (d % 88) * 4.1
    venus = (d % 225) * 1.6
    mars = (d % 687) * 0.52
    jupiter = (d % 4332) * 0.083
    saturn = (d % 10759) * 0.033

    asc = (sun + moon) % 360

    return {
        "Güneş": zodiac(sun),
        "Ay": zodiac(moon),
        "Merkür": zodiac(mercury),
        "Venüs": zodiac(venus),
        "Mars": zodiac(mars),
        "Jüpiter": zodiac(jupiter),
        "Satürn": zodiac(saturn),
        "Yükselen": zodiac(asc)
    }

# =========================
# AI YORUM MOTORU
# =========================
def ai_comment(p):
    return f"""
☀ {p['Güneş']} burcu → karakterin güçlü ve yön belirleyici.

🌙 {p['Ay']} → duygusal dünyanda derinlik var.

💖 {p['Venüs']} → aşk hayatında yoğun bağlar kurarsın.

🔥 {p['Mars']} → harekete geçme enerjin yüksek.

💼 Kariyer: disiplinli ilerlersen büyük başarı gelir.

⚡ Genel: Hayatında önemli bir dönüşüm dönemindesin.
"""

# =========================
# SESSION
# =========================
if "show" not in st.session_state:
    st.session_state.show = False

# =========================
# UI
# =========================
st.markdown('<div class="title">🔮 Astro AI Pro</div>', unsafe_allow_html=True)

st.markdown('<div class="card">📅 Doğum Bilgileri</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    day = st.number_input("Gün",1,31)

with col2:
    month = st.number_input("Ay",1,12)

with col3:
    year = st.number_input("Yıl",1900,2026)

col4, col5 = st.columns(2)

with col4:
    hour = st.number_input("Saat",0,23)

with col5:
    minute = st.number_input("Dakika",0,59)

# =========================
# BUTTON
# =========================
if st.button("✨ Analiz Et"):
    try:
        datetime(year, month, day)
        st.session_state.show = True
    except:
        st.error("Geçersiz tarih")

# =========================
# RESULT
# =========================
if st.session_state.show:

    planets = get_planets(day, month, year)

    st.markdown('<div class="card">🪐 Gezegenler</div>', unsafe_allow_html=True)
    for k,v in planets.items():
        st.write(f"**{k}:** {v}")

    st.markdown('<div class="card">📅 Günlük Yorum</div>', unsafe_allow_html=True)
    st.write(f"""
Bugün {planets['Güneş']} enerjisi baskın.
{planets['Ay']} etkisi duygularını yönlendiriyor.
{planets['Yükselen']} dış dünyaya yansımanı belirliyor.

Dengeyi korursan fırsatlar seni bulacak.
""")

    st.markdown('<div class="card">🧠 AI Analiz</div>', unsafe_allow_html=True)
    st.write(ai_comment(planets))
