import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot

# -----------------------------
# Funciones auxiliares
# -----------------------------
def normalizar(v):
    return v / np.linalg.norm(v)

def arco_gran_circulo(A, B, n=100):
    A = normalizar(A)
    B = normalizar(B)
    ang = np.arccos(np.clip(np.dot(A, B), -1, 1))
    t = np.linspace(0, 1, n)
    puntos = []
    for ti in t:
        v = (np.sin((1 - ti) * ang) * A + np.sin(ti * ang) * B) / np.sin(ang)
        puntos.append(normalizar(v))
    return np.array(puntos)

def arco_angulo(vertice, p1, p2, fraccion_radio=0.2, n=64):
    v = normalizar(vertice)
    a = p1 - v * np.dot(v, p1)
    b = p2 - v * np.dot(v, p2)
    a = normalizar(a)
    b = normalizar(b)
    ang = np.arccos(np.clip(np.dot(a, b), -1, 1))
    t = np.linspace(0, 1, n)
    pts = []
    for ti in t:
        dir_vec = (np.sin((1 - ti) * ang) * a + np.sin(ti * ang) * b) / np.sin(ang)
        pts.append(normalizar(v + fraccion_radio * dir_vec))
    return np.array(pts)

# -----------------------------
# Definición de puntos
# -----------------------------
R = 1.0
polo_norte = np.array([0, 0, R])
lat_obs = np.radians(40)
lon_obs = np.radians(0)
cenit = np.array([
    np.cos(lat_obs) * np.cos(lon_obs),
    np.cos(lat_obs) * np.sin(lon_obs),
    np.sin(lat_obs)
]) * R
dec_star = np.radians(60)
ra_star = np.radians(45)
estrella = np.array([
    np.cos(dec_star) * np.cos(ra_star),
    np.cos(dec_star) * np.sin(ra_star),
    np.sin(dec_star)
]) * R

# -----------------------------
# Lados y ángulos
# -----------------------------
arco_PC = arco_gran_circulo(polo_norte, cenit)
arco_PE = arco_gran_circulo(polo_norte, estrella)
arco_CE = arco_gran_circulo(cenit, estrella)

arco_ang_polo     = arco_angulo(polo_norte, cenit, estrella, fraccion_radio=0.22)
arco_ang_cenit    = arco_angulo(cenit, polo_norte, estrella, fraccion_radio=0.22)
arco_ang_estrella = arco_angulo(estrella, polo_norte, cenit, fraccion_radio=0.22)

# -----------------------------
# Figura Plotly
# -----------------------------
fig = go.Figure()

# Puntos
fig.add_trace(go.Scatter3d(
    x=[polo_norte[0], cenit[0], estrella[0]],
    y=[polo_norte[1], cenit[1], estrella[1]],
    z=[polo_norte[2], cenit[2], estrella[2]],
    mode="markers+text",
    text=["Polo Norte", "Cenit", "Estrella"],
    textposition="top center",
    marker=dict(size=6, color=["red", "purple", "yellow"]),
    name="Puntos"
))

# Lados
for arco, nombre in zip(
    [arco_PC, arco_PE, arco_CE],
    ["Meridiano (90 - latitud)", "Círculo Horario (90 - declinación)", "Vertical (90 - altura)"]
):
    fig.add_trace(go.Scatter3d(
        x=arco[:, 0], y=arco[:, 1], z=arco[:, 2],
        mode="lines",
        line=dict(color="blue", width=3),
        name=nombre
    ))

# ---------- Ángulo en el Polo ----------
grupo_polo = "grupo_angulo_polo"
fig.add_trace(go.Scatter3d(
    x=arco_ang_polo[:, 0], y=arco_ang_polo[:, 1], z=arco_ang_polo[:, 2],
    mode="lines",
    line=dict(color="red", width=4, dash="dot"),
    name="Ángulo en el Polo",
    legendgroup=grupo_polo,
    showlegend=True
))
mid_polo = arco_ang_polo[len(arco_ang_polo)//2]
fig.add_trace(go.Scatter3d(
    x=[mid_polo[0]], y=[mid_polo[1]], z=[mid_polo[2]],
    mode="text",
    text=["Ángulo en el Polo"],
    showlegend=False,
    legendgroup=grupo_polo,
    hoverinfo="skip"
))

# ---------- Azimut ----------
grupo_cenit = "grupo_angulo_cenit"
fig.add_trace(go.Scatter3d(
    x=arco_ang_cenit[:, 0], y=arco_ang_cenit[:, 1], z=arco_ang_cenit[:, 2],
    mode="lines",
    line=dict(color="purple", width=4, dash="dot"),
    name="Azimut",
    legendgroup=grupo_cenit,
    showlegend=True
))
mid_cenit = arco_ang_cenit[len(arco_ang_cenit)//2]
fig.add_trace(go.Scatter3d(
    x=[mid_cenit[0]], y=[mid_cenit[1]], z=[mid_cenit[2]],
    mode="text",
    text=["Azimut"],
    showlegend=False,
    legendgroup=grupo_cenit,
    hoverinfo="skip"
))

# ---------- Ángulo Paraláctico ----------
grupo_estrella = "grupo_angulo_estrella"
fig.add_trace(go.Scatter3d(
    x=arco_ang_estrella[:, 0], y=arco_ang_estrella[:, 1], z=arco_ang_estrella[:, 2],
    mode="lines",
    line=dict(color="orange", width=4, dash="dot"),
    name="Ángulo Paraláctico",
    legendgroup=grupo_estrella,
    showlegend=True
))
mid_est = arco_ang_estrella[len(arco_ang_estrella)//2]
fig.add_trace(go.Scatter3d(
    x=[mid_est[0]], y=[mid_est[1]], z=[mid_est[2]],
    mode="text",
    text=["Ángulo Paraláctico"],
    showlegend=False,
    legendgroup=grupo_estrella,
    hoverinfo="skip"
))

# Layout
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode="data"
    ),
    legend=dict(groupclick="togglegroup"),
    margin=dict(l=0, r=0, t=30, b=0),
    height=700,
    title="Triángulo de Posición"
)

# -----------------------------
# Exportar a HTML
# -----------------------------
plot(fig, filename="TrianguloPosicion.html", auto_open=True)
