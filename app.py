import streamlit as st
from skyfield.api import load
from geopy.geocoders import Nominatim
from datetime import datetime
import math

st.set_page_config(page_title="Astro Pro", layout="centered")

# =========================
# LOAD NASA DATA
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
# GEO
# =========================
def get_coords(city):
    try:
        geo = Nominatim(user_agent="astro_pro")
        loc = geo.geocode(city, timeout=10)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass
    return 41.0082, 28.9784  # default Istanbul

# =========================
# PLANET POSITIONS
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

        lon = ra.hours * 15
        result[name] = zodiac(lon)

    return result

# =========================
# ASC (YÜKSELEN)
# =========================
def ascendant(lat, lon, hour):
    # basit sidereal yaklaşım
    asc_lon = (hour * 15 + lon) % 360
    return zodiac(asc_lon)

# =========================
# HOUSE SYSTEM (BASİT)
# =========================
def houses(asc_sign):
    signs = ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak",
             "Terazi","Akrep","Yay","Oğlak","Kova","Balık"]

    index = signs.index(asc_sign)

    return {f"{i+1}. Ev": signs[(index+i)%12] for i in range(12)}

# =========================
# AI YORUM
# =========================
def ai_comment(planets, asc):
    return f"""
☀ Güneş {planets['Güneş']} → karakterin güçlü.

🌙 Ay {planets['Ay']} → duygusal derinlik yüksek.

🌅 Yükselen {asc} → dış dünyaya verdiğin izlenim.

💖 Venüs {planets['Venüs']} → aşk tarzın belirgin.

🔥 Mars {planets['Mars']} → hareket enerjin yüksek.

Genel olarak güçlü bir dönüşüm dönemindesin.
"""

# =========================
# UI
# =========================
st.title("🔮 Profesyonel Astroloji Sistemi")

col1,col2,col3 = st.columns(3)

with col1:
    day = st.number_input("Gün",1,31)
with col2:
    month = st.number_input("Ay",1,12)
with col3:
    year = st.number_input("Yıl",1900,2026)

hour = st.number_input("Saat",0,23)
city = st.text_input("Şehir (Istanbul yaz önerilir)", "Istanbul")

# =========================
# RUN
# =========================
if st.button("✨ Doğum Haritası"):

    try:
        datetime(year, month, day)

        lat, lon = get_coords(city)

        planets_data = get_positions(year, month, day, hour)
        asc = ascendant(lat, lon, hour)
        house_data = houses(asc)

        st.subheader("🪐 Gezegenler")
        for k,v in planets_data.items():
            st.write(f"{k}: {v}")

        st.subheader("🌅 Yükselen")
        st.write(asc)

        st.subheader("🏠 Evler")
        for k,v in house_data.items():
            st.write(f"{k}: {v}")

        st.subheader("🧠 AI Analiz")
        st.write(ai_comment(planets_data, asc))

    except:
        st.error("Geçersiz tarih")
