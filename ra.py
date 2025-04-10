import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===================== FUNCIONES AUXILIARES =====================
# Convierte grados, minutos y segundos a grados decimales
def gms_a_decimal(grados, minutos, segundos):
    if grados < 0:
        grados_dec = grados - (minutos / 60) - (segundos / 3600)
    else:
        grados_dec = grados + (minutos / 60) + (segundos / 3600)
    return grados_dec

# Convierte grados decimales a grados, minutos y décimas de minuto
def decimal_a_grados_minutos(decimales):
    grados = int(decimales)
    minutos = (abs(decimales) - abs(grados)) * 60
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

st.header("2. Observaciones")
azimut1 = st.number_input("Azimut 1 (°)", step=1.0, value=0.0)
dh1t = st.number_input("Diferencia de alturas 1", step=0.1, value=0.0)

rumbo = st.number_input("Rumbo del desplazamiento", step=1.0, value=0.0)
distancia = st.number_input("Distancia recorrida (millones de millas)", step=0.1, value=0.0)

azimut2 = st.number_input("Azimut 2 (°)", step=1.0, value=0.0)
dh2t = st.number_input("Diferencia de alturas 2", step=0.1, value=0.0)

# ===================== CÁLCULO =====================
if st.button("Calcular"):
    # Convertir coordenadas a decimales
    latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos)
    longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

    # Vectores 1 y 2
    az1 = azimut1 + 180 if dh1t < 0 else azimut1
    dh1 = abs(dh1t / np.cos(np.radians(latitud)))
    dx1 = dh1 * np.sin(np.radians(az1))
    dy1 = dh1 * np.cos(np.radians(az1))

    # Rumbo desplazamiento
    dh0 = abs(distancia / np.cos(np.radians(latitud)))
    dx0 = dh0 * np.sin(np.radians(rumbo))
    dy0 = dh0 * np.cos(np.radians(rumbo))

    # Vectores 2
    az2 = azimut2 + 180 if dh2t < 0 else azimut2
    dh2 = abs(dh2t / np.cos(np.radians(latitud)))
    dx2 = dh2 * np.sin(np.radians(az2))
    dy2 = dh2 * np.cos(np.radians(az2))

    # Pendientes de vectores
    mz1 = dy1 / dx1
    mz2 = dy2 / dx2
    m1 = -1 / mz1
    m2 = -1 / mz2
    b1 = dy1 - m1 * dx1
    b2 = dy2 - m2 * dx2

    # Intersección
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
    st.subheader("3. Situación")

    st.markdown("**Coordenadas decimales:**")
    st.write(f"Latitud: `{lat_intersec:.6f}`")
    st.write(f"Longitud: `{lon_intersec:.6f}`")

    st.markdown("**Coordenadas en GMS:**")
    st.write(f"Latitud: `{abs(lat_g)}° {lat_m:.2f}' {NS}`")
    st.write(f"Longitud: `{abs(lon_g)}° {lon_m:.2f}' {EW}`")

    # ===================== DIBUJAR GRÁFICO =====================
# Crear la figura
plt.figure()

# Mantener sistema de coordenadas cuadrado
plt.gca().set_aspect('equal', adjustable='box')

# Dibujar ejes
plt.axhline(0, color='k', linewidth=2)  # Eje X
plt.axvline(0, color='k', linewidth=2)  # Eje Y

# Dibujar vectores desde el origen
plt.plot([0, dx1 - dx0], [0, dy1 - dy0], 'y', linewidth=2)  # Vector 1 en amarillo
plt.plot([dx1 - dx0, dx1], [dy1 - dy0, dy1], 'b', linewidth=2)  # Vector desplazamiento en azul
plt.plot([0, dx2], [0, dy2], 'g', linewidth=2)  # Vector 2 en verde

# Calcular desplazamientos perpendiculares para las rectas de altura
perp_dx1 = dy1
perp_dy1 = -dx1

perp_dx2 = dy2
perp_dy2 = -dx2

# Dibujar rectas de altura en rojo (largas para que se crucen)
plt.plot([dx1 - perp_dx1, dx1 + perp_dx1], [dy1 - perp_dy1, dy1 + perp_dy1], 'r--', linewidth=2)
plt.plot([dx2 - perp_dx2, dx2 + perp_dx2], [dy2 - perp_dy2, dy2 + perp_dy2], 'r--', linewidth=2)

# Marcar el punto de intersección en el gráfico
plt.plot(x_intersec, y_intersec, 'mo', markersize=8)  # Punto morado para la intersección

# Añadir etiqueta con coordenadas geográficas
str_intersec = f"Lat: {lat_intersec:.6f}\nLon: {lon_intersec:.6f}"
plt.text(x_intersec + 1, y_intersec + 1, str_intersec)

# Ajustar límites dinámicamente para mostrar todo el gráfico
lim_x = max([abs(dx1), abs(dx2), abs(perp_dx1), abs(perp_dx2), abs(x_intersec)]) + 5
lim_y = max([abs(dy1), abs(dy2), abs(perp_dy1), abs(perp_dy2), abs(y_intersec)]) + 5
plt.xlim(-lim_x, lim_x)
plt.ylim(-lim_y, lim_y)

# Etiquetas
plt.title("Rectas de Altura")
plt.xlabel("Longitud")
plt.ylabel("Latitud")

# Mostrar gráfico
plt.grid(True)
plt.show()