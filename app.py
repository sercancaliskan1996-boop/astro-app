import streamlit as st
import sqlite3
import hashlib
from datetime import date
from geopy.geocoders import Nominatim
import math

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Astro App", layout="centered")

# =========================
# DATABASE
# =========================
conn = sqlite3.connect('astro.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    premium INTEGER DEFAULT 0
)
''')
conn.commit()

# =========================
# SECURITY
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# AUTH
# =========================
def register(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?,?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def login(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

# =========================
# GEO
# =========================
def get_coordinates(city):
    try:
        geolocator = Nominatim(user_agent="astro_app")
        loc = geolocator.geocode(city)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass
    return None, None

# =========================
# UTILS
# =========================
def day_of_year(d, m, y):
    return (date(y, m, d) - date(y, 1, 1)).days + 1

def zodiac_sign(lon):
    signs = [
        "Koç","Boğa","İkizler","Yengeç","Aslan","Başak",
        "Terazi","Akrep","Yay","Oğlak","Kova","Balık"
    ]
    return signs[int((lon % 360) / 30)]

# =========================
# ASTRO ENGINE
# =========================
def get_planets(day, month, year):
    doy = day_of_year(day, month, year)

    sun = (doy / 365.25) * 360
    moon = (doy % 29.53) / 29.53 * 360
    mercury = (doy % 88) / 88 * 360
    venus = (doy % 225) / 225 * 360
    mars = (doy % 687) / 687 * 360
    jupiter = (doy % 4332) / 4332 * 360
    saturn = (doy % 10759) / 10759 * 360

    asc = (sun + moon) % 360

    return {
        "Güneş": zodiac_sign(sun),
        "Ay": zodiac_sign(moon),
        "Merkür": zodiac_sign(mercury),
        "Venüs": zodiac_sign(venus),
        "Mars": zodiac_sign(mars),
        "Jüpiter": zodiac_sign(jupiter),
        "Satürn": zodiac_sign(saturn),
        "Yükselen": zodiac_sign(asc)
    }

# =========================
# COMMENTS
# =========================
def daily_comment(planets):
    return f"""
☀ Güneş: {planets['Güneş']}
🌙 Ay: {planets['Ay']}
🌅 Yükselen: {planets['Yükselen']}

Bugün enerjin Güneş ve Ay kombinasyonuna göre şekilleniyor.
İlişkilerde (Venüs) ve iletişimde (Merkür) dikkatli ol.
Yeni fırsatlar kapıda olabilir.
"""

def ai_comment(planets):
    return f"""
✨ {planets['Güneş']} burcu güçlü bir karakter verir.
🌙 {planets['Ay']} duygusal dünyanı etkiler.
💖 {planets['Venüs']} aşk hayatını belirler.

Genel olarak değişim ve farkındalık sürecindesin.
"""

# =========================
# SESSION STATE FIX
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_result" not in st.session_state:
    st.session_state.show_result = False

# =========================
# MENU
# =========================
menu = st.sidebar.selectbox("Menü", ["Kayıt", "Giriş", "Uygulama"])

# =========================
# REGISTER
# =========================
if menu == "Kayıt":
    st.subheader("Kayıt Ol")
    u = st.text_input("Kullanıcı adı")
    p = st.text_input("Şifre", type="password")

    if st.button("Kayıt"):
        if register(u, p):
            st.success("Kayıt başarılı")
        else:
            st.error("Kullanıcı zaten var")

# =========================
# LOGIN
# =========================
elif menu == "Giriş":
    st.subheader("Giriş Yap")
    u = st.text_input("Kullanıcı adı")
    p = st.text_input("Şifre", type="password")

    if st.button("Giriş"):
        user = login(u, p)
        if user:
            st.session_state.logged_in = True
            st.success("Giriş başarılı")
        else:
            st.error("Hatalı giriş")

# =========================
# APP
# =========================
elif menu == "Uygulama":

    if not st.session_state.logged_in:
        st.warning("Önce giriş yap")
    else:
        st.subheader("Doğum Haritası")

        col1, col2, col3 = st.columns(3)

        with col1:
            day = st.number_input("Gün", 1, 31)
        with col2:
            month = st.number_input("Ay", 1, 12)
        with col3:
            year = st.number_input("Yıl", 1900, 2026)

        city = st.text_input("Doğum Şehri")

        if st.button("Harita Oluştur"):
            st.session_state.show_result = True

        # ✅ STABİL SONUÇ BLOĞU
        if st.session_state.show_result:

            lat, lon = get_coordinates(city)

            if not lat:
                st.error("Şehir bulunamadı")
            else:
                planets = get_planets(day, month, year)

                st.subheader("🪐 Gezegenler")
                for k, v in planets.items():
                    st.write(f"{k}: {v}")

                st.subheader("📅 Günlük Yorum")
                st.write(daily_comment(planets))

                st.subheader("🧠 AI Yorum")
                st.write(ai_comment(planets))
