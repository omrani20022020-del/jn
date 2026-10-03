import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# --- Simulation ou récupération de tes données de télémétrie ---
# (Ici, on génère un jeu de données simulant l'effet du sable sur l'EGT au fil du temps)
np.random.seed(42)
temps_heures = np.linspace(0, 500, 100)  # Heures de fonctionnement
deg_sable = np.linspace(0, 10, 100)  # Indice d'encrassement par le sable (%)

# Création d'une grille 2D pour un bel effet de surface 3D
T, S = np.meshgrid(temps_heures, deg_sable)
# Modélisation physique simplifiée : l'EGT augmente avec le temps et l'encrassement
EGT = 520 + 0.08 * T + 3.5 * S + np.random.normal(0, 1, T.shape)

# Aplatissement pour Plotly Express (ou utilisation de graph_objects pour une surface)
df_3d = pd.DataFrame(
    {
        "Temps (heures)": T.flatten(),
        "Dégradation Sable (%)": S.flatten(),
        "EGT (°C)": EGT.flatten(),
    }
)

# --- Affichage dans Streamlit ---
st.markdown("### 📊 Analyse 3D : Temps vs Dégradation Sable vs EGT")
st.markdown(
    "Ce graphique interactif met en évidence l'impact de l'encrassement des aubes par le sable sur l'élévation de la température des gaz d'échappement (EGT)."
)

import plotly.graph_objects as go

fig = go.Figure(
    data=[
        go.Surface(
            z=EGT,
            x=T,
            y=S,
            colorscale="Plasma",
        )
    ]
)

fig.update_layout(
    title="Surface de Réponse : Évolution de l'EGT",
    scene=dict(
        xaxis_title="Temps (h)",
        yaxis_title="Dégradation Sable (%)",
        zaxis_title="EGT (°C)",
    ),
    autosize=True,
    margin=dict(l=65, r=50, b=65, t=90),
)

st.plotly_chart(fig, use_container_width=True)
# Amélioration du design pour s'adapter au thème sombre/clair
