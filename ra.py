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

# Añadir desplazamiento
st.header("3. Desplazamiento")
azimut3 = st.number_input("Rumbo (azimut 3)", step=1.0, value=0.0)
dh3t = st.number_input("Distancia navegada", step=0.1, value=0.0)

# ===================== BOTÓN =====================
if st.button("Calcular"):
    # Convertir coordenadas a decimales
    latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos)
    longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

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

    # Vector 3 (desplazamiento)
    az3 = azimut3 + 180 if dh3t < 0 else azimut3
    dh3 = abs(dh3t / np.cos(np.radians(latitud)))
    dx3 = dh3 * np.sin(np.radians(az3))
    dy3 = dh3 * np.cos(np.radians(az3))

    # Sumar desplazamiento al vector 1
    dx1_total = dx1 + dx3
    dy1_total = dy1 + dy3

    # Cálculo de la pendiente para la recta de altura del azimut 1
    mz1 = dy1 / dx1
    m1 = -1 / mz1
    b1 = dy1 - m1 * dx1  # Esta recta de altura debe pasar por el final del azimut 1, no por el 0,0

    # Cálculo de la pendiente para la recta de altura del azimut 2
    mz2 = dy2 / dx2
    m2 = -1 / mz2
    b2 = dy2 - m2 * dx2  # Recta de altura 2

    # Cálculo del punto de intersección de las rectas
    x_intersec = (b2 - b1) / (m1 - m2)
    y_intersec = m1 * x_intersec + b1

    # Coordenadas geográficas
    y_i = y_intersec * np.cos(np.radians(latitud))
    lat_intersec = latitud + (y_i / 60)
    lon_intersec = longitud - (x_intersec / 60)

    # Convertir a grados y minutos
    lat_g, lat_m = decimal_a_grados_minutos(lat_intersec)
    lon_g, lon_m = decimal_a_grados_minutos(lon_intersec)
    NS = "N" if lat_intersec > 0 else "S"
    EW = "W" if lon_intersec > 0 else "E"

    # ===================== RESULTADOS =====================
    st.subheader("4. Situación")

    st.markdown("**Coordenadas decimales:**")
    st.write(f"Latitud: `{lat_intersec:.6f}`")
    st.write(f"Longitud: `{lon_intersec:.6f}`")

    st.markdown("**Coordenadas en GMS:**")
    st.write(f"Latitud: `{abs(lat_g)}° {lat_m:.2f}' {NS}`")
    st.write(f"Longitud: `{abs(lon_g)}° {lon_m:.2f}' {EW}`")

    # ===================== GRÁFICO =====================
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    # Dibujar los vectores
    ax.plot([0, dx3], [0, dy3], 'orange', linewidth=2, label="Desplazamiento")
    ax.plot([0, dx1_total], [0, dy1_total], 'b', linewidth=2, label="Azimut 1 + Desplazamiento")
    ax.plot([0, dx2], [0, dy2], 'g', linewidth=2, label="Azimut 2")

    # Rectas de altura (perpendiculares)
    ax.plot([dx1 - dy1, dx1 + dy1], [dy1 + dx1, dy1 - dx1], 'r--', linewidth=2)
    ax.plot([dx2 - dy2, dx2 + dy2], [dy2 + dx2, dy2 - dx2], 'r--', linewidth=2)

    # Punto de intersección
    ax.plot(x_intersec, y_intersec, 'mo', markersize=10)
    ax.text(x_intersec + 0.5, y_intersec + 0.5,
            f"Lat: {lat_intersec:.6f}\nLon: {lon_intersec:.6f}", fontsize=12)

    # Ajustes de gráfico
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_title("Rectas de Altura")
    ax.grid(True)

    st.pyplot(fig)