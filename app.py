import streamlit as st
from skyfield.api import load
from datetime import datetime

st.set_page_config(page_title="Astro Pro", layout="centered")

# =========================
# SAFE LOAD (FIX)
# =========================
@st.cache_resource
def load_data():
    eph = load('de421.bsp')
    ts = load.timescale()
    return eph, ts

eph, ts = load_data()
earth = eph['earth']

# =========================
# ZODIAC
# =========================
def zodiac(lon):
    signs = ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak",
             "Terazi","Akrep","Yay","Oğlak","Kova","Balık"]
    return signs[int((lon % 360)/30)]

# =========================
# PLANETS (FIXED)
# =========================
def get_positions(year, month, day, hour):

    t = ts.utc(year, month, day, hour)

    bodies = {
        "Güneş": eph['sun'],
        "Ay": eph['moon'],
        "Merkür": eph['mercury'],
        "Venüs": eph['venus'],
        "Mars": eph['mars'],
        "Jüpiter": eph['jupiter barycenter'],
        "Satürn": eph['saturn barycenter']
    }

    result = {}

    for name, body in bodies.items():
        astrometric = earth.at(t).observe(body)
        ecliptic = astrometric.ecliptic_latlon()

        lon = ecliptic[1].degrees  # 🔥 DOĞRU
        result[name] = zodiac(lon)

    return result

# =========================
# ASC (STABLE)
# =========================
def ascendant(hour, lon):
    asc_lon = (hour * 15 + lon) % 360
    return zodiac(asc_lon)

# =========================
# UI
# =========================
st.title("🔮 Profesyonel Astroloji")

col1,col2,col3 = st.columns(3)

with col1:
    day = st.number_input("Gün",1,31)
with col2:
    month = st.number_input("Ay",1,12)
with col3:
    year = st.number_input("Yıl",1900,2026)

hour = st.number_input("Saat",0,23)

# şehir kaldırdık → stabil
lon = 28.9784  # Istanbul sabit

if st.button("✨ Hesapla"):

    try:
        datetime(year, month, day)

        data = get_positions(year, month, day, hour)
        asc = ascendant(hour, lon)

        st.subheader("🪐 Gezegenler")
        for k,v in data.items():
            st.write(f"{k}: {v}")

        st.subheader("🌅 Yükselen")
        st.write(asc)

    except Exception as e:
        st.error("Hata oluştu")
        st.write(e)
