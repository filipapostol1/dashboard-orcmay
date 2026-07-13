import streamlit as st
import pandas as pd
import json
import os

# Importiamo l'orchestratore in modo pulito: la logica rimane di là, noi la "chiamiamo" solo.
try:
    from orchestrator import BusinessDataOrchestrator
except ImportError:
    st.error("⚠️ File orchestrator.py non trovato. Assicurati che sia nella stessa cartella.")
    st.stop()

st.set_page_config(page_title="E-com Intelligence Dashboard", layout="wide")

nome_file = os.path.join(os.getcwd(), "dati_dashboard.json")

# --- MOTORE DI AGGIORNAMENTO IN BACKGROUND ---
def aggiorna_tutto():
    motore = BusinessDataOrchestrator()
    dati_f = motore.fetch_financial_data()
    dati_m = motore.fetch_marketing_data()
    dati_t = motore.fetch_market_trends()
    motore.genera_output_sistemi(dati_f, dati_m, dati_t)

# Se il file non esiste, lo crea in automatico senza chiedertelo
if not os.path.exists(nome_file):
    with st.spinner("Prima configurazione in corso... Connessione a Shopify..."):
        aggiorna_tutto()

# --- FUNZIONE DI LETTURA ---
def carica_pacchetto_dashboard():
    try:
        with open(nome_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# --- SIDEBAR E COMANDI ---
st.sidebar.title("🚀 E-com Intel")
status = st.sidebar.selectbox("Livello Account", ["PIANO BASE", "PIANO PRO"])

# IL PULSANTE MAGICO: Tu clicchi, lui aggiorna tutto in background
if st.sidebar.button("🔄 Sincronizza Dati Ora"):
    with st.spinner("Scaricamento nuovi ordini e prezzi..."):
        aggiorna_tutto()
    st.sidebar.success("Dati aggiornati!")
    st.rerun()  # Ricarica la pagina coi dati freschi

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigazione", ["📈 Panoramica Store", "🕵️ Spia Competitor"])

dati_sito = carica_pacchetto_dashboard()

if not dati_sito:
    st.error("⚠️ Impossibile leggere i dati. Riprova la sincronizzazione.")
    st.stop()

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
            st.warning("🔒 Versione limitata: Storico ridotto a 48 ore e 1 solo competitor visibile.")
            st.dataframe(df_c, use_container_width=True)
        else:
            st.success("🔓 Modalità PRO: Storico temporale completo e tracciamento globale attivo.")
            st.line_chart(df_c)
            st.dataframe(df_c, use_container_width=True)
    else:
        st.info("Nessun dato competitor elaborato per questo profilo.")
