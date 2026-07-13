import streamlit as st
import pandas as pd
import json
import os

# Configurazione della pagina
st.set_page_config(page_title="E-com Intelligence Dashboard", layout="wide")

# --- FUNZIONE DI SOLA LETTURA ---
def carica_dati_calcolati():
    nome_file = "report_orchestra_holding.json"
    
    # Se il file non esiste ancora, creiamo una struttura di sicurezza per non far crashare il sito
    if not os.path.exists(nome_file):
        return {
            "metriche_finanziarie": {"mrr_netto_stimato": 0, "ltv_stimato": 0, "valore_totale_attivi": 0},
            "performance_marketing_reale": {"efficienza_pubblicitaria_roi": "0%", "costo_acquisizione_cliente_cac_euro": 0, "tasso_conversione_sito": "0%"},
            "dati_per_grafici": {"storico_vendite": [], "storico_competitor": []}
        }
        
    with open(nome_file, "r", encoding="utf-8") as f:
        return json.load(f)

# Carica i dati dal file JSON condiviso
dati = carica_dati_calcolati()

# --- SIDEBAR (Navigazione) ---
st.sidebar.title("🚀 E-com Intel")
st.sidebar.write("Account: **Orchestra Holding**")
status = st.sidebar.selectbox("Livello Account", ["PIANO BASE", "PIANO PRO"])
menu = st.sidebar.radio("Navigazione", ["📈 Panoramica Store", "🕵️ Spia Competitor"])

# --- SEZIONE 1: PANORAMICA STORE ---
if menu == "📈 Panoramica Store":
    st.title("📈 Panoramica del tuo E-commerce")
    st.write("Dati estratti in tempo reale da Shopify e pre-elaborati.")
    
    # KPI Principali recuperati dal JSON
    finanza = dati.get("metriche_finanziarie", {})
    mktg = dati.get("performance_marketing_reale", {})
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fatturato Lordo", f"{finanza.get('mrr_netto_stimato', 0)} €")
    col2.metric("Ordini Totali", f"{finanza.get('valore_totale_attivi', 0)}")
    col3.metric("CAC", f"{mktg.get('costo_acquisizione_cliente_cac_euro', 0)} €")
    col4.metric("ROI ADS", f"{mktg.get('efficienza_pubblicitaria_roi', '0%')}")
    
    st.markdown("---")
    
    # --- GRAFICO VENDITE REALI DA SHOPIFY ---
    st.subheader("📊 Andamento Fatturato Giornaliero")
    storico_vendite = dati.get("dati_per_grafici", {}).get("storico_vendite", [])
    
    if storico_vendite:
        df_vendite = pd.DataFrame(storico_vendite).set_index("data")
        # Mostra il grafico a linee del fatturato
        st.line_chart(df_vendite["fatturato"])
    else:
        st.info("Nessun dato storico disponibile al momento.")

# --- SEZIONE 2: SPIA COMPETITOR ---
elif menu == "🕵️ Spia Competitor":
    st.title("🕵️ Intelligence Competitor")
    
    storico_comp = dati.get("dati_per_grafici", {}).get("storico_competitor", [])
    
    if storico_comp:
        df_comp = pd.DataFrame(storico_comp).set_index("data")
        
        if status == "PIANO BASE":
            st.error("🔒 Questa sezione è limitata nel Piano Base. Puoi tracciare solo 3 competitor.")
            # Nel piano base mostriamo solo la tabella semplice
            st.dataframe(df_comp)
        else:
            st.success("🔓 Accesso PRO: Grafici Interattivi e Algoritmo Predittivo Attivo")
            # Nel piano pro sblocchiamo il grafico a linee con il confronto dei prezzi
            st.line_chart(df_comp)
    else:
        st.info("Nessun dato sui competitor disponibile.")
