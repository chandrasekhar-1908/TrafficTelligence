import streamlit as st, joblib, pandas as pd
from datetime import datetime
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[1] / 'models' / 'traffic_model.joblib'

# ----------------------------
# 🚦 App UI (NO BACKGROUND)
# ----------------------------
st.title('🚦 TrafficTelligence')

if not MODEL_PATH.exists():
    st.warning('Train the model first: run `python main.py`')
else:
    model = joblib.load(MODEL_PATH)
    st.subheader('Predict Traffic Volume')

    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", value=datetime(2025, 1, 1).date())
    with col2:
        time = st.time_input("Time", value=datetime(2025, 1, 1, 8).time())

    dt = datetime.combine(date, time)

    weather = st.selectbox('Weather', ['Sunny', 'Cloudy', 'Rainy'])
    temp = st.number_input('Temperature °C', value=25.0)
    precip = st.number_input('Precip mm', value=0.0)
    hol = st.selectbox('Holiday?', [0, 1])
    lanes = st.selectbox('Num lanes', [2, 3, 4])
    speed = st.number_input('Avg Speed km/h', value=40.0)
    school = st.selectbox('Near School Zone?', [0, 1])

    if st.button('Predict'):
        row = pd.DataFrame([{
            'hour': dt.hour,
            'day_of_week': dt.weekday(),
            'month': dt.month,
            'weather': weather,
            'temperature_c': temp,
            'precip_mm': precip,
            'is_holiday': hol,
            'num_lanes': lanes,
            'speed_avg_kmh': speed,
            'near_school_zone': school
        }])
        pred = model.predict(row)[0]
        st.success(f'Estimated Traffic Volume: {int(pred)} vehicles/hour')
