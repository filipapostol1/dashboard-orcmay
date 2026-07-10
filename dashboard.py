import streamlit as st
import pandas as pd
from orchestrator import BusinessDataOrchestrator

st.set_page_config(page_title="Orcmay Store Dashboard", layout="wide")
st.title("📊 Orcmay Store - Business Dashboard")

# 1. Inizializzazione sicura dell'Orchestratore
@st.cache_resource
def get_orchestrator():
    try:
        return BusinessDataOrchestrator()
    except Exception as e:
        st.sidebar.error(f"Errore inizializzazione: {e}")
        return None

orchestrator = get_orchestrator()

# 2. Caricamento dati protetto (Se fallisce, restituisce None invece di crashare)
if orchestrator:
    with st.spinner("Caricamento dati da Shopify in corso..."):
        try:
            # Proviamo a scaricare i dati finanziari
            financial_data = orchestrator.fetch_financial_data()
        except Exception as e:
            st.sidebar.warning(f"Impossibile recuperare i dati live: {e}")
            financial_data = None
else:
    financial_data = None

# 3. Funzione helper per mostrare i dati o N/D in caso di errore
def get_metric_value(data_source, key, default="N/D"):
    if data_source and isinstance(data_source, dict) and key in data_source:
        return data_source[key]
    return default

# --- LAYOUT DELLA DASHBOARD ---

# Esempio di metriche principali che non crasheranno mai
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Se financial_data è corrotto o vuoto, mostrerà "N/D" senza rompere la pagina
    tot_vendite = get_metric_value(financial_data, "total_sales")
    st.metric(label="Vendite Totali", value=f"{tot_vendite} €" if tot_vendite != "N/D" else tot_vendite)

with col2:
    ordini = get_metric_value(financial_data, "total_orders")
    st.metric(label="Ordini Totali", value=ordini)

with col3:
    aov = get_metric_value(financial_data, "average_order_value")
    st.metric(label="AOV (Ordine Medio)", value=f"{aov} €" if aov != "N/D" else aov)

with col4:
    status = "Attivo 🟢" if financial_data else "Errore Connessione 🔴"
    st.metric(label="Stato Connessione", value=status)

# Spazio per i grafici (protetti anch'essi)
st.subheader("📈 Andamento del Negozio")
try:
    if financial_data and "historical_data" in financial_data:
        df = pd.DataFrame(financial_data["historical_data"])
        st.line_chart(df)
    else:
        st.info("I dati storici per il grafico non sono al momento disponibili (N/D).")
except Exception as e:
    st.error(f"Errore nel rendering del grafico: {e}")
