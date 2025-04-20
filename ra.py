# ===================== GRÁFICO =====================
    fig, ax = plt.subplots(figsize=(10, 8))

    # Ejes cartesianos
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    # Azimut 1 desde el extremo del desplazamiento
    line1, = ax.plot([dxD, dxD + dx1], [dyD, dyD + dy1], 'b', linewidth=2, label='Azimut 1')

    # Azimut 2
    line2, = ax.plot([0, dx2], [0, dy2], 'g', linewidth=2, label='Azimut 2')
    x_r2 = np.array([dx2 - dy2, dx2 + dy2])
    y_r2 = m2 * x_r2 + b2
    line3, = ax.plot(x_r2, y_r2, 'r--', linewidth=2)

    # Desplazamiento
    line4, = ax.plot([0, dxD], [0, dyD], 'm', linewidth=2, label='Desplazamiento')

    # Recta de altura desplazada
    x_r1 = np.array([dx1n - 5, dx1n + 5])
    y_r1 = m1 * x_r1 + b1_nuevo
    line5, = ax.plot(x_r1, y_r1, 'r--', linewidth=2)

    # Punto de corte nuevo
    line6, = ax.plot(x_intersec_nueva, y_intersec_nueva, 'mo', markersize=10)
    ax.text(x_intersec_nueva + 0.3, y_intersec_nueva + 0.3,
            f"Lat: {lat_intersec_nueva:.5f}\nLon: {lon_intersec_nueva:.5f}",
            fontsize=10, color='purple')

    # Redimensionar el gráfico automáticamente
    margen = 1.5  # margen extra para no pegarse al borde
    max_dist = max(abs(x_intersec_nueva), abs(y_intersec_nueva), 8) + margen
    ax.set_xlim(-max_dist, max_dist)
    ax.set_ylim(-max_dist, max_dist)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_title("Rectas de Altura")
    ax.grid(True)

    # Agregar la leyenda
    ax.legend([line1, line2, line3, line4, line6], [
       "Azimut 1", 
       "Azimut 2", 
       "Rectas de altura", 
       "Desplazamiento",  
       "Intersección"
    ], loc='upper right', fontsize=10, bbox_to_anchor=(1.27, 1))

    # Mostrar gráfico
    st.pyplot(fig)