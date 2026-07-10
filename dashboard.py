import streamlit as st
import pandas as pd
from orchestrator import BusinessDataOrchestrator

# Configurazione della dashboard
st.set_page_config(page_title="CEO Dashboard", page_icon="💼")
st.title("💼 CEO Business Orchestrator - PRO")

# Inizializza il motore
motore = BusinessDataOrchestrator(company_name="Orchestra Holding")

# Recupero dati sicuro dall'orchestratore
try:
    dati_finanza = motore.fetch_financial_data()
    dati_mktg = motore.fetch_marketing_data()
    dati_trend = motore.fetch_market_trends()
    report = motore.elabora_metriche_avanzate(dati_finanza, dati_mktg, dati_trend)
except Exception as e:
    st.error(f"Impossibile comunicare con l'orchestratore: {e}")
    report = {}

# --- L'ADATTATORE INTELLIGENTE (Mappato sullo screenshot) ---
def estrai(dizionario, *chiavi):
    valore = dizionario
    for chiave in chiavi:
        if isinstance(valore, dict) and chiave in valore:
            valore = valore[chiave]
        else:
            return "N/D"
    return valore

# Estrazione chirurgica basata sul tuo JSON reale
entrate_lorde = estrai(report, 'quadro_finanziario', 'entrate_lorde_euro')
utile_netto = estrai(report, 'quadro_finanziario', 'utile_netto_stimato_euro')
abbonati_attivi = estrai(report, 'quadro_finanziario', 'metriche_abbonati', 'totale_attivi')

# Marketing e Trend (che andavano già alla grande)
roi = estrai(report, 'performance_marketing_reale', 'efficienza_pubblicitaria_roi')
cac = estrai(report, 'performance_marketing_reale', 'costo_acquisizione_cliente_cac_euro')
trend = estrai(report, 'analisi_contesto_esterno', 'trend_mercato')

# Stato di salute dal quadro generale
stato = estrai(report, 'quadro_generale_CEO', 'stato_salute_azienda')

# --- INTERFACCIA GRAFICA ---

# Sezione 1: KPI Finanziari Reali
st.subheader("📊 Quadro Finanziario")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Entrate Lorde", f"€ {entrate_lorde}" if entrate_lorde != "N/D" else "N/D")
with col2:
    st.metric("Utile Netto Stimato", f"€ {utile_netto}" if utile_netto != "N/D" else "N/D")
with col3:
    st.metric("Abbonati Attivi", abbonati_attivi)

# Sezione 2: KPI Marketing
st.subheader("📈 Performance Marketing")
col4, col5 = st.columns(2)
with col4:
    st.metric("ROI Pubblicitario", roi)
with col5:
    st.metric("CAC (Costo Acquisizione)", f"€ {cac}" if cac != "N/D" else "N/D")

# Sezione 3: Grafico Aziendale
st.subheader("📉 Analisi dei Trend")
chart_data = pd.DataFrame({'Valore': [100, 120, 150, 130]})
st.line_chart(chart_data)

# Barra di stato finale dinamica
if stato == "Eccellente":
    st.success(f"Stato Salute Azienda: {stato} | Mercato: {trend}")
else:
    st.info(f"Stato Salute Azienda: {stato} | Mercato: {trend}")

# --- ISPEZIONE DEL DIZIONARIO ---
with st.expander("🔍 Struttura Dati Rilevata (Nessun Errore, Solo Controllo)"):
    st.json(report)