import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Rectas de Altura")

# ==== ENTRADA DE LATITUD Y LONGITUD ====

st.subheader("1. Punto de estima")

col1, col2 = st.columns(2)

with col1:
    lat_g = st.number_input("Latitud grados", value=36, format="%d")
    lat_m = st.number_input("Latitud minutos", value=40.0, format="%.1f")
    lat_s = st.number_input("Latitud segundos", value=0.0, format="%.1f")
    lat_dir = st.selectbox("Latitud", ["N", "S"])

with col2:
    lon_g = st.number_input("Longitud grados", value=4, format="%d")
    lon_m = st.number_input("Longitud minutos", value=30.0, format="%.1f")
    lon_s = st.number_input("Longitud segundos", value=0.0, format="%.1f")
    lon_dir = st.selectbox("Longitud", ["E", "O"])

def dms_a_decimal(g, m, s, direccion):
    decimal = g + m / 60 + s / 3600
    if direccion in ["S", "O"]:
        decimal *= -1
    return decimal

lat_decimal = dms_a_decimal(lat_g, lat_m, lat_s, lat_dir)
lon_decimal = dms_a_decimal(lon_g, lon_m, lon_s, lon_dir)

# ==== ENTRADA DE DATOS ====

st.subheader("2. Rectas de altura")

azimut2 = st.number_input("Azimut 2", value=45.0)
dh2 = st.number_input("Diferencia de altura 2", value=5.0)

st.subheader("3. Desplazamiento")

rumbo = st.number_input("Rumbo", value=90.0)
dh0 = st.number_input("Distancia de desplazamiento", value=4.0)

st.subheader("4. Recta de altura 1")

azimut1 = st.number_input("Azimut 1", value=135.0)
dh1 = st.number_input("Diferencia de altura 1", value=5.0)

# ==== CÁLCULOS ====

# Desplazamiento
dx0 = dh0 * np.sin(np.radians(rumbo))
dy0 = dh0 * np.cos(np.radians(rumbo))

# Vector 1
dx1 = dh1 * np.sin(np.radians(azimut1)) 
dy1 = dh1 * np.cos(np.radians(azimut1)) 

# Vector 2
dx2 = dh2 * np.sin(np.radians(azimut2))
dy2 = dh2 * np.cos(np.radians(azimut2))

# Punto final del vector 1
x1 = dx0 + dx1
y1 = dy0 + dy1

# ==== NUEVO VECTOR DESDE EJE Y ====
if x1 != 0:
    m_aux = y1 / x1
    y_inicio_aux = y1 - m_aux * x1
else:
    y_inicio_aux = 0

x_aux = 0
dx_aux = x1 - x_aux
dy_aux = y1 - y_inicio_aux

# ==== CÁLCULO DE INTERSECCIÓN DE RECTAS DE ALTURA ====

if dx_aux != 0 and dx2 != 0:
    mz1 = dy_aux / dx_aux
    mz2 = dy2 / dx2

    m1 = -1 / mz1
    m2 = -1 / mz2

    b1 = y1 - m1 * x1
    b2 = dy2 - m2 * dx2

    x_intersec = (b2 - b1) / (m1 - m2)
    y_intersec = m1 * x_intersec + b1
else:
    st.error("Error en el cálculo de la intersección: división por cero.")
    x_intersec, y_intersec = 0, 0

# ==== GRÁFICO ====

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(8, -8)
ax.set_ylim(-8, 8)
ax.set_aspect('equal')
ax.grid(True)
ax.axhline(0, color='gray')
ax.axvline(0, color='gray')

# Vectores
ax.arrow(0, 0, dx0, dy0, head_width=0.2, color='blue', label='Desplazamiento')
ax.arrow(dx0, dy0, dx1, dy1, head_width=0.2, color='green', label='Vector 1')
ax.arrow(0, 0, dx2, dy2, head_width=0.2, color='orange', label='Vector 2')
ax.arrow(x_aux, y_inicio_aux, dx_aux, dy_aux, head_width=0.2, color='purple', label='Vector adicional')

# Rectas de altura
x_vals = np.linspace(-10, 10, 400)
y_recta1 = m1 * x_vals + b1
y_recta2 = m2 * x_vals + b2
ax.plot(x_vals, y_recta1, '--', color='green')
ax.plot(x_vals, y_recta2, '--', color='orange')

# Punto de intersección
ax.plot(x_intersec, y_intersec, 'ro', label='Intersección')

ax.legend()
ax.set_title("Vectores y Rectas de Altura")
st.pyplot(fig)

# ==== LATITUD Y LONGITUD EN GRADOS Y MINUTOS CON DÉCIMAS ====

def decimal_a_gm(decimal, is_lat=True):
    direccion = ""
    if is_lat:
        direccion = "N" if decimal >= 0 else "S"
    else:
        direccion = "E" if decimal >= 0 else "O"
    decimal = abs(decimal)
    grados = int(decimal)
    minutos = round((decimal - grados) * 60, 1)
    return f"{grados}° {minutos}' {direccion}"

st.subheader("Coordenadas ingresadas:")
st.markdown(f"**Latitud:** {decimal_a_gm(lat_decimal, is_lat=True)}")
st.markdown(f"**Longitud:** {decimal_a_gm(lon_decimal, is_lat=False)}")