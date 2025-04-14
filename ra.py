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

st.header("1. Punto de estima")
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

st.header("3. Desplazamiento")
rumbo = st.number_input("Rumbo (°)", step=1.0, value=0.0)
distancia = st.number_input("Distancia navegada", step=0.1, value=0.0)

# ===================== BOTÓN =====================
if st.button("Calcular"):
    # Convertir coordenadas a decimales
    latitud = gms_a_decimal(lat_grados, lat_minutos, lat_segundos)
    longitud = gms_a_decimal(lon_grados, lon_minutos, lon_segundos)

    # ================== VECTORES ==================
    # Vector 1 (azimut 1)
    az1 = azimut1 + 180 if dh1t < 0 else azimut1
    dh1 = abs(dh1t / np.cos(np.radians(latitud)))
    dx1 = dh1 * np.sin(np.radians(az1))
    dy1 = dh1 * np.cos(np.radians(az1))

    # Vector 2 (azimut 2)
    az2 = azimut2 + 180 if dh2t < 0 else azimut2
    dh2 = abs(dh2t / np.cos(np.radians(latitud)))
    dx2 = dh2 * np.sin(np.radians(az2))
    dy2 = dh2 * np.cos(np.radians(az2))

    # Vector desplazamiento
    dD = abs(distancia / np.cos(np.radians(latitud)))
    dxD = dD * np.sin(np.radians(rumbo))
    dyD = dD * np.cos(np.radians(rumbo))

    # ================== RECTAS DE ALTURA ==================
    # Rectas perpendiculares
    mz1 = dy1 / dx1
    mz2 = dy2 / dx2
    m1 = -1 / mz1
    m2 = -1 / mz2

    b1 = dy1 - m1 * dx1
    b2 = dy2 - m2 * dx2

    # Intersección original
    x_intersec = (b2 - b1) / (m1 - m2)
    y_intersec = m1 * x_intersec + b1

    # Nueva posición del vector azimut 1 tras desplazamiento
    dx1n = dxD + dx1
    dy1n = dyD + dy1
    b1_nuevo = dy1n - m1 * dx1n

    # Nueva intersección con la recta del azimut 2
    x_intersec_nueva = (b2 - b1_nuevo) / (m1 - m2)
    y_intersec_nueva = m1 * x_intersec_nueva + b1_nuevo

    # ===================== RESULTADOS =====================
    st.subheader("4. Posición observada")

    y_i_nueva = y_intersec_nueva * np.cos(np.radians(latitud))
    lat_intersec_nueva = latitud + (y_i_nueva / 60)
    lon_intersec_nueva = longitud - (x_intersec_nueva / 60)

# Corregir longitud si sale del rango 180
    if lon_intersec_nueva < -180:
        lon_intersec_nueva += 360
    elif lon_intersec_nueva > 180:
        lon_intersec_nueva -= 360

    lat_gn, lat_mn = decimal_a_grados_minutos(lat_intersec_nueva)
    lon_gn, lon_mn = decimal_a_grados_minutos(lon_intersec_nueva)
    NSn = "N" if lat_intersec_nueva > 0 else "S"
    EWn = "W" if lon_intersec_nueva > 0 else "E"

    st.write(f"Latitud: `{abs(lat_gn)}° {lat_mn:.2f}' {NSn}`")
    st.write(f"Longitud: `{abs(lon_gn)}° {lon_mn:.2f}' {EWn}`")

    # ===================== GRÁFICO =====================
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

   
     # Azimut 1 desde el extremo del desplazamiento
    ax.plot([dxD, dxD + dx1], [dyD, dyD + dy1], 'y', linewidth=2, label='Azimut 1')

    # Azimut 2
    ax.plot([0, dx2], [0, dy2], 'g', linewidth=2, label='Azimut 2')
    x_r2 = np.array([dx2 - dy2, dx2 + dy2])
    y_r2 = m2 * x_r2 + b2
    ax.plot(x_r2, y_r2, 'r--', linewidth=2)

    # Desplazamiento
    ax.plot([0, dxD], [0, dyD], 'b', linewidth=2, label='Desplazamiento')

    
    # Recta de altura desplazada
    x_r1 = np.array([dx1n - 5, dx1n + 5])
    y_r1 = m1 * x_r1 + b1_nuevo
    ax.plot(x_r1, y_r1, 'r--', linewidth=2)

    # Punto de corte nuevo
    ax.plot(x_intersec_nueva, y_intersec_nueva, 'mo', markersize=10)
    ax.text(x_intersec_nueva + 0.3, y_intersec_nueva + 0.3,
            f"Lat: {lat_intersec_nueva:.5f}\nLon: {lon_intersec_nueva:.5f}",
            fontsize=10, color='purple')

    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_title("Rectas de Altura")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

     # ===================== GRÁFICO 2: Ángulo igual a la latitud =====================
    fig2, ax2 = plt.subplots(figsize=(5, 4))  # Más largo, acorde a 0–8

    r = 8  # Un cuadrante (como de 0 a 8 en el gráfico 1)

    # Línea horizontal
    ax2.plot([0, r], [0, 0], color='black', linewidth=2)

    # Línea oblicua que forma el ángulo con la horizontal
    x_angle = r
    y_angle = r * np.tan(np.radians(latitud))
    ax2.plot([0, x_angle], [0, y_angle], color='purple', linewidth=2)

    # Marcas y líneas verticales hasta la oblicua
    for i in np.arange(0, r + 0.01, 0.5):
        y_i = i * np.tan(np.radians(latitud))
        ax2.plot([i, i], [0, y_i], color='gray', linestyle='--', linewidth=1)

        # Números solo en pares enteros debajo del eje
        if i % 2 == 0:
            ax2.text(i, -0.3, f"{int(i)}", ha='center', va='top', fontsize=10)

    # Estética
    ax2.set_xlim(-0.5, r + 0.5)
    ax2.set_ylim(-0.5, max(1, y_angle + 0.5))
    ax2.axis('off')

    # Título debajo del gráfico
    st.markdown("#### Ángulo = Latitud")

    st.pyplot(fig2)