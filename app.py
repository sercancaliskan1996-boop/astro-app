import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Ultimate Astro", layout="centered")

# =========================
# SWISS EPHEMERIS
# =========================
swe.set_ephe_path('.')

# =========================
# ZODIAC
# =========================
def zodiac(lon):
    signs = ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak",
             "Terazi","Akrep","Yay","Oğlak","Kova","Balık"]
    return signs[int(lon/30)]

# =========================
# GEO
# =========================
def get_coords(city):
    try:
        geo = Nominatim(user_agent="astro")
        loc = geo.geocode(city, timeout=10)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass
    return 41.0082, 28.9784

# =========================
# PLANETS (REAL)
# =========================
def get_chart(y, m, d, hour, lat, lon):

    jd = swe.julday(y, m, d, hour)

    planets = {
        "Güneş": swe.SUN,
        "Ay": swe.MOON,
        "Merkür": swe.MERCURY,
        "Venüs": swe.VENUS,
        "Mars": swe.MARS,
        "Jüpiter": swe.JUPITER,
        "Satürn": swe.SATURN
    }

    results = {}
    longitudes = {}

    for name, p in planets.items():
        lon_val = swe.calc_ut(jd, p)[0][0]
        results[name] = zodiac(lon_val)
        longitudes[name] = lon_val

    # ASC + Houses (GERÇEK)
    houses = swe.houses(jd, lat, lon)

    asc = zodiac(houses[0][0])

    return results, longitudes, asc

# =========================
# ASPECTS
# =========================
def aspects(longitudes):
    res = []
    keys = list(longitudes.keys())

    for i in range(len(keys)):
        for j in range(i+1, len(keys)):

            p1 = keys[i]
            p2 = keys[j]

            diff = abs(longitudes[p1] - longitudes[p2])
            diff = min(diff, 360 - diff)

            if abs(diff - 0) < 8:
                res.append(f"{p1} ☌ {p2}")
            elif abs(diff - 90) < 6:
                res.append(f"{p1} □ {p2}")
            elif abs(diff - 120) < 6:
                res.append(f"{p1} △ {p2}")
            elif abs(diff - 180) < 8:
                res.append(f"{p1} ☍ {p2}")

    return res

# =========================
# AI COMMENT
# =========================
def ai(planets, asc):
    return f"""
☀ {planets['Güneş']} → temel karakter

🌙 {planets['Ay']} → duygular

🌅 {asc} → dış görünüm

💖 {planets['Venüs']} → aşk

🔥 {planets['Mars']} → enerji

Hayatında önemli bir dönüşüm sürecindesin.
"""

# =========================
# UI
# =========================
st.title("🔮 Ultimate Astro Engine (Gerçek)")

col1,col2,col3 = st.columns(3)

with col1:
    day = st.number_input("Gün",1,31)
with col2:
    month = st.number_input("Ay",1,12)
with col3:
    year = st.number_input("Yıl",1900,2026)

hour = st.number_input("Saat",0,23)
minute = st.number_input("Dakika",0,59)

city = st.text_input("Şehir", "Istanbul")

if st.button("✨ Hesapla"):

    try:
        datetime(year, month, day)

        hour_decimal = hour + minute/60

        lat, lon = get_coords(city)

        planets, longitudes, asc = get_chart(
            year, month, day, hour_decimal, lat, lon
        )

        st.subheader("🪐 Gezegenler")
        for k,v in planets.items():
            st.write(f"{k}: {v}")

        st.subheader("🌅 Yükselen")
        st.write(asc)

        st.subheader("🔺 Açılar")
        for a in aspects(longitudes):
            st.write(a)

        st.subheader("🧠 Yorum")
        st.write(ai(planets, asc))

    except Exception as e:
        st.error("Hata")
        st.write(e)
