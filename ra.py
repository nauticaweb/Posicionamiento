import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rectas de Altura", layout="wide")

st.title("Rectas de Altura")

# ======= ENTRADA DE LATITUD Y LONGITUD =======

st.subheader("Punto de estima (latitud y longitud):")

col1, col2 = st.columns(2)

with col1:
    lat_grados = st.number_input("Latitud - Grados", -90, 90, 36)
    lat_minutos = st.number_input("Latitud - Minutos", 0.0, 60.0, 30.0, format="%.1f")
    lat_segundos = st.number_input("Latitud - Segundos", 0, 59, 0)
    lat_direccion = st.selectbox("Latitud - Dirección", ["N", "S"])

with col2:
    lon_grados = st.number_input("Longitud - Grados", -180, 180, 5)
    lon_minutos = st.number_input("Longitud - Minutos", 0.0, 60.0, 0.0, format="%.1f")
    lon_segundos = st.number_input("Longitud - Segundos", 0, 59, 0)
    lon_direccion = st.selectbox("Longitud - Dirección", ["E", "O"])

def a_decimal(grados, minutos, segundos, direccion):
    decimal = abs(grados) + minutos / 60 + segundos / 3600
    if direccion in ["S", "O"]:
        decimal *= -1
    return decimal

lat_decimal = a_decimal(lat_grados, lat_minutos, lat_segundos, lat_direccion)
lon_decimal = a_decimal(lon_grados, lon_minutos, lon_segundos, lon_direccion)

# ======= ENTRADA DE DATOS DE NAVEGACIÓN =======

st.subheader("Datos de navegación:")

azimut2 = st.number_input("Azimut 2 (°)", 0, 360, 45)
dh2 = st.number_input("Diferencia de altura 2", value=2.0)

rumbo = st.number_input("Rumbo del desplazamiento (°)", 0, 360, 90)
dh0 = st.number_input("Distancia del desplazamiento", value=3.0)

azimut1 = st.number_input("Azimut 1 (°)", 0, 360, 135)
dh1 = st.number_input("Diferencia de altura 1", value=2.0)

# ======= CÁLCULO DE VECTORES =======

dx0 = dh0 * np.sin(np.radians(rumbo))
dy0 = dh0 * np.cos(np.radians(rumbo))

dx1 = dh1 * np.sin(np.radians(azimut1))
dy1 = dh1 * np.cos(np.radians(azimut1))

dx2 = dh2 * np.sin(np.radians(azimut2))
dy2 = dh2 * np.cos(np.radians(azimut2))

# Vector 1: desde el final del desplazamiento
vx1 = dx0 + dx1
vy1 = dy0 + dy1

# Vector nuevo: desde algún punto en el eje Y hasta el punto final del vector 1
# Queremos prolongar hacia atrás el vector 1 hasta cortar el eje Y

if vx1 != 0:
    m_nuevo = vy1 / vx1
    x_virtual = 0
    y_virtual = -m_nuevo * vx1 + vy1
    dx_virtual = vx1
    dy_virtual = vy1 - y_virtual
else:
    x_virtual = 0
    y_virtual = 0
    dx_virtual = 0
    dy_virtual = 0

# ======= INTERSECCIÓN DE RECTAS DE ALTURA =======

try:
    # Pendientes de los vectores
    mz1 = dy2 / dx2
    mz2 = dy_virtual / dx_virtual

    # Pendientes de las rectas de altura (perpendiculares)
    m1 = -1 / mz1
    m2 = -1 / mz2

    # Términos independientes
    b1 = dy2 - m1 * dx2
    b2 = y_virtual - m2 * x_virtual

    # Intersección
    x_intersec = (b2 - b1) / (m1 - m2)
    y_intersec = m1 * x_intersec + b1

    interseccion_valida = True

except Exception as e:
    interseccion_valida = False
    st.error(f"Error en el cálculo de la intersección: {e}")

# ======= GRÁFICO =======

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.invert_xaxis()

# Vectores
ax.quiver(0, 0, dx0, dy0, angles='xy', scale_units='xy', scale=1, color='gray', label='Desplazamiento')
ax.quiver(dx0, dy0, dx1, dy1, angles='xy', scale_units='xy', scale=1, color='blue', label='Vector 1')
ax.quiver(0, 0, dx2, dy2, angles='xy', scale_units='xy', scale=1, color='green', label='Vector 2')
ax.quiver(x_virtual, y_virtual, dx_virtual, dy_virtual, angles='xy', scale_units='xy', scale=1, color='orange', linestyle='dashed', label='Vector nuevo')

# Rectas de altura
if interseccion_valida:
    x_vals = np.array([-8, 8])
    y_recta1 = m1 * x_vals + b1
    y_recta2 = m2 * x_vals + b2
    ax.plot(x_vals, y_recta1, 'r--', label='Recta altura 1')
    ax.plot(x_vals, y_recta2, 'm--', label='Recta altura 2')
    ax.plot(x_intersec, y_intersec, 'ko', label='Intersección')

ax.legend()
st.pyplot(fig)

# ======= COORDENADAS DEL PUNTO DE CORTE =======

lat_corte = lat_decimal + y_intersec / 60
lon_corte = lon_decimal + x_intersec / 60

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

if interseccion_valida:
    st.subheader("Coordenadas del punto de corte:")
    st.markdown(f"**Latitud:** {decimal_a_gm(lat_corte, is_lat=True)}")
    st.markdown(f"**Longitud:** {decimal_a_gm(lon_corte, is_lat=False)}")