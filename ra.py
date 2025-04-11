import streamlit as st 
import numpy as np 
import matplotlib.pyplot as plt

def gms_a_decimal(grados, minutos, segundos): return grados + minutos / 60 + segundos / 3600

def decimal_a_grados_minutos(decimal): grados = int(decimal) minutos = abs((decimal - grados) * 60) return grados, minutos

st.title("Rectas de Altura")

st.sidebar.header("1. Coordenadas iniciales") lat_grados = st.sidebar.number_input("Latitud (grados)", value=36) lat_minutos = st.sidebar.number_input("Latitud (minutos)", value=30) lat_segundos = st.sidebar.number_input("Latitud (segundos)", value=0) lon_grados = st.sidebar.number_input("Longitud (grados)", value=-6) lon_minutos = st.sidebar.number_input("Longitud (minutos)", value=15) lon_segundos = st.sidebar.number_input("Longitud (segundos)", value=0)

st.sidebar.header("2. Datos de observación") distancia = st.sidebar.number_input("Desplazamiento estimado (mn)", value=3.0) rumbo = st.sidebar.number_input("Rumbo (grados)", value=45.0) dh1t = st.sidebar.number_input("Diferencia de altura 1", value=2.0) dh2t = st.sidebar.number_input("Diferencia de altura 2", value=2.0) azimut1 = st.sidebar.number_input("Azimut 1 (grados)", value=135.0) azimut2 = st.sidebar.number_input("Azimut 2 (grados)", value=225.0)

if st.button("Calcular"): latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos) longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

dh1 = abs(dh1t / np.cos(np.radians(latitud)))
dh2 = abs(dh2t / np.cos(np.radians(latitud)))
dh0 = abs(distancia / np.cos(np.radians(latitud)))

if dh1t < 0:
    azimut1 += 180
if dh2t < 0:
    azimut2 += 180

dx0 = dh0 * np.sin(np.radians(rumbo))
dy0 = dh0 * np.cos(np.radians(rumbo))
dx1 = dh1 * np.sin(np.radians(azimut1)) + dx0
dy1 = dh1 * np.cos(np.radians(azimut1)) + dy0
dx2 = dh2 * np.sin(np.radians(azimut2))
dy2 = dh2 * np.cos(np.radians(azimut2))

mz1 = dy1 / dx1
mz2 = dy2 / dx2
m1 = -1 / mz1
m2 = -1 / mz2

b1 = dy1 - m1 * dx1
b2 = dy2 - m2 * dx2
x_intersec = (b2 - b1) / (m1 - m2)
y_intersec = m1 * x_intersec + b1

y_i = y_intersec * np.cos(np.radians(latitud))
lat_intersec = latitud + (y_i / 60)
lon_intersec = longitud - (x_intersec / 60)

lat_g, lat_m = decimal_a_grados_minutos(lat_intersec)
lon_g, lon_m = decimal_a_grados_minutos(lon_intersec)
NS = "N" if lat_intersec > 0 else "S"
EW = "W" if lon_intersec > 0 else "E"

st.subheader("3. Situación estimada")
st.markdown("**Coordenadas decimales:**")
st.write(f"Latitud: `{lat_intersec:.6f}`")
st.write(f"Longitud: `{lon_intersec:.6f}`")

st.markdown("**Coordenadas en GMS:**")
st.write(f"Latitud: `{abs(lat_g)}° {lat_m:.2f}' {NS}`")
st.write(f"Longitud: `{abs(lon_g)}° {lon_m:.2f}' {EW}`")

# ===================== GRÁFICO DE RECTAS DE ALTURA =====================
fig, ax = plt.subplots(figsize=(10, 8))
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

ax.plot([0, dx0], [0, dy0], 'b', linewidth=2, label='Desplazamiento')
ax.plot([dx0, dx1], [dy0, dy1], 'y', linewidth=2, label='azimut 1')
ax.plot([0, dx2], [0, dy2], 'g', linewidth=2, label='azimut 2')
ax.plot([dx1 - dy1, dx1 + dy1], [dy1 + dx1, dy1 - dx1], 'r--', linewidth=2)
ax.plot([dx2 - dy2, dx2 + dy2], [dy2 + dx2, dy2 - dx2], 'r--', linewidth=2)

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

# ===================== GRÁFICO DE PARTES IGUALES Y AUMENTADAS =====================
fig2, ax2 = plt.subplots(figsize=(10, 8))

x_iguales = np.linspace(0, 8, 9)
y_iguales = np.zeros_like(x_iguales)
angulo_latitud_rad = np.radians(abs(latitud))
y_aumentadas = x_iguales * np.tan(angulo_latitud_rad)

ax2.plot(x_iguales, y_iguales, 'k-', linewidth=2, label='Partes Iguales')
ax2.plot(x_iguales, y_aumentadas, 'r-', linewidth=2, label='Partes Aumentadas')

for xi, yi in zip(x_iguales, y_aumentadas):
    ax2.plot([xi, xi], [0, yi], 'gray', linestyle='--', linewidth=1)

ax2.set_title("Relación entre Partes Iguales y Partes Aumentadas")
ax2.set_xlabel("Unidades (0 a 8)")
ax2.set_ylabel("Proporción Aumentada")
ax2.set_xlim(0, 8)
ax2.set_ylim(0, max(y_aumentadas) * 1.1)
ax2.set_aspect('equal', adjustable='box')
ax2.grid(True)
ax2.legend()

st.pyplot(fig2)

