import numpy as np

# ================== DATOS DE ENTRADA ==================
# Estima en grados y minutos decimales
lat_g, lat_m = 41, 37.1  # Norte
lon_g, lon_m = 50, 12.6  # Oeste

# Azimut 1 y su diferencia de altura
azimut1 = 218.3
dh1 = 5

# Azimut 2 y su diferencia de altura
azimut2 = 168
dh2 = -4.5

# Rumbo del desplazamiento y su distancia
rumbo = 327
dh0 = 2

# ================== FUNCIONES ==================
def gms_a_decimal(grados, minutos, direccion):
    decimal = grados + minutos / 60
    if direccion in ['S', 'O']:
        decimal *= -1
    return decimal

def decimal_a_gm(decimal, is_lat=False):
    direccion = 'N' if decimal >= 0 else 'S' if is_lat else 'E' if decimal >= 0 else 'O'
    decimal = abs(decimal)
    grados = int(decimal)
    minutos = (decimal - grados) * 60
    return f"{grados}° {minutos:.2f}' {direccion}"

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
lat_corte = lat0 + y_intersec / 60
lon_corte = lon0 + x_intersec / 60

decimal_lat = decimal_a_gm(lat_corte, is_lat=True)
decimal_lon = decimal_a_gm(lon_corte, is_lat=False)

# Mostrar resultados
print(f"**Latitud de corte:** {decimal_lat}")
print(f"**Longitud de corte:** {decimal_lon}")