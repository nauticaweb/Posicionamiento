import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Cálculo de Rectas de Altura")

# ====== Conversión GMS y GMM ======

def gms_a_decimal(grados, minutos, segundos):
    signo = -1 if grados < 0 else 1
    return signo * (abs(grados) + minutos / 60 + segundos / 3600)

def decimal_a_gmm(decimal):
    grados = int(decimal)
    minutos_dec = abs((decimal - grados) * 60)
    return grados, minutos_dec

# ====== Entrada de datos ======

st.subheader("1. Punto de estima")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Latitud (GMS)**")
    lat_g = st.number_input("Grados Latitud", value=40, step=1, format="%d")
    lat_m = st.number_input("Minutos Latitud", value=0, step=1, format="%d")
    lat_s = st.number_input("Segundos Latitud", value=0.0, step=0.1)
    lat = gms_a_decimal(lat_g, lat_m, lat_s)
    lat_g_out, lat_min_out = decimal_a_gmm(lat)
    direccion_lat = "N" if lat >= 0 else "S"
    st.markdown(f"**Latitud:** {abs(lat_g_out)}° {lat_min_out:.1f}′ {direccion_lat}")

with col2:
    st.markdown("**Longitud (GMS)**")
    lon_g = st.number_input("Grados Longitud", value=-5, step=1, format="%d")
    lon_m = st.number_input("Minutos Longitud", value=0, step=1, format="%d")
    lon_s = st.number_input("Segundos Longitud", value=0.0, step=0.1)
    lon = gms_a_decimal(lon_g, lon_m, lon_s)
    lon_g_out, lon_min_out = decimal_a_gmm(lon)
    direccion_lon = "E" if lon >= 0 else "W"
    st.markdown(f"**Longitud:** {abs(lon_g_out)}° {lon_min_out:.1f}′ {direccion_lon}")

st.subheader("2. Azimut 1")
azimut1 = st.number_input("Azimut 1 (°)", value=70.0)
dh1 = st.number_input("Diferencia de altura 1 (distancia)", value=15.0)

st.subheader("3. Desplazamiento")
rumbo = st.number_input("Rumbo (°)", value=45.0)
dh0 = st.number_input("Distancia de desplazamiento", value=10.0)

st.subheader("4. Azimut 2")
azimut2 = st.number_input("Azimut 2 (°)", value=120.0)
dh2 = st.number_input("Diferencia de altura 2 (distancia)", value=15.0)

# ====== Cálculo de vectores ======

dx0 = dh0 * np.sin(np.radians(rumbo))
dy0 = dh0 * np.cos(np.radians(rumbo))

dx1 = dh1 * np.sin(np.radians(azimut1))
dy1 = dh1 * np.cos(np.radians(azimut1))

dx2 = dh2 * np.sin(np.radians(azimut2))
dy2 = dh2 * np.cos(np.radians(azimut2))

x1f = dx0 + dx1
y1f = dy0 + dy1

# Cálculo del nuevo vector desde eje Y hasta el punto final del vector 1
if x1f != 0:
    m_aux = y1f / x1f
    y_inicio_aux = y1f - m_aux * x1f
else:
    y_inicio_aux = 0

x_aux = 0
dx_aux = x1f - x_aux
dy_aux = y1f - y_inicio_aux

# ====== Cálculo de la intersección ======
interseccion = None
if dx_aux != 0 and dx2 != 0:
    mz1 = dy_aux / dx_aux
    m1 = -1 / mz1

    mz2 = dy2 / dx2
    m2 = -1 / mz2

    b1 = y1f - m1 * x1f
    b2 = dy2 - m2 * dx2

    x_intersec = (b2 - b1) / (m1 - m2)
    y_intersec = m1 * x_intersec + b1

    interseccion = (x_intersec, y_intersec)

# ====== Gráfico 1: Vectores y Rectas de Altura ======

with st.expander("Gráfico 1: Vectores y Rectas de Altura", expanded=True):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.grid(True)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)

    ax.arrow(0, 0, dx0, dy0, head_width=0.5, color='blue', label='Desplazamiento')
    ax.arrow(dx0, dy0, dx1, dy1, head_width=0.5, color='green', label='Vector 1')
    ax.arrow(0, 0, dx2, dy2, head_width=0.5, color='orange', label='Vector 2')

    if interseccion:
        x_vals = np.linspace(-20, 30, 200)
        y_vals1 = m1 * x_vals + b1
        y_vals2 = m2 * x_vals + b2
        ax.plot(x_vals, y_vals1, '--', color='green', label='Recta Altura 1')
        ax.plot(x_vals, y_vals2, '--', color='orange', label='Recta Altura 2')
        ax.plot(*interseccion, 'ro', label='Intersección')

    ax.legend()
    ax.set_title("Vectores y Rectas de Altura")
    st.pyplot(fig)

# ====== Gráfico 2: Ángulo igual a la latitud ======

with st.expander("Gráfico 2: Ángulo igual a la Latitud", expanded=True):
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.set_aspect('equal')
    ax2.grid(True)

    r = 5
    ax2.plot([0, 0], [0, r], 'k')
    ax2.plot([0, r * np.cos(np.radians(lat))], [0, r * np.sin(np.radians(lat))], 'b', label=f'Latitud = {lat:.4f}°')

    ax2.annotate(f"{lat:.2f}°", xy=(r * 0.5 * np.cos(np.radians(lat)), r * 0.5 * np.sin(np.radians(lat))),
                 textcoords="offset points", xytext=(10, 10), ha='center')
    ax2.set_title("Ángulo igual a la Latitud")
    ax2.set_xlim(-r, r)
    ax2.set_ylim(0, r + 1)
    ax2.legend()
    st.pyplot(fig2)

# ====== Mostrar coordenadas de intersección ======
if interseccion:
    st.success(f"Intersección encontrada en: x = {x_intersec:.2f}, y = {y_intersec:.2f}")
else:
    st.warning("No se pudo calcular la intersección (posible división por cero).")


# ====== Coordenadas definitivas (lat/lon) ======
if interseccion:
    dx_final, dy_final = interseccion

    # Aproximación simple: 1 minuto de latitud ≈ 1.852 km = 1 milla náutica
    milla_nautica_km = 1.852
    metros_por_minuto = milla_nautica_km * 1000
    grados_por_metro = 1 / (60 * metros_por_minuto)  # 1° = 60 min

    # Conversión de desplazamientos a grados
    lat_final = lat + dy_final * grados_por_metro
    lon_final = lon + (dx_final * grados_por_metro) / np.cos(np.radians(lat))

    # Conversión a GMM
    lat_g, lat_m = decimal_a_gmm(lat_final)
    lon_g, lon_m = decimal_a_gmm(lon_final)

    # Direcciones
    lat_dir = "N" if lat_final >= 0 else "S"
    lon_dir = "E" if lon_final >= 0 else "W"

    st.subheader("5. Coordenadas Finales Estimadas")
    st.markdown(f"**Latitud:** {abs(lat_final):.5f}° {lat_dir}  →  {abs(lat_g)}° {lat_m:.1f}′ {lat_dir}")
    st.markdown(f"**Longitud:** {abs(lon_final):.5f}° {lon_dir}  →  {abs(lon_g)}° {lon_m:.1f}′ {lon_dir}")