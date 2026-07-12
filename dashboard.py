import streamlit as st
import pandas as pd
from orchestrator import BusinessDataOrchestrator

# Configurazione della dashboard
st.set_page_config(page_title="CEO Dashboard", page_icon="💼")
st.title("💼 CEO Business Orchestrator - PRO")
st.write("Dati estratti dal motore:", report)

# Recupero dati sicuro dall'orchestratore
try:
    # Mettiamo l'inizializzazione DENTRO il try, così non crasha se il token o la connessione falliscono
    motore = BusinessDataOrchestrator(company_name="Orchestra Holding")
    
    dati_finanza = motore.fetch_financial_data()
    dati_mktg = motore.fetch_marketing_data()
    dati_trend = motore.fetch_market_trends()
    report = motore.elabora_metriche_avanzate(dati_finanza, dati_mktg, dati_trend)
except Exception as e:
    st.error(f"Impossibile comunicare con l'orchestratore: {e}")
    report = {}

# Funzione flessibile per estrarre i dati senza crashare (mostra N/D)
def estrai(dizionario, *chiavi):
    valore = dizionario
    for chiave in chiavi:
        if isinstance(valore, dict) and chiave in valore:
            valore = valore[chiave]
        else:
            return "N/D"
    return valore

# --- LAYOUT DASHBOARD ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Vendite Totali", value=f"{estrai(report, 'finanze', 'totale_vendite')} €")
with col2:
    st.metric(label="Ordini Ricevuti", value=estrai(report, "finanze", "totale_ordini"))
with col3:
    st.metric(label="AOV (Ordine Medio)", value=f"{estrai(report, 'finanze', 'aov')} €")

st.subheader("📈 Analisi Trend")
st.info("I dati flessibili sono pronti. Se Shopify non risponde, le metriche mostreranno N/D senza bloccare la pagina.")
