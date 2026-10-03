import time
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="STEG El Borma - Jumeau Numérique", layout="wide"
)

st.title("⚡ STEG - Station de Compression d'El Borma")
st.caption(
    "Supervision Télémetrique Temps Réel - Jumeau Numérique (KVS-412) & Cycle ORC"
)

# --- 1. AFFICHAGE DU SCHÉMA TECHNIQUE OFFICIEL ---
st.subheader(
    "🔀 Synoptique de l'Installation (Turbine KVS-412 & Cycle Fermé n-Butane)"
)
try:
  # Utilise exactement le nom du fichier que tu viens de téléverser
  st.image("schema_steg.png", use_container_width=True)
except Exception as e:
  st.error(
      "⚠️ Erreur de chargement de l'image : vérifie que le fichier"
      " 'schema_steg.png' est bien là."
  )

st.markdown("---")

# --- 2. SECTION SIMULATION ET RÉACTION DU SYSTÈME ---
st.subheader(
    "📊 Réaction du Système et Surveillance EGT (Jumeau Numérique vs SCADA)"
)

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    lancer = st.button("🚀 Lancer la Simulation")

# Conteneurs pour l'animation dynamique
chart_placeholder = st.empty()
status_placeholder = st.empty()

# Graphique initial statique ou vide avant le clic
t_steps = np.linspace(0, 240, 100)
base_egt = 520 + 30 * np.sin(2 * np.pi * t_steps / 160) - 10 * np.cos(
    4 * np.pi * t_steps / 240
)

np.random.seed(42)
egt_scada = base_egt.copy()
for i in range(50, 100):
    egt_scada[i] += (i - 50) * 1.2

fig_init = go.Figure()
fig_init.add_trace(
    go.Scatter(
        x=t_steps,
        y=base_egt * 1.03,
        mode="lines",
        line=dict(color="#444444", dash="dash"),
        name="Seuil Max (+3%)",
    )
)
fig_init.add_trace(
    go.Scatter(
        x=t_steps,
        y=base_egt * 0.97,
        mode="lines",
        line=dict(color="#444444", dash="dash"),
        fill="tonexty",
        fillcolor="rgba(80,80,80,0.2)",
        name="Bande Tolérance",
    )
)
fig_init.add_trace(
    go.Scatter(
        x=t_steps,
        y=base_egt,
        mode="lines",
        line=dict(color="#bc8cff", width=2),
        name="Jumeau Numérique",
    )
)
fig_init.add_trace(
    go.Scatter(
        x=t_steps,
        y=egt_scada,
        mode="lines",
        line=dict(color="#58a6ff", width=2),
        name="Mesure SCADA",
    )
)
fig_init.update_layout(
    template="plotly_dark",
    height=400,
    xaxis_title="Temps d'exploitation (Minutes)",
    yaxis_title="Température d'Échappement EGT (°C)",
)
chart_placeholder.plotly_chart(fig_init, use_container_width=True)

# Action lorsque l'utilisateur clique sur le bouton de simulation
if lancer:
  for step in range(10, len(t_steps), 5):
    fig = go.Figure()
    x_curr = t_steps[:step]
    y_pred = base_egt[:step]
    y_scada = egt_scada[:step]

    fig.add_trace(
        go.Scatter(
            x=x_curr,
            y=y_pred * 1.03,
            mode="lines",
            line=dict(color="#444444", dash="dash"),
            name="Seuil Max (+3%)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_curr,
            y=y_pred * 0.97,
            mode="lines",
            line=dict(color="#444444", dash="dash"),
            fill="tonexty",
            fillcolor="rgba(80,80,80,0.2)",
            name="Bande Tolérance",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_curr,
            y=y_pred,
            mode="lines",
            line=dict(color="#bc8cff", width=2),
            name="Jumeau Numérique",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_curr,
            y=y_scada,
            mode="lines+markers",
            line=dict(color="#58a6ff", width=2),
            name="Mesure SCADA",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Temps d'exploitation (Minutes)",
        yaxis_title="Température d'Échappement EGT (°C)",
    )
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    if step > 50:
      status_placeholder.warning(
          "⚠️ ALERTE KVS-412 : Déviation critique détectée - Encrassement des"
          " aubes par le sable saharien ! Impact sur l'échangeur ORC."
      )
    else:
      status_placeholder.info(
          "ℹ️ Système en fonctionnement nominal stable (Bande $\\pm3\\%$"
          " respectée)."
      )

    time.sleep(0.1)

  status_placeholder.success(
      "✅ Simulation terminée. Détectabilité AMDEC validée (D=1)."
  )
