import streamlit as st
import numpy as np

# ================== FUNCIONES ==================
def gms_a_decimal(grados, minutos, direccion):
    """Convierte coordenadas en grados, minutos y dirección a decimal"""
    decimal = grados + minutos / 60
    if direccion in ['S', 'O']:
        decimal *= -1
    return decimal

def decimal_a_gm(decimal, is_lat=False):
    """Convierte coordenadas decimales a grados y minutos con decimales"""
    direccion = 'N' if decimal >= 0 else 'S' if is_lat else 'E' if decimal >= 0 else 'O'
    decimal = abs(decimal)
    grados = int(decimal)
    minutos = (decimal - grados) * 60
    return f"{grados}° {minutos:.2f}' {direccion}"

# ================== STREAMLIT INTERFAZ ==================
st.title("Cálculo de Punto de Corte")

# Datos de entrada: latitud y longitud
st.sidebar.header("Datos de Entrada")
lat_g = st.sidebar.number_input("Latitud (Grados)", min_value=-90.0, max_value=90.0, value=41.0)
lat_m = st.sidebar.number_input("Latitud (Minutos)", min_value=0.0, max_value=60.0, value=37.1)
lon_g = st.sidebar.number_input("Longitud (Grados)", min_value=-180.0, max_value=180.0, value=50.0)
lon_m = st.sidebar.number_input("Longitud (Minutos)", min_value=0.0, max_value=60.0, value=12.6)

# Azimut y diferencia de altura
azimut1 = st.sidebar.number_input("Azimut 1 (°)", min_value=0.0, max_value=360.0, value=218.3)
dh1 = st.sidebar.number_input("Diferencia de altura 1", min_value=-100.0, max_value=100.0, value=5.0)

azimut2 = st.sidebar.number_input("Azimut 2 (°)", min_value=0.0, max_value=360.0, value=168.0)
dh2 = st.sidebar.number_input("Diferencia de altura 2", min_value=-100.0, max_value=100.0, value=-4.5)

# Rumbo del desplazamiento y distancia
rumbo = st.sidebar.number_input("Rumbo del desplazamiento (°)", min_value=0.0, max_value=360.0, value=327.0)
dh0 = st.sidebar.number_input("Distancia del desplazamiento (millas náuticas)", min_value=0.0, max_value=100.0, value=2.0)

# ================== CÁLCULO ==================
# Punto de estima en decimal
lat0 = gms_a_decimal(lat_g, lat_m, 'N')
lon0 = gms_a_decimal(lon_g, lon_m, 'O')

# Desplazamiento (vector 0)
dx0 = dh0 * np.sin(np.radians(rumbo))
dy0 = dh0 * np.cos(np.radians(rumbo))

# Vector 1 (desde fin de vector 0)
dx1 = dh1 * np.sin(np.radians(azimut1))
dy1 = dh1 * np.cos(np.radians(azimut1))
x1 = dx0 + dx1
y1 = dy0 + dy1

# Vector 2 (desde 0,0)
dx2 = dh2 * np.sin(np.radians(azimut2))
dy2 = dh2 * np.cos(np.radians(azimut2))
x2 = dx2
y2 = dy2

# Vector auxiliar que une un punto en el eje y con el final de vector 1
if x1 != 0:
    m_aux = y1 / x1
    x_aux = 0
    y_aux = -m_aux * x1 + y1
else:
    x_aux = 0
    y_aux = 0

# Rectas de altura
mz_aux = (y1 - y_aux) / (x1 - x_aux) if (x1 - x_aux) != 0 else float('inf')
mz2 = dy2 / dx2 if dx2 != 0 else float('inf')

m1 = -1 / mz_aux if mz_aux != 0 and mz_aux != float('inf') else float('inf')
m2 = -1 / mz2 if mz2 != 0 and mz2 != float('inf') else float('inf')

b1 = y1 - m1 * x1 if m1 != float('inf') else float('inf')
b2 = y2 - m2 * x2 if m2 != float('inf') else float('inf')

# Intersección
if m1 != m2:
    x_intersec = (b2 - b1) / (m1 - m2)
    y_intersec = m1 * x_intersec + b1
else:
    x_intersec, y_intersec = None, None

# ================== COORDENADAS FINALES ==================
lat_corte = lat0 + y_intersec / 60 if x_intersec is not None else None
lon_corte = lon0 + x_intersec / 60 if x_intersec is not None else None

# Mostrar resultados
if x_intersec is not None and y_intersec is not None:
    decimal_lat = decimal_a_gm(lat_corte, is_lat=True)
    decimal_lon = decimal_a_gm(lon_corte, is_lat=False)

    st.markdown(f"**Latitud de corte:** {decimal_lat}")
    st.markdown(f"**Longitud de corte:** {decimal_lon}")
else:
    st.error("No se pudo calcular la intersección.")