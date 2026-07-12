import streamlit as st
import pandas as pd
from orchestrator import BusinessDataOrchestrator

# 1. Configurazione della pagina
st.set_page_config(page_title="CEO Dashboard", page_icon="💼", layout="wide")

st.title("💼 CEO Business Orchestrator - PRO")

# 2. Recupero dati sicuro
try:
    motore = BusinessDataOrchestrator(company_name="Orchestra Holding")
    
    dati_finanza = motore.fetch_financial_data()
    dati_mktg = motore.fetch_marketing_data()
    dati_trend = motore.fetch_market_trends()
    report = motore.elabora_metriche_avanzate(dati_finanza, dati_mktg, dati_trend)
except Exception as e:
    st.error(f"Impossibile comunicare con l'orchestratore: {e}")
    report = {}

# 3. Funzione estrattore flessibile (Evita i crash)
def estrai(dizionario, *chiavi):
    valore = dizionario
    for chiave in chiavi:
        if isinstance(valore, dict) and chiave in valore:
            valore = valore[chiave]
        else:
            return "N/D"
    return valore

# --- LAYOUT DASHBOARD REALE MAPPATO SUI TUOI DATI ---

# SEZIONE 1: METRICHE FINANZIARIE
st.subheader("📊 Metriche Finanziarie")
col1, col2, col3 = st.columns(3)

mrr = estrai(report, 'metriche_finanziarie', 'mrr_netto_stimato')
ltv = estrai(report, 'metriche_finanziarie', 'ltv_stimato')
attivi = estrai(report, 'metriche_finanziarie', 'valore_totale_attivi')

with col1:
    st.metric(label="MRR Netto Stimato", value=f"{mrr} €" if mrr != "N/D" else "N/D")
with col2:
    st.metric(label="LTV Stimato", value=f"{ltv} €" if ltv != "N/D" else "N/D")
with col3:
    st.metric(label="Valore Totale Attivi", value=attivi)

st.markdown("---")

# SEZIONE 2: PERFORMANCE MARKETING
st.subheader("📢 Performance Marketing & Conversioni")
col4, col5, col6 = st.columns(3)

roi = estrai(report, 'performance_marketing_reale', 'efficienza_pubblicitaria_roi')
cac = estrai(report, 'performance_marketing_reale', 'costo_acquisizione_cliente_cac_euro')
tasso_conv = estrai(report, 'performance_marketing_reale', 'tasso_conversione_sito')

with col4:
    st.metric(label="ROI Pubblicitario (Efficienza)", value=roi)
with col5:
    st.metric(label="CAC (Costo Acq. Cliente)", value=f"{cac} €" if cac != "N/D" else "N/D")
with col6:
    st.metric(label="Tasso Conversione Sito", value=tasso_conv)

st.markdown("---")

# SEZIONE 3: CONTESTO ESTERNO E GOVERNANCE
st.subheader("🌐 Analisi Contesto & Asset")
col7, col8, col9 = st.columns(3)

salute = estrai(report, 'indicatori_ceo', 'stato_salute_asset')
trend = estrai(report, 'analisi_contesto_esterno', 'trend_mercato')
bench = estrai(report, 'analisi_contesto_esterno', 'benchmark_prezzo_concorrenza_euro')

with col7:
    st.metric(label="Stato Salute Asset (CEO)", value=salute)
with col8:
    st.metric(label="Trend di Mercato", value=trend)
with col9:
    st.metric(label="Benchmark Concorrenza", value=f"{bench} €" if bench != "N/D" else "N/D")
