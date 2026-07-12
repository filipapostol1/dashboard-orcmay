import streamlit as st
import pandas as pd
from orchestrator import BusinessDataOrchestrator

# 1. LA CONFIGURAZIONE DELLA PAGINA (Deve essere tassativamente la prima istruzione Streamlit)
st.set_page_config(page_title="CEO Dashboard", page_icon="💼", layout="wide")

st.title("💼 CEO Business Orchestrator - PRO")

# 2. RECUPERO DATI PROTETTO DA CRASH (Tolleranza totale)
try:
    motore = BusinessDataOrchestrator(company_name="Orchestra Holding")
    
    dati_finanza = motore.fetch_financial_data()
    dati_mktg = motore.fetch_marketing_data()
    dati_trend = motore.fetch_market_trends()
    report = motore.elabora_metriche_avanzate(dati_finanza, dati_mktg, dati_trend)
except Exception as e:
    st.error(f"Impossibile comunicare con l'orchestratore: {e}")
    report = {}

# 🔍 RIGA DI ISPEZIONE FONDAMENTALE (Ci dice esattamente cosa risponde il motore)
st.write("### 🔍 Ispezione Dati in Tempo Reale", report)

# 3. FUNZIONE ESTRATTORE FLESSIBILE
def estrai(dizionario, *chiavi):
    valore = dizionario
    for chiave in chiavi:
        if isinstance(valore, dict) and chiave in valore:
            valore = valore[chiave]
        else:
            return "N/D"
    return valore

# 4. STRUTTURA DELLE METRICHE A SCHERMO
st.subheader("📊 Indicatori di Performance")
col1, col2, col3 = st.columns(3)

# Estrazione sicura preventiva
tot_vendite = estrai(report, 'finanze', 'totale_vendite')
tot_ordini = estrai(report, 'finanze', 'totale_ordini')
val_aov = estrai(report, 'finanze', 'aov')

with col1:
    st.metric(
        label="Vendite Totali", 
        value=f"{tot_vendite} €" if tot_vendite != "N/D" else "N/D"
    )
with col2:
    st.metric(
        label="Ordini Ricevuti", 
        value=tot_ordini
    )
with col3:
    st.metric(
        label="AOV (Ordine Medio)", 
        value=f"{val_aov} €" if val_aov != "N/D" else "N/D"
    )

st.subheader("📈 Analisi Trend")
st.info("Sistema difensivo attivo. Se le metriche sopra mostrano 'N/D', guarda il riquadro di Ispezione Dati per vedere quali chiavi esatte sta generando il tuo orchestratore.")
