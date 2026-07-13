import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="E-com Intelligence Dashboard", layout="wide")

def carica_pacchetto_dashboard():
    nome_file = "dati_dashboard.json"
    if not os.path.exists(nome_file):
        return {
            "PIANO BASE": {"kpi": {}, "storico_vendite": [], "storico_competitor": []},
            "PIANO PRO": {"kpi": {}, "storico_vendite": [], "storico_competitor": []}
        }
    with open(nome_file, "r", encoding="utf-8") as f:
        return json.load(f)

dati_sito = carica_pacchetto_dashboard()

# --- SIDEBAR ---
st.sidebar.title("🚀 E-com Intel")
status = st.sidebar.selectbox("Livello Account", ["PIANO BASE", "PIANO PRO"])
menu = st.sidebar.radio("Navigazione", ["📈 Panoramica Store", "🕵️ Spia Competitor"])

# Estraiamo direttamente il pacchetto dati già pre-tagliato dall'orchestratore per quel piano
dati_piano = dati_sito.get(status, {})
kpi = dati_piano.get("kpi", {})

# --- SEZIONE 1: PANORAMICA STORE ---
if menu == "📈 Panoramica Store":
    st.title(f"📈 Panoramica dello Store ({status})")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fatturato", f"{kpi.get('fatturato', 0)} €")
    col2.metric("Ordini", f"{kpi.get('ordini', 0)}")
    col3.metric("CAC", f"{kpi.get('cac', 0)} €")
    col4.metric("ROI", f"{kpi.get('roi', '0%')}")
    
    st.markdown("---")
    st.subheader("📊 Andamento Fatturato")
    
    storico_v = dati_piano.get("storico_vendite", [])
    if storico_v:
        df_v = pd.DataFrame(storico_v).set_index("data")
        st.line_chart(df_v["fatturato"])
    else:
        st.info("Nessun dato storico elaborato per questo profilo.")

# --- SEZIONE 2: SPIA COMPETITOR ---
elif menu == "🕵️ Spia Competitor":
    st.title(f"🕵️ Intelligence Competitor ({status})")
    
    storico_c = dati_piano.get("storico_competitor", [])
    if storico_c:
        df_c = pd.DataFrame(storico_c).set_index("data")
        
        if status == "PIANO BASE":
            st.warning("🔒 Versione limitata: Storico ridotto a 48 ore e competitor parziali.")
            st.dataframe(df_c)
        else:
            st.success("🔓 Modalità PRO: Storico temporale completo e tracciamento globale attivo.")
            st.line_chart(df_c)
            st.dataframe(df_c)
    else:
        st.info("Nessun dato competitor elaborato per questo profilo.")
