import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===================== FUNCIONES =====================
def gms_a_decimal(grados, minutos, segundos):
    if grados < 0:
        return grados - (minutos / 60) - (segundos / 3600)
    else:
        return grados + (minutos / 60) + (segundos / 3600)

def decimal_a_grados_minutos(decimales):
    grados = int(decimales)
    minutos = (abs(decimales) - abs(grados)) * 60
    return grados, minutos

# ==================== INTERFAZ =====================
st.title("Cálculo de posición por Rectas de Altura")

st.header("1. Punto de estima")
col1, col2 = st.columns(2)
with col1:
    lat_grados = st.number_input("Latitud grados", step=1, format="%d", value=0)
    lat_minutos = st.number_input("Latitud minutos", step=1.0, value=0.0)
    lat_segundos = st.number_input("Latitud segundos", step=0.1, value=0.0)
with col2:
    lon_grados = st.number_input("Longitud grados", step=1, format="%d", value=0)
    lon_minutos = st.number_input("Longitud minutos", step=1.0, value=0.0)
    lon_segundos = st.number_input("Longitud segundos", step=0.1, value=0.0)

st.header("2. Observaciones")
azimut1 = st.number_input("Azimut 1 (grados)", step=1.0, value=0.0)
dh1t = st.number_input("Diferencia de alturas 1", step=0.1, value=0.0)

azimut2 = st.number_input("Azimut 2 (grados)", step=1.0, value=0.0)
dh2t = st.number_input("Diferencia de alturas 2", step=0.1, value=0.0)

st.header("3. Desplazamiento")
rumbo = st.number_input("Rumbo (grados)", step=1.0, value=0.0)
distancia = st.number_input("Distancia navegada", step=0.1, value=0.0)

# ===================== BOTÓN =====================
if st.button("Calcular"):
    # Convertir coordenadas a decimales
    latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos)
    longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

    # ================== VECTORES ==================
    # Vector 1 (azimut 1)
    az1 = azimut1 + 180 if dh1t < 0 else azimut1
    dh1 = abs(dh1t / np.cos(np.radians(latitud)))
    dx1 = dh1 * np.sin(np.radians(az1))
    dy1 = dh1 * np.cos(np.radians(az1))

    # Vector 2 (azimut 2)
    az2 = azimut2 + 180 if dh2t < 0 else azimut2