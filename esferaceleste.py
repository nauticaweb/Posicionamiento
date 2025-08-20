import numpy as np
import plotly.graph_objects as go

# --------------------------
# Función para generar esferas
# --------------------------
def create_sphere(radius=1, opacity=1, color='lightblue', show=True):
    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(0, np.pi, 30)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, color],[1, color]],
        opacity=opacity,
        showscale=False,
        visible=show
    )

# --------------------------
# Parámetros
# --------------------------
R_earth = 1.0
R_celestial = 3.0

# --------------------------
# Tierra y esfera celeste
# --------------------------
earth = create_sphere(radius=R_earth, opacity=1.0, color="blue", show=True)
celestial_sphere = create_sphere(radius=R_celestial, opacity=0.18, color="lightgrey", show=True)

# --------------------------
# Líneas base
# --------------------------
theta = np.linspace(0, 2*np.pi, 400)

# Ecuador celeste
x_eq = R_celestial * np.cos(theta)
y_eq = R_celestial * np.sin(theta)
z_eq = np.zeros_like(theta)
ecuador = go.Scatter3d(x=x_eq, y=y_eq, z=z_eq, mode="lines",
                       line=dict(color="red", width=4),
                       name="Ecuador Celeste", visible=False)

# Eje del mundo
eje = go.Scatter3d(x=[0,0], y=[0,0], z=[-R_celestial, R_celestial], mode="lines",
                   line=dict(color="green", width=4),
                   name="Eje del Mundo", visible=False)

# Meridiano de Greenwich
x_mer = R_celestial * np.cos(theta)
y_mer = np.zeros_like(theta)
z_mer = R_celestial * np.sin(theta)
greenwich = go.Scatter3d(x=x_mer, y=y_mer, z=z_mer, mode="lines",
                         line=dict(color="orange", width=4),
                         name="Meridiano Greenwich", visible=False)

# --------------------------
# Estrella (AR=45°, Dec=60°)
# --------------------------
alpha = np.deg2rad(45.0)
delta = np.deg2rad(60.0)
x_star = R_celestial * np.cos(delta) * np.cos(alpha)
y_star = R_celestial * np.cos(delta) * np.sin(alpha)
z_star = R_celestial * np.sin(delta)
estrella_point = go.Scatter3d(x=[x_star], y=[y_star], z=[z_star],
                              mode="markers", marker=dict(size=6, color="yellow"),
                              name="Estrella", visible=True)

# Paralelo de declinación
phi = np.linspace(0, 2*np.pi, 400)
x_par = R_celestial * np.cos(delta) * np.cos(phi)
y_par = R_celestial * np.cos(delta) * np.sin(phi)
z_par = np.ones_like(phi) * R_celestial * np.sin(delta)
paralelo_decl = go.Scatter3d(x=x_par, y=y_par, z=z_par, mode="lines",
                             line=dict(color="cyan", width=3, dash="dot"),
                             name="Paralelo Declinación", visible=False)

# Círculo horario (pasa por polos y estrella)
x_ch = R_celestial * np.cos(phi) * np.cos(alpha)
y_ch = R_celestial * np.cos(phi) * np.sin(alpha)
z_ch = R_celestial * np.sin(phi)
circulo_horario = go.Scatter3d(x=x_ch, y=y_ch, z=z_ch, mode="lines",
                               line=dict(color="magenta", width=3),
                               name="Círculo Horario", visible=False)

# --------------------------
# Observador (ejemplo: Madrid ~ 40°N, -3°)
# --------------------------
lat_obs = np.deg2rad(40.0)
lon_obs = np.deg2rad(-3.0)
x_obs = R_earth * np.cos(lat_obs) * np.cos(lon_obs)
y_obs = R_earth * np.cos(lat_obs) * np.sin(lon_obs)
z_obs = R_earth * np.sin(lat_obs)

observador = go.Scatter3d(x=[x_obs], y=[y_obs], z=[z_obs],
                          mode="markers", marker=dict(size=5, color="white"),
                          name="Observador", visible=True)

# Vector unitario cenit del observador
n_obs = np.array([x_obs, y_obs, z_obs], dtype=float)
n_obs /= np.linalg.norm(n_obs)

# Eje Cenit-Nadir
cenit_vec = R_celestial * n_obs
nadir_vec = -R_celestial * n_obs
zenit_nadir = go.Scatter3d(x=[nadir_vec[0], cenit_vec[0]],
                           y=[nadir_vec[1], cenit_vec[1]],
                           z=[nadir_vec[2], cenit_vec[2]],
                           mode="lines", line=dict(color="purple", width=4),
                           name="Eje Cenit-Nadir", visible=False)

# --------------------------
# Horizonte del observador (plano ⟂ n_obs)
# --------------------------
t = np.linspace(0, 2*np.pi, 400)
b1 = np.cross(n_obs, np.array([0.0, 0.0, 1.0]))
if np.linalg.norm(b1) < 1e-8:
    b1 = np.cross(n_obs, np.array([0.0, 1.0, 0.0]))
b1 /= np.linalg.norm(b1)
b2 = np.cross(n_obs, b1)
b2 /= np.linalg.norm(b2)

x_h = R_celestial * (np.cos(t)*b1[0] + np.sin(t)*b2[0])
y_h = R_celestial * (np.cos(t)*b1[1] + np.sin(t)*b2[1])
z_h = R_celestial * (np.cos(t)*b1[2] + np.sin(t)*b2[2])
horizonte = go.Scatter3d(x=x_h, y=y_h, z=z_h, mode="lines",
                         line=dict(color="brown", width=3),
                         name="Horizonte", visible=False)

# --------------------------
# Almicantarat
# --------------------------
star_unit = np.array([x_star, y_star, z_star], dtype=float) / R_celestial
h_star = float(np.dot(star_unit, n_obs))
r_small = R_celestial * np.sqrt(max(0.0, 1.0 - h_star**2))
centro_alm = R_celestial * h_star * n_obs
x_alm = centro_alm[0] + r_small*(np.cos(t)*b1[0] + np.sin(t)*b2[0])
y_alm = centro_alm[1] + r_small*(np.cos(t)*b1[1] + np.sin(t)*b2[1])
z_alm = centro_alm[2] + r_small*(np.cos(t)*b1[2] + np.sin(t)*b2[2])
almicantarat = go.Scatter3d(x=x_alm, y=y_alm, z=z_alm, mode="lines",
                            line=dict(color="blue", width=3, dash="dot"),
                            name="Almicantarat", visible=False)

# --------------------------
# Vertical
# --------------------------
normal_vertical = np.cross(n_obs, star_unit)
norm_nv = np.linalg.norm(normal_vertical)
if norm_nv < 1e-8:
    normal_vertical = np.cross(n_obs, np.array([1.0, 0.0, 0.0]))
    norm_nv = np.linalg.norm(normal_vertical)
normal_vertical /= norm_nv

e1 = star_unit / np.linalg.norm(star_unit)
e2 = np.cross(normal_vertical, e1)
e2 /= np.linalg.norm(e2)
x_vert = R_celestial * (np.cos(t)*e1[0] + np.sin(t)*e2[0])
y_vert = R_celestial * (np.cos(t)*e1[1] + np.sin(t)*e2[1])
z_vert = R_celestial * (np.cos(t)*e1[2] + np.sin(t)*e2[2])
vertical = go.Scatter3d(x=x_vert, y=y_vert, z=z_vert, mode="lines",
                        line=dict(color="lime", width=3),
                        name="Vertical", visible=False)

# --------------------------
# Eclíptica
# --------------------------
epsilon = np.deg2rad(23.44)
theta_ecl = np.linspace(0, 2*np.pi, 400)
x_ecl = R_celestial * np.cos(theta_ecl)
y_ecl = R_celestial * np.sin(theta_ecl)
z_ecl = np.zeros_like(theta_ecl)
x_rot = x_ecl
y_rot = y_ecl * np.cos(epsilon) - z_ecl * np.sin(epsilon)
z_rot = y_ecl * np.sin(epsilon) + z_ecl * np.cos(epsilon)
ecliptica = go.Scatter3d(x=x_rot, y=y_rot, z=z_rot,
                         mode="lines",
                         line=dict(color="gold", width=4, dash="dash"),
                         name="Eclíptica", visible=False)

# --------------------------
# Meridiano del Observador (corregido)
# --------------------------
p_norte = np.array([0,0,R_celestial])
p_sur = np.array([0,0,-R_celestial])
obs_vec_unit = n_obs
v1 = p_norte
v2 = obs_vec_unit
n_plane = np.cross(v1, v2)
n_plane /= np.linalg.norm(n_plane)
e1_m = v1 / np.linalg.norm(v1)
e2_m = np.cross(n_plane, e1_m)
e2_m /= np.linalg.norm(e2_m)
theta_m = np.linspace(0, 2*np.pi, 400)
x_mer_obs = R_celestial * (np.cos(theta_m)*e1_m[0] + np.sin(theta_m)*e2_m[0])
y_mer_obs = R_celestial * (np.cos(theta_m)*e1_m[1] + np.sin(theta_m)*e2_m[1])
z_mer_obs = R_celestial * (np.cos(theta_m)*e1_m[2] + np.sin(theta_m)*e2_m[2])
meridiano_obs = go.Scatter3d(x=x_mer_obs, y=y_mer_obs, z=z_mer_obs,
                             mode="lines",
                             line=dict(color="darkblue", width=3, dash="dot"),
                             name="Meridiano Observador",
                             visible=False)

# --------------------------
# Puntos resaltados
# --------------------------
polo_norte_point = go.Scatter3d(
    x=[0], y=[0], z=[R_celestial],
    mode="markers", marker=dict(size=8, color="red"),
    name="Polo Norte", visible=False
)
cenit_point = go.Scatter3d(
    x=[cenit_vec[0]], y=[cenit_vec[1]], z=[cenit_vec[2]],
    mode="markers", marker=dict(size=8, color="purple"),
    name="Cenit", visible=False
)
estrella_point_resaltada = go.Scatter3d(
    x=[x_star], y=[y_star], z=[z_star],
    mode="markers", marker=dict(size=8, color="yellow", symbol="diamond"),
    name="Estrella Resaltada", visible=False
)

# --------------------------
# Figura completa
# --------------------------
fig = go.Figure(data=[
    estrella_point,      # 1
    eje,                 # 2
    ecuador,             # 3
    greenwich,           # 4
    paralelo_decl,       # 5
    circulo_horario,     # 6
    observador,          # 7
    zenit_nadir,         # 8
    horizonte,           # 9
    meridiano_obs,       #10
    almicantarat,        #11
    vertical,            #12
    ecliptica,           #13
    earth,               #14
    celestial_sphere,    #15
    polo_norte_point,    #16
    cenit_point,         #17
    estrella_point_resaltada  #18
])

# --------------------------
# Visibilidad por defecto
# --------------------------
visible_all = [True]*len(fig.data)
visible_clear = [False]*len(fig.data)
for idx in [0, 6, 13, 14]:  # estrella, observador, tierra y esfera
    visible_clear[idx] = True

# --------------------------
# Menú de botones
# --------------------------
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode="data"
    ),
    margin=dict(l=0, r=0, b=0, t=30),
    updatemenus=[dict(
        type="buttons",
        direction="left",
        buttons=[
            dict(label="Mostrar todo", method="update", args=[{"visible": visible_all}]),
            dict(label="Borrar todo", method="update", args=[{"visible": visible_clear}]),
            dict(label="Resaltar puntos", method="update", args=[{"visible":[True if i in [-3,-2,-1] else False for i in range(len(fig.data))]}])
        ],
        x=0.02, y=-0.12,
        pad=dict(r=8, t=8),
        showactive=False
    )]
)

# --------------------------
# Exportar a HTML
# --------------------------
fig.write_html("esfera_celeste.html")
print("✅ Archivo generado: esfera_celeste.html")
