import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="STEG El Borma - Jumeau Numérique", layout="wide")

st.title("⚡ STEG - Station de Compression d'El Borma")
st.caption("Supervision Télémetrique Temps Réel - Jumeau Numérique (KVS-412) & Cycle ORC")

# Création de deux onglets pour structurer l'affichage
tab1, tab2 = st.tabs(["🔀 Synoptique & Réaction des Composants", "📈 Courbes de Télémesure & EGT"])

with tab1:
    st.subheader("Vue Synoptique du Circuit et État des Composants")
    
    # Optionnel : Afficher l'image du schéma si elle est présente dans le dossier
    try:
        st.image("schema_steg.png", caption="Schéma P&ID - Station de Compression KVS-412 & ORC", use_column_width=True)
    except:
        st.info("💡 Astuce : Ajoute une image nommée 'schema_steg.png' dans ton dossier pour l'afficher ici.")

    st.markdown("---")
    
    # Cartes d'état en temps réel pour montrer comment réagit chaque composant
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**1. Turbine à Gaz KVS-412**")
        st.write("- **Régime :** 95% Nnom")
        st.write("- **Température EGT :** 565 °C")
        st.warning("⚠️ État : Alerte encrassement aubes (Sable)")
        
    with col2:
        st.info("**2. Compresseur de Gaz**")
        st.write("- **Pression Amont :** 25 bar")
        st.write("- **Pression Aval :** 58 bar")
        st.success("✅ État : Fonctionnement nominal")
        
    with col3:
        st.info("**3. Cycle ORC (Récupération)**")
        st.write("- **Source Chaude :** Gaz d'échappement")
        st.write("- **Puissance Récupérée :** 1.2 MW")
        st.success("✅ État : Optimisation active")

with tab2:
    st.subheader("Simulation et Analyse de la Température d'Échappement (EGT)")
    
    if st.button("🚀 Lancer la simulation de la turbine"):
        chart_placeholder = st.empty()
        metric_placeholder = st.empty()
        
        t_steps = np.linspace(0, 240, 100)
        base_egt = 520 + 30 * np.sin(2 * np.pi * t_steps / 160) - 10 * np.cos(4 * np.pi * t_steps / 240)
        
        np.random.seed(42)
        egt_scada = base_egt.copy()
        for i in range(50, 100):
            egt_scada[i] += (i - 50) * 1.2

        for step in range(10, len(t_steps), 5):
            fig = go.Figure()
            x_curr = t_steps[:step]
            y_pred = base_egt[:step]
            y_scada = egt_scada[:step]
            
            fig.add_trace(go.Scatter(x=x_curr, y=y_pred*1.03, mode='lines', line=dict(color='#444444', dash='dash'), name='Seuil Max (+3%)'))
            fig.add_trace(go.Scatter(x=x_curr, y=y_pred*0.97, mode='lines', line=dict(color='#444444', dash='dash'), fill='tonexty', fillcolor='rgba(80,80,80,0.2)', name='Bande Tolérance'))
            fig.add_trace(go.Scatter(x=x_curr, y=y_pred, mode='lines', line=dict(color='#bc8cff', width=2), name='Jumeau Numérique'))
            fig.add_trace(go.Scatter(x=x_curr, y=y_scada, mode='lines+markers', line=dict(color='#58a6ff', width=2), name='Mesure SCADA'))
            
            fig.update_layout(template="plotly_dark", height=400, xaxis_title="Temps (Minutes)", yaxis_title="EGT (°C)")
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            
            if step > 50:
                metric_placeholder.warning("⚠️ ALERTE : Déviation critique détectée - Encrassement des aubes par le sable saharien !")
            
            time.sleep(0.1)
            
        st.success("✅ Fin de la simulation. Détectabilité AMDEC validée (D=1).")
