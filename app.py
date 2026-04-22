import streamlit as st
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Astro AI", layout="centered")

API_KEY = "rPj8lg7danUhC74RSavTw2H73peVXx0oT1amRnGq"

# =========================
# CSS (MOBİL)
# =========================
st.markdown("""
<style>
.card {
    padding:15px;
    border-radius:20px;
    background:#111;
    color:white;
    margin-bottom:10px;
}
.title {
    font-size:22px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# AI YORUM
# =========================
def ai_yorum(data):
    sun = data.get("sun", "bilinmiyor")
    moon = data.get("moon", "bilinmiyor")

    return f"""
☀ Güneş {sun} konumunda: güçlü karakter ve yön belirleme.

🌙 Ay {moon} konumunda: duygusal dalgalanmalar ve sezgi yüksek.

❤️ Aşk: yoğun duygular ve bağ kurma isteği artıyor.

💼 Kariyer: fırsatlar var ama sabırlı olmalısın.
"""

# =========================
# UI
# =========================
st.markdown('<div class="title">🔮 Astro AI</div>', unsafe_allow_html=True)

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

city = st.text_input("Şehir (Istanbul önerilir)")

# =========================
# BUTTON
# =========================
if st.button("✨ Analiz Et"):

    url = "https://api.api-ninjas.com/v1/astrology"

    headers = {
        "X-Api-Key": API_KEY
    }

    params = {
        "year": int(year),
        "month": int(month),
        "day": int(day),
        "hour": int(hour),
        "min": int(minute),
        "city": city
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:

        data = response.json()

        st.markdown('<div class="card">🪐 Gezegenler</div>', unsafe_allow_html=True)
        st.json(data)

        st.markdown('<div class="card">🧠 AI Yorum</div>', unsafe_allow_html=True)
        st.write(ai_yorum(data))

    else:
        st.error("API hatası - şehir veya key yanlış olabilir")
