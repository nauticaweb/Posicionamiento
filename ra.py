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

def dibujar_perpendicular(ax, x, y, azimut, largo=10):
    angulo_rad = np.radians(azimut + 90)
    dx = largo * np.cos(angulo_rad)
    dy = largo * np.sin(angulo_rad)
    ax.plot([x - dx, x + dx], [y - dy, y + dy], 'r--', linewidth=2)

# ===================== INTERFAZ STREAMLIT =====================
st.title("Cálculo de posición por Rectas de Altura")

# Entrada de coordenadas
lat_grados = st.number_input("Latitud grados", step=1, format="%d", value=44)
lat_minutos = st.number_input("Latitud minutos", step=1.0, value=58.88)
lat_segundos = st.number_input("Latitud segundos", step=0.1, value=0.0)

lon_grados = st.number_input("Longitud grados", step=1, format="%d", value=8)
lon_minutos = st.number_input("Longitud minutos", step=1.0, value=5.81)
lon_segundos = st.number_input("Longitud segundos", step=0.1, value=0.0)

# Observaciones y desplazamiento
azimut1 = st.number_input("Azimut 1 (grados)", step=1.0, value=185.0)
dh1t = st.number_input("Diferencia de altura 1", step=0.1, value=2.0)
rumbo = st.number_input("Rumbo del desplazamiento (grados)", step=1.0, value=63.0)
distancia = st.number_input("Distancia recorrida (millas)", step=0.1, value=1.0)
azimut2 = st.number_input("Azimut 2 (grados)", step=1.0, value=300.0)
dh2t = st.number_input("Diferencia de altura 2", step=0.1, value=3.0)

if st.button("Calcular"):
    # Conversión de coordenadas a formato decimal
    latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos)
    longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

    # Ajuste de las diferencias de altura por latitud
    dh1 = abs(dh1t / np.cos(np.radians(latitud)))
    dh2 = abs(dh2t / np.cos(np.radians(latitud)))
    dh0 = abs(distancia / np.cos(np.radians(latitud)))

    # Ajustar azimuts si las diferencias son negativas
    if dh1t < 0:
        azimut1 += 180
    if dh2t < 0:
        azimut2 += 180

    # Vector de desplazamiento
    dx0 = dh0 * np.sin(np.radians(rumbo))
    dy0 = dh0 * np.cos(np.radians(rumbo))
    x0, y0 = dx0, dy0

    # Vector azimut 1 (desde final del desplazamiento)
    dx1 = dh1 * np.sin(np.radians(azimut1))
    dy1 = dh1 * np.cos(np.radians(azimut1))
    x1 = x0 + dx1
    y1 = y0 + dy1

    # Vector azimut 2 (desde origen)
    dx2 = dh2 * np.sin(np.radians(azimut2))
    dy2 = dh2 * np.cos(np.radians(azimut2))
    x2 = dx2
    y2 = dy2

    # Pendientes de las rectas perpendiculares (rectas de altura)
    m1 = np.tan(np.radians(azimut1 + 90))
    m2 = np.tan(np.radians(azimut2 + 90))

    if np.isclose(m1, m2):
        st.error("Las rectas de altura son paralelas, no hay intersección.")
    else:
        x_intersec = (m1 * x1 - m2 * x2 + y2 - y1) / (m1 - m2)
        y_intersec = m1 * (x_intersec - x1) + y1

        # Conversión a coordenadas geográficas
        y_i = y_intersec * np.cos(np.radians(latitud))
        lat_intersec = latitud + (y_i / 60)
        lon_intersec = longitud - (x_intersec / 60)

        # Conversión a grados y minutos
        lat_g, lat_m = decimal_a_grados_minutos(lat_intersec)
        lon_g, lon_m = decimal_a_grados_minutos(lon_intersec)

        st.write(f"Latitud de la intersección: {lat_g}° {lat_m:.2f}'")
        st.write(f"Longitud de la intersección: {lon_g}° {lon_m:.2f}'")

    # ===================== GRÁFICO CORREGIDO =====================
fig, ax = plt.subplots(figsize=(10, 8))
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Vectores
ax.plot([0, dx0], [0, dy0], 'b', linewidth=2, label='Desplazamiento')
ax.plot([dx0, dx1], [dy0, dy1], 'y', linewidth=2, label='Azimut 1')
ax.plot([0, dx2], [0, dy2], 'g', linewidth=2, label='Azimut 2')

# Recta de altura 1: perpendicular a Azimut 1, pasa por (dx1, dy1)
pendiente_az1 = np.tan(np.radians(azimut1))
pendiente_perp1 = -1 / pendiente_az1 if pendiente_az1 != 0 else np.inf
if np.isinf(pendiente_perp1):
    x1 = [dx1, dx1]
    y1 = [dy1 - 10, dy1 + 10]
else:
    x1 = np.linspace(dx1 - 10, dx1 + 10, 100)
    y1 = pendiente_perp1 * (x1 - dx1) + dy1
ax.plot(x1, y1, 'r--', linewidth=2, label='Recta de altura 1')

# Recta de altura 2: perpendicular a Azimut 2, pasa por (dx2, dy2)
pendiente_az2 = np.tan(np.radians(azimut2))
pendiente_perp2 = -1 / pendiente_az2 if pendiente_az2 != 0 else np.inf
if np.isinf(pendiente_perp2):
    x2 = [dx2, dx2]
    y2 = [dy2 - 10, dy2 + 10]
else:
    x2 = np.linspace(dx2 - 10, dx2 + 10, 100)
    y2 = pendiente_perp2 * (x2 - dx2) + dy2
ax.plot(x2, y2, 'r--', linewidth=2, label='Recta de altura 2')

# Punto de intersección
ax.plot(x_intersec, y_intersec, 'mo', markersize=10)
ax.text(x_intersec + 0.5, y_intersec + 0.5,
        f"Lat: {lat_intersec:.6f}\nLon: {lon_intersec:.6f}", fontsize=12)

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.set_title("Rectas de Altura")
ax.grid(True)
ax.legend()

st.pyplot(fig)

        # ===================== GRÁFICO DE PARTES IGUALES =====================
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        x_iguales = np.linspace(0, 8, 9)
        y_iguales = np.zeros_like(x_iguales)
        angulo_latitud_rad = np.radians(abs(latitud))
        y_aumentadas = x_iguales * np.tan(angulo_latitud_rad)

        ax2.plot(x_iguales, y_iguales, 'k-', linewidth=2, label='Partes Iguales')
        ax2.plot(x_iguales, y_aumentadas, 'r-', linewidth=2, label='Partes Aumentadas')

        for xi, yi in zip(x_iguales, y_aumentadas):
            ax2.plot([xi, xi], [0, yi], 'gray', linestyle='--', linewidth=1)

        ax2.set_title("Angulo = latitud")
        ax2.set_xlabel("Partes Iguales")
        ax2.set_ylabel("Partes Aumentadas")
        ax2.set_xlim(0, 8)
        ax2.set_ylim(0, max(y_aumentadas) * 1.1)
        ax2.grid(True)
        ax2.legend()

        st.pyplot(fig2)