import streamlit as st
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Astro Mobile", layout="centered")

# =========================
# CSS (MOBİL TASARIM)
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}
.card {
    padding: 15px;
    border-radius: 20px;
    background: #111;
    color: white;
    box-shadow: 0 0 15px rgba(255,255,255,0.1);
    margin-bottom: 15px;
}
.title {
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# OFFLINE CITY
# =========================
cities = {
    "Istanbul": (41.0082, 28.9784),
    "Ankara": (39.9334, 32.8597),
    "Izmir": (38.4237, 27.1428),
    "Bursa": (40.1885, 29.0610),
    "Antalya": (36.8969, 30.7133),
}

# =========================
# ZODIAC
# =========================
def zodiac(lon):
    signs = ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak",
             "Terazi","Akrep","Yay","Oğlak","Kova","Balık"]
    return signs[int((lon % 360)/30)]

# =========================
# BASİT ASTRO ENGINE (STABİL)
# =========================
def planets(day, month, year):
    d = datetime(year, month, day).timetuple().tm_yday

    return {
        "Güneş": zodiac((d/365)*360),
        "Ay": zodiac((d%29)*12),
        "Merkür": zodiac((d%88)*4),
        "Venüs": zodiac((d%225)*1.6),
        "Mars": zodiac((d%687)*0.5),
        "Jüpiter": zodiac((d%4332)*0.08),
        "Satürn": zodiac((d%10759)*0.03),
        "Yükselen": zodiac((d*2)%360)
    }

# =========================
# SESSION
# =========================
if "show" not in st.session_state:
    st.session_state.show = False

# =========================
# UI
# =========================
st.markdown('<div class="title">🔮 Astro Mobile</div>', unsafe_allow_html=True)

st.markdown('<div class="card">📅 Doğum Bilgileri</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    day = st.number_input("Gün", 1, 31)

with col2:
    month = st.number_input("Ay", 1, 12)

with col3:
    year = st.number_input("Yıl", 1900, 2026)

col4, col5 = st.columns(2)

with col4:
    hour = st.number_input("Saat", 0, 23)

with col5:
    minute = st.number_input("Dakika", 0, 59)

city = st.selectbox("Şehir", list(cities.keys()))

# =========================
# BUTTON
# =========================
if st.button("✨ Haritayı Oluştur"):
    try:
        datetime(year, month, day)
        st.session_state.show = True
    except:
        st.error("Geçersiz tarih")

# =========================
# RESULT
# =========================
if st.session_state.show:

    data = planets(day, month, year)

    st.markdown('<div class="card">🪐 Gezegenler</div>', unsafe_allow_html=True)

    for k, v in data.items():
        st.write(f"**{k}:** {v}")

    st.markdown('<div class="card">📅 Günlük Yorum</div>', unsafe_allow_html=True)

    st.write(f"""
Bugün {data['Güneş']} enerjisi baskın.
{data['Ay']} etkisi duygularını yönlendiriyor.
{data['Yükselen']} dış dünyaya yansımanı belirliyor.

İlişkilerde ve kariyerde dengeli olman gereken bir gün.
""")

    st.markdown('<div class="card">🧠 Genel Analiz</div>', unsafe_allow_html=True)

    st.write(f"""
{data['Güneş']} karakterini oluşturur.
{data['Ay']} iç dünyanı temsil eder.
{data['Venüs']} aşk hayatını etkiler.

Bugün içsel farkındalık kazanma zamanı.
""")
