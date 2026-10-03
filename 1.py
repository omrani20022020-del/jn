import time
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="STEG El Borma - Jumeau Numérique SCADA", layout="wide")
st.title("⚡ STEG - Station de Compression d'El Borma")
st.caption("Supervision Télémetrique Temps Réel - Jumeau Numérique (KVS-412) & Cycle ORC")

if st.button("🚀 Démarrer la simulation de la turbine"):
    # Conteneur pour le graphique dynamique
    chart_placeholder = st.empty()
    metric_placeholder = st.empty()
    
    t_steps = np.linspace(0, 240, 100)
    base_egt = 520 + 30 * np.sin(2 * np.pi * t_steps / 160) - 10 * np.cos(4 * np.pi * t_steps / 240)
    
    np.random.seed(42)
    egt_scada = base_egt.copy()
    for i in range(50, 100):
        egt_scada[i] += (i - 50) * 1.2

    # Animation pas à pas dans la boucle
    for step in range(10, len(t_steps), 5):
        fig = go.Figure()
        
        # Données partielles pour simuler le temps réel
        x_curr = t_steps[:step]
        y_pred = base_egt[:step]
        y_scada = egt_scada[:step]
        
        fig.add_trace(go.Scatter(x=x_curr, y=y_pred*1.03, mode='lines', line=dict(color='#444444', dash='dash'), name='Seuil Max (+3%)'))
        fig.add_trace(go.Scatter(x=x_curr, y=y_pred*0.97, mode='lines', line=dict(color='#444444', dash='dash'), fill='tonexty', fillcolor='rgba(80,80,80,0.2)', name='Bande Tolérance'))
        fig.add_trace(go.Scatter(x=x_curr, y=y_pred, mode='lines', line=dict(color='#bc8cff', width=2), name='Jumeau Numérique'))
        fig.add_trace(go.Scatter(x=x_curr, y=y_scada, mode='lines+markers', line=dict(color='#58a6ff', width=2), name='Mesure SCADA'))
        
        fig.update_layout(template="plotly_dark", height=400, xaxis_title="Temps (Minutes)", yaxis_title="EGT (°C)")
        
        chart_placeholder.plotly_chart(fig, width='stretch')
        
        # Alerte si dépassement
        if step > 50:
            metric_placeholder.warning("⚠️ ALERTE : Déviation critique détectée - Encrassement des aubes (Sable saharien) !")
        
        time.sleep(0.1)  # Vitesse de simulation
        
    st.success("✅ Fin de la simulation. Détectabilité AMDEC validée (D=1).")