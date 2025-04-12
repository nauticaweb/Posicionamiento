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

    # Ajuste de las diferencias de altura por latitud (sin errores de redondeo)
    dh1 = abs(dh1t / np.cos(np.radians(latitud)))
    dh2 = abs(dh2t / np.cos(np.radians(latitud)))
    dh0 = abs(distancia / np.cos(np.radians(latitud)))

    # Ajuste de los azimuts en función de las diferencias de altura
    if dh1t < 0:
        azimut1 += 180
    if dh2t < 0:
        azimut2 += 180

    # Componentes del desplazamiento
    dx0 = dh0 * np.sin(np.radians(rumbo))
    dy0 = dh0 * np.cos(np.radians(rumbo))

    dx1 = dh1 * np.sin(np.radians(azimut1)) + dx0
    dy1 = dh1 * np.cos(np.radians(azimut1)) + dy0

    dx2 = dh2 * np.sin(np.radians(azimut2))
    dy2 = dh2 * np.cos(np.radians(azimut2))

    # Cálculo de la intersección
    if dx1 != 0 and dx2 != 0:
        mz1 = dy1 / dx1
        mz2 = dy2 / dx2

        m1 = -1 / mz1
        m2 = -1 / mz2

        b1 = dy1 - m1 * dx1
        b2 = dy2 - m2 * dx2
        x_intersec = (b2 - b1) / (m1 - m2)
        y_intersec = m1 * x_intersec + b1
    else:
        st.error("Error en el cálculo de la intersección: división por cero.")

    # Conversión de la intersección a coordenadas geográficas (sin errores de redondeo)
    y_i = y_intersec * np.cos(np.radians(latitud))
    lat_intersec = latitud + (y_i / 60)
    lon_intersec = longitud - (x_intersec / 60)

    # Conversión de la latitud y longitud a grados y minutos
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
    ax.plot([dx0, dx1], [dy0, dy1], 'y', linewidth=2, label='azimut 1')
    ax.plot([0, dx2], [0, dy2], 'g', linewidth=2, label='azimut 2')

    # Rectas de altura (rojas punteadas)
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

    # ===================== GRÁFICO DE PARTES IGUALES Y PARTES AUMENTADAS =====================
    fig2, ax2 = plt.subplots(figsize=(10, 4))

    # Línea horizontal: Partes Iguales
    x_iguales = np.linspace(0, 8, 9)  # De 0 a 8 en partes iguales
    y_iguales = np.zeros_like(x_iguales)

    # Línea inclinada: Partes Aumentadas (ángulo igual a la latitud absoluta)
    angulo_latitud_rad = np.radians(abs(latitud))
    y_aumentadas = x_iguales * np.tan(angulo_latitud_rad)

    # Dibujar líneas
    ax2.plot(x_iguales, y_iguales, 'k-', linewidth=2, label='Partes Iguales')
    ax2.plot(x_iguales, y_aumentadas, 'r-', linewidth=2, label='Partes Aumentadas')

    # Líneas verticales que unen ambos ejes (como "<")
    for xi, yi in zip(x_iguales, y_aumentadas):
        ax2.plot([xi, xi], [0, yi], 'gray', linestyle='--', linewidth=1)

    # Formato del gráfico
    ax2.set_title("Angulo = latitud")
    ax2.set_xlabel("Partes Iguales")
    ax2.set_ylabel("Partes Aumentadas")
    ax2.set_xlim(0, 8)
    ax2.set_ylim(0, max(y_aumentadas) * 1.1)
    ax2.grid(True)
    ax2.legend()

    st.pyplot(fig2)