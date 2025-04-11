import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===================== FUNCIONES AUXILIARES =====================
def gms_a_decimal(grados, minutos, segundos):
    if grados < 0:
        grados_dec = grados - (minutos / 60) - (segundos / 3600)
    else:
        grados_dec = grados + (minutos / 60) + (segundos / 3600)
    return grados_dec

def decimal_a_grados_minutos(decimal):
    grados = int(decimal)
    minutos = abs((decimal - grados) * 60)
    return grados, minutos

# ===================== INTERFAZ STREAMLIT =====================
st.title("Cálculo de posición por Rectas de Altura")

st.header("1. Punto de estima (coordenadas)")
col1, col2 = st.columns(2)
with col1:
    lat_grados = st.number_input("Latitud grados", step=1, format="%d", value=0)
    lat_minutos = st.number_input("Latitud minutos", step=1.0, value=0.0)
    lat_segundos = st.number_input("Latitud segundos", step=0.1, value=0.0)
with col2:
    lon_grados = st.number_input("Longitud grados", step=1, format="%d", value=0)
    lon_minutos = st.number_input("Longitud minutos", step=1.0, value=0.0)
    lon_segundos = st.number_input("Longitud segundos", step=0.1, value=0.0)

st.header("2. Observaciones y desplazamiento")
azimut1 = st.number_input("Azimut 1 (grados)", step=1.0, value=0.0)
dh1t = st.number_input("Diferencia de alturas 1", step=0.1, value=0.0)

rumbo = st.number_input("Rumbo del desplazamiento (grados)", step=1.0, value=0.0)
distancia = st.number_input("Distancia recorrida (millas)", step=0.1, value=0.0)

azimut2 = st.number_input("Azimut 2 (grados)", step=1.0, value=0.0)
dh2t = st.number_input("Diferencia de alturas 2", step=0.1, value=0.0)

if st.button