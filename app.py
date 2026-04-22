import streamlit as st
from skyfield.api import load
from datetime import datetime

st.set_page_config(page_title="Astro Real", layout="centered")

# =========================
# LOAD DATA
# =========================
planets = load('de421.bsp')
ts = load.timescale()

earth = planets['earth']

# =========================
# ZODIAC
# =========================
def zodiac(lon):
    signs = ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak",
             "Terazi","Akrep","Yay","Oğlak","Kova","Balık"]
    return signs[int((lon % 360)/30)]

# =========================
# PLANETS
# =========================
def get_positions(year, month, day, hour):

    t = ts.utc(year, month, day, hour)

    bodies = {
        "Güneş": planets['sun'],
        "Ay": planets['moon'],
        "Merkür": planets['mercury'],
        "Venüs": planets['venus'],
        "Mars": planets['mars'],
        "Jüpiter": planets['jupiter barycenter'],
        "Satürn": planets['saturn barycenter']
    }

    result = {}

    for name, body in bodies.items():
        astrometric = earth.at(t).observe(body)
        ra, dec, distance = astrometric.radec()

        lon = ra.hours * 15  # approx ecliptic conversion
        result[name] = zodiac(lon)

    return result

# =========================
# UI
# =========================
st.title("🔮 Gerçek Astroloji (NASA Veri)")

col1,col2,col3 = st.columns(3)

with col1:
    day = st.number_input("Gün",1,31)
with col2:
    month = st.number_input("Ay",1,12)
with col3:
    year = st.number_input("Yıl",1900,2026)

hour = st.number_input("Saat",0,23)

if st.button("Hesapla"):

    try:
        datetime(year, month, day)

        data = get_positions(year, month, day, hour)

        st.subheader("🪐 Gezegenler (Gerçek Veri)")
        for k,v in data.items():
            st.write(f"{k}: {v}")

    except:
        st.error("Geçersiz tarih")
