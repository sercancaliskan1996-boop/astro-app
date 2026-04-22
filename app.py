import streamlit as st
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from datetime import datetime

st.set_page_config(page_title="Astro Pro Max", layout="centered")

# =========================
# LOAD DATA (CACHE)
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
    return signs[int((lon % 360) / 30)]

# =========================
# PLANETS (GERÇEK)
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
    longitudes = {}

    for name, body in bodies.items():
        astrometric = earth.at(t).observe(body)

        lat, lon, distance = astrometric.frame_latlon(ecliptic_frame)

        lon_deg = lon.degrees
        result[name] = zodiac(lon_deg)
        longitudes[name] = lon_deg

    return result, longitudes

# =========================
# ASC (YAKLAŞIM)
# =========================
def ascendant(hour, lon):
    asc_lon = (hour * 15 + lon) % 360
    return zodiac(asc_lon)

# =========================
# EVLER
# =========================
def houses(asc_sign):
    signs = ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak",
             "Terazi","Akrep","Yay","Oğlak","Kova","Balık"]

    index = signs.index(asc_sign)

    return {f"{i+1}. Ev": signs[(index+i)%12] for i in range(12)}

# =========================
# AÇILAR (ASPECTS)
# =========================
def calculate_aspects(longitudes):
    aspects = []
    names = list(longitudes.keys())

    for i in range(len(names)):
        for j in range(i+1, len(names)):

            p1 = names[i]
            p2 = names[j]

            diff = abs(longitudes[p1] - longitudes[p2])
            diff = min(diff, 360 - diff)

            if abs(diff - 0) < 8:
                aspects.append(f"{p1} ☌ {p2} (Kavuşum)")
            elif abs(diff - 60) < 6:
                aspects.append(f"{p1} ⚹ {p2} (Sextile)")
            elif abs(diff - 90) < 6:
                aspects.append(f"{p1} □ {p2} (Kare)")
            elif abs(diff - 120) < 6:
                aspects.append(f"{p1} △ {p2} (Üçgen)")
            elif abs(diff - 180) < 8:
                aspects.append(f"{p1} ☍ {p2} (Karşıt)")

    return aspects

# =========================
# AI YORUM
# =========================
def ai_comment(planets, asc, aspects):
    return f"""
☀ Güneş {planets['Güneş']} → karakterin.

🌙 Ay {planets['Ay']} → duyguların.

🌅 Yükselen {asc} → dış dünyaya yansıman.

💖 Venüs {planets['Venüs']} → aşk tarzın.

🔥 Mars {planets['Mars']} → motivasyonun.

🔺 Açılar:
{', '.join(aspects[:5]) if aspects else 'Belirgin açı yok'}

Genel olarak güçlü bir dönüşüm sürecindesin.
"""

# =========================
# UI
# =========================
st.title("🔮 Astro Pro Max")

col1, col2, col3 = st.columns(3)

with col1:
    day = st.number_input("Gün", 1, 31)

with col2:
    month = st.number_input("Ay", 1, 12)

with col3:
    year = st.number_input("Yıl", 1900, 2026)

hour = st.number_input("Saat", 0, 23)

# stabil için sabit longitude (İstanbul)
lon = 28.9784

# =========================
# RUN
# =========================
if st.button("✨ Doğum Haritası Oluştur"):

    try:
        datetime(year, month, day)

        planets_data, longitudes = get_positions(year, month, day, hour)

        asc = ascendant(hour, lon)
        house_data = houses(asc)
        aspects = calculate_aspects(longitudes)

        st.subheader("🪐 Gezegenler")
        for k, v in planets_data.items():
            st.write(f"{k}: {v}")

        st.subheader("🌅 Yükselen")
        st.write(asc)

        st.subheader("🏠 Evler")
        for k, v in house_data.items():
            st.write(f"{k}: {v}")

        st.subheader("🔺 Açılar")
        for a in aspects:
            st.write(a)

        st.subheader("🧠 AI Analiz")
        st.write(ai_comment(planets_data, asc, aspects))

    except Exception as e:
        st.error("Hata oluştu")
        st.write(e)
