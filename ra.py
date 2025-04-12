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

def calcular_interseccion(x1, y1, m1, x2, y2, m2):
    """
    Calcula la intersección de dos rectas dadas por sus pendientes (m1, m2) y un punto de cada recta.
    """
    if m1 == m2:
        return None  # Las rectas son paralelas

    # Ecuación de las rectas: y = m * x + b
    # Para cada recta, se tiene que calcular 'b' a partir del punto y la pendiente.
    b1 = y1 - m1 * x1
    b2 = y2 - m2 * x2

    # Resolver para encontrar la intersección
    x_intersec = (b2 - b1) / (m1 - m2)
    y_intersec = m1 * x_intersec + b1

    return x_intersec, y_intersec

# ===================== INTERFAZ STREAMLIT =====================
st.title("Cálculo de posición por Rectas de Altura")

# Entrada de coordenadas
lat_grados = st.number_input("Latitud grados", step=1, format="%d", value=41)
lat_minutos = st.number_input("Latitud minutos", step=1.0, value=37.1)
lat_segundos = st.number_input("Latitud segundos", step=0.1, value=0.0)

lon_grados = st.number_input("Longitud grados", step=1, format="%d", value=50)
lon_minutos = st.number_input("Longitud minutos", step=1.0, value=12.6)
lon_segundos = st.number_input("Longitud segundos", step=0.1, value=0.0)

# Observaciones y desplazamiento
azimut1 = st.number_input("Azimut 1 (grados)", step=1.0, value=218.3)
dh1t = st.number_input("Diferencia de altura 1", step=0.1, value=5.0)
rumbo = st.number_input("Rumbo del desplazamiento (grados)", step=1.0, value=327.0)
distancia = st.number_input("Distancia recorrida (millas)", step=0.1, value=1.63)
azimut2 = st.number_input("Azimut 2 (grados)", step=1.0, value=168.0)
dh2t = st.number_input("Diferencia de altura 2", step=0.1, value=-4.5)

if st.button("Calcular"):
    # Conversión de coordenadas a formato decimal
    latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos)
    longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

    # Ajustar diferencias de altura
    dh1 = dh1t
    dh2 = dh2t

    # Desplazamiento
    dh0 = distancia * 60  # Convertir millas a minutos de latitud

    # Calcular los desplazamientos en x e y en función del rumbo
    dx0 = dh0 * np.sin(np.radians(rumbo))
    dy0 = dh0 * np.cos(np.radians(rumbo))

    # Calcular las coordenadas de los puntos de las observaciones
    dx1 = dh1 * np.sin(np.radians(azimut1))
    dy1 = dh1 * np.cos(np.radians(azimut1))

    dx2 = dh2 * np.sin(np.radians(azimut2))
    dy2 = dh2 * np.cos(np.radians(azimut2))

    # ===================== CÁLCULO DE INTERSECCIÓN =====================
    # Calculamos las pendientes de las rectas (perpendiculares a los azimuts)
    m1 = -1 / np.tan(np.radians(azimut1))
    m2 = -1 / np.tan(np.radians(azimut2))

    # Usamos la función para calcular la intersección de las rectas
    interseccion = calcular_interseccion(dx1, dy1, m1, dx2, dy2, m2)

    if interseccion is None:
        st.error("Las rectas son paralelas, no tienen intersección.")
        x_intersec, y_intersec = None, None
    else:
        x_intersec, y_intersec = interseccion

    if x_intersec is not None and y_intersec is not None:
        # Convertir la intersección a coordenadas geográficas
        lat_intersec = latitud + (y_intersec / 60)
        lon_intersec = longitud + (x_intersec / 60)

        # Convertir a grados y minutos
        lat_g, lat_m = decimal_a_grados_minutos(lat_intersec)
        lon_g, lon_m = decimal_a_grados_minutos(lon_intersec)

        # Mostrar resultados
        st.write(f"Latitud de la intersección: {lat_g}° {lat_m:.2f}'")
        st.write(f"Longitud de la intersección: {lon_g}° {lon_m:.2f}'")

        # ===================== GRÁFICO =====================
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)

        # Vectores
        ax.plot([0, dx0], [0, dy0], 'b', linewidth=2, label='Desplazamiento')
        ax.plot([dx0, dx1], [dy0, dy1], 'y', linewidth=2, label='Azimut 1')
        ax.plot([0, dx2], [0, dy2], 'g', linewidth=2, label='Azimut 2')

        # Rectas de altura (rojas punteadas)
        ax.plot([dx1 - dy1, dx1 + dy1], [dy1 + dx1, dy1 - dx1], 'r--', linewidth=2)
        ax.plot([dx2 - dy2, dx2 + dy2], [dy2 + dx2, dy2 - dx2], 'r--', linewidth=2)

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