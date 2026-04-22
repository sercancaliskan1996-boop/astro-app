import streamlit as st
import requests

st.title("🔮 Astro Pro API Version")

name = st.text_input("İsim")
date = st.date_input("Doğum Tarihi")
time = st.time_input("Doğum Saati")
city = st.text_input("Şehir")

if st.button("Hesapla"):

    url = "https://api.api-ninjas.com/v1/astrology"
    
    headers = {
        "X-Api-Key": "rPj8lg7danUhC74RSavTw2H73peVXx0oT1amRnGq"
    }

    params = {
        "year": date.year,
        "month": date.month,
        "day": date.day,
        "hour": time.hour,
        "min": time.minute,
        "city": city
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code == 200:
        data = r.json()

        st.subheader("🪐 Gezegenler")
        st.write(data)

    else:
        st.error("API hatası")
