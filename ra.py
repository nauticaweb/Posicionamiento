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

st.header("2. Observaciones")
azimut1 = st.number_input("Azimut 1 (°)", step=1.0, value=0.0)
dh1t = st.number_input("Diferencia de alturas 1", step=0.1, value=0.0)

azimut2 = st.number_input("Azimut 2 (°)", step=1.0, value=0.0)
dh2t = st.number_input("Diferencia de alturas 2", step=0.1, value=0.0)

st.header("3. Desplazamiento")
rumbo = st.number_input("Rumbo (°)", step=1.0, value=0.0)
distancia = st.number_input("Distancia navegada", step=0.1, value=0.0)

# ===================== BOTÓN =====================
if st.button("Calcular"):
    # Convertir coordenadas a decimales
    latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos)
    longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

    # Vector Azimut 1
    az1 = azimut1 + 180 if dh1t < 0 else azimut1
    dh1 = abs(dh1t / np.cos(np.radians(latitud)))
    dx1 = dh1 * np.sin(np.radians(az1))
    dy1 = dh1 * np.cos(np.radians(az1))

    # Vector Azimut 2
    az2 = azimut2 + 180 if dh2t < 0 else azimut2
    dh2 = abs(dh2t / np.cos(np.radians(latitud)))
    dx2 = dh2 * np.sin(np.radians(az2))
    dy2 = dh2 * np.cos(np.radians(az2))

    # Vector Desplazamiento
    desplazamiento = abs(distancia / np.cos(np.radians(latitud)))
    dxD = desplazamiento * np.sin(np.radians(rumbo))
    dyD = desplazamiento * np.cos(np.radians(rumbo))

    # Rectas de altura
    mz1 = dy1 / dx1
    mz2 = dy2 / dx2
    m1 = -1 / mz1
    m2 = -1 / mz2
    b1 = dy1 - m1 * dx1
    b2 = dy2 - m2 * dx2

    # Punto de corte original (posición observada sin desplazamiento)
    x_intersec = (b2 - b1) / (m1 - m2)
    y_intersec = m1 * x_intersec + b1

    # Nueva recta paralela a la recta 1 que pasa por el final de azimut1 + desplazamiento
    dx1D = dx1 + dxD
    dy1D = dy1 + dyD
    b1D = dy1D - m1 * dx1D

    # Nuevo punto de corte (con desplazamiento)
    x_intersec_nueva = (b2 - b1D) / (m1 - m2)
    y_intersec_nueva = m1 * x_intersec_nueva + b1D

    # ===================== RESULTADOS =====================
    st.subheader("4. Resultados")

    # Posición observada original
    y_i = y_intersec * np.cos(np.radians(latitud))
    lat_intersec = latitud + (y_i / 60)
    lon_intersec = longitud - (x_intersec / 60)

    lat_g, lat_m = decimal_a_grados_minutos(lat_intersec)
    lon_g, lon_m = decimal_a_grados_minutos(lon_intersec)
    NS = "N" if lat_intersec > 0 else "S"
    EW = "W" if lon_intersec > 0 else "E"

    st.markdown("**Posición observada (sin desplazamiento):**")
    st.write(f"Latitud: `{lat_intersec:.6f}`")
    st.write(f"Longitud: `{lon_intersec:.6f}`")
    st.write(f"Latitud: `{abs(lat_g)}° {lat_m:.2f}' {NS}`")
    st.write(f"Longitud: `{abs(lon_g)}° {lon_m:.2f}' {EW}`")

    # Posición observada con desplazamiento
    y_i_nueva = y_intersec_nueva * np.cos(np.radians(latitud))
    lat_intersec_nueva = latitud + (y_i_nueva / 60)
    lon_intersec_nueva = longitud - (x_intersec_nueva / 60)

    lat_gn, lat_mn = decimal_a_grados_minutos(lat_intersec_nueva)
    lon_gn, lon_mn = decimal_a_grados_minutos(lon_intersec_nueva)
    NSn = "N" if lat_intersec_nueva > 0 else "S"
    EWn = "W" if lon_intersec_nueva > 0 else "E"

    st.markdown("**Posición observada (con desplazamiento):**")
    st.write(f"Latitud: `{lat_intersec_nueva:.6f}`")
    st.write(f"Longitud: `{lon_intersec_nueva:.6f}`")
    st.write(f"Latitud: `{abs(lat_gn)}° {lat_mn:.2f}' {NSn}`")
    st.write(f"Longitud: `{abs(lon_gn)}° {lon_mn:.2f}' {EWn}`")