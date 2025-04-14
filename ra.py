import streamlit as st import numpy as np import matplotlib.pyplot as plt

===================== FUNCIONES =====================

def gms_a_decimal(grados, minutos, segundos): if grados < 0: return grados - (minutos / 60) - (segundos / 3600) else: return grados + (minutos / 60) + (segundos / 3600)

def decimal_a_grados_minutos(decimales): grados = int(decimales) minutos = (abs(decimales) - abs(grados)) * 60 return grados, minutos

==================== INTERFAZ =====================

st.title("Cálculo de posición por Rectas de Altura")

st.header("1. Punto de estima (coordenadas)") col1, col2 = st.columns(2) with col1: lat_grados = st.number_input("Latitud grados", step=1, format="%d", value=0) lat_minutos = st.number_input("Latitud minutos", step=1.0, value=0.0) lat_segundos = st.number_input("Latitud segundos", step=0.1, value=0.0) with col2: lon_grados = st.number_input("Longitud grados", step=1, format="%d", value=0) lon_minutos = st.number_input("Longitud minutos", step=1.0, value=0.0) lon_segundos = st.number_input("Longitud segundos", step=0.1, value=0.0)

st.header("2. Observaciones") azimut1 = st.number_input("Azimut 1 (°)", step=1.0, value=0.0) dh1t = st.number_input("Diferencia de alturas 1", step=0.1, value=0.0)

azimut2 = st.number_input("Azimut 2 (°)", step=1.0, value=0.0) dh2t = st.number_input("Diferencia de alturas 2", step=0.1, value=0.0)

rumbo = st.number_input("Rumbo de desplazamiento (°)", step=1.0, value=0.0) distancia = st.number_input("Distancia navegada", step=0.1, value=0.0)

===================== BOTÓN =====================

if st.button("Calcular"): # Convertir coordenadas a decimales latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos) longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

# Vector 1
az1 = azimut1 + 180 if dh1t < 0 else azimut1
dh1 = abs(dh1t / np.cos(np.radians(latitud)))
dx1 = dh1 * np.sin(np.radians(az1))
dy1 = dh1 * np.cos(np.radians(az1))

# Vector 2
az2 = azimut2 + 180 if dh2t < 0 else azimut2
dh2 = abs(dh2t / np.cos(np.radians(latitud)))
dx2 = dh2 * np.sin(np.radians(az2))
dy2 = dh2 * np.cos(np.radians(az2))

# Vector desplazamiento
desp = abs(distancia / np.cos(np.radians(latitud)))
dx_desp = desp * np.sin(np.radians(rumbo))
dy_desp = desp * np.cos(np.radians(rumbo))

# Pendientes y rectas de altura originales
mz1 = dy1 / dx1
mz2 = dy2 / dx2
m1 = -1 / mz1
m2 = -1 / mz2
b1 = dy1 - m1 * dx1
b2 = dy2 - m2 * dx2

# Punto de intersección original
x_intersec = (b2 - b1) / (m1 - m2)
y_intersec = m1 * x_intersec + b1

# Posición observada original
y_i = y_intersec * np.cos(np.radians(latitud))
lat_intersec = latitud + (y_i / 60)
lon_intersec = longitud - (x_intersec / 60)

lat_g, lat_m = decimal_a_grados_minutos(lat_intersec)
lon_g, lon_m = decimal_a_grados_minutos(lon_intersec)
NS = "N" if lat_intersec > 0 else "S"
EW = "W" if lon_intersec > 0 else "E"

# Nueva recta desplazada (paralela a la 1)
dx1_total = dx1 + dx_desp
dy1_total = dy1 + dy_desp
b1_desp = dy1_total - m1 * dx1_total

# Nuevo punto de intersección
x_intersec_desp = (b2 - b1_desp) / (m1 - m2)
y_intersec_desp = m1 * x_intersec_desp + b1_desp

y_i_desp = y_intersec_desp * np.cos(np.radians(latitud))
lat_intersec_desp = latitud + (y_i_desp / 60)
lon_intersec_desp = longitud - (x_intersec_desp / 60)

lat_g_desp, lat_m_desp = decimal_a_grados_minutos(lat_intersec_desp)
lon_g_desp, lon_m_desp = decimal_a_grados_minutos(lon_intersec_desp)
NS_desp = "N" if lat_intersec_desp > 0 else "S"
EW_desp = "W" if lon_intersec_desp > 0 else "E"

# ===================== RESULTADOS =====================
st.subheader("3. Situación (posición observada sin desplazamiento)")
st.markdown("**Coordenadas decimales:**")
st.write(f"Latitud: `{lat_intersec:.6f}`")
st.write(f"Longitud: `{lon_intersec:.6f}`")

st.markdown("**Coordenadas en GMS:**")
st.write(f"Latitud: `{abs(lat_g)}° {lat_m:.2f}' {NS}`")
st.write(f"Longitud: `{abs(lon_g)}° {lon_m:.2f}' {EW}`")

st.subheader("4. Situación corregida (posición observada con desplazamiento)")
st.markdown("**Coordenadas decimales:**")
st.write(f"Latitud: `{lat_intersec_desp:.6f}`")
st.write(f"Longitud: `{lon_intersec_desp:.6f}`")

st.markdown("**Coordenadas en GMS:**")
st.write(f"Latitud: `{abs(lat_g_desp)}° {lat_m_desp:.2f}' {NS_desp}`")
st.write(f"Longitud: `{abs(lon_g_desp)}° {lon_m_desp:.2f}' {EW_desp}`")

