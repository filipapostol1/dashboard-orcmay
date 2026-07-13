import streamlit as st
import pandas as pd
import json
import os

try:
    from orchestrator import BusinessDataOrchestrator
except ImportError:
    st.error("⚠️ File orchestrator.py non trovato. Assicurati che sia nella stessa cartella.")
    st.stop()

st.set_page_config(page_title="E-com Intelligence Dashboard", layout="wide")

nome_file = os.path.join(os.getcwd(), "dati_dashboard.json")

def aggiorna_tutto():
    motore = BusinessDataOrchestrator()
    dati_f = motore.fetch_financial_data()
    dati_m = motore.fetch_marketing_data()
    dati_t = motore.fetch_market_trends()
    motore.genera_output_sistemi(dati_f, dati_m, dati_t)

if not os.path.exists(nome_file):
    with st.spinner("Creazione database iniziale..."):
        aggiorna_tutto()

def carica_pacchetto_dashboard():
    try:
        with open(nome_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# --- SIDEBAR E COMANDI ---
st.sidebar.title("🚀 E-com Intel")
status = st.sidebar.selectbox("Livello Account", ["PIANO BASE", "PIANO PRO"])

# QUESTO È IL BOTTONE MAGICO DA CLICCARE
if st.sidebar.button("🔄 Sincronizza Dati Ora"):
    with st.spinner("Scaricamento nuovi ordini e aggiornamento prezzi..."):
        aggiorna_tutto()
    st.sidebar.success("Dati aggiornati!")
    st.rerun()

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigazione", ["📈 Panoramica Store", "🕵️ Spia Competitor"])

dati_sito = carica_pacchetto_dashboard()

if not dati_sito:
    st.error("⚠️ Impossibile leggere i dati. Clicca su 'Sincronizza Dati Ora'.")
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
        # Rinomino le colonne per renderle professionali
        df_v = df_v.rename(columns={"fatturato": "Fatturato (€)", "ordini": "N° Ordini"})
        
        if status == "PIANO BASE":
            st.warning("🔒 Piano BASE: Nessun grafico di andamento. Hai accesso solo ai crudi numeri delle ultime 48 ore.")
            # Nel base mostra SOLO LA TABELLA (Niente grafici)
            st.dataframe(df_v, use_container_width=True)
        else:
            st.success("🔓 Piano PRO: Grafico andamento sbloccato.")
            # Nel PRO mostra IL GRAFICO e poi i dati
            st.line_chart(df_v["Fatturato (€)"])
    else:
        st.info("Nessun dato storico elaborato.")

# --- SEZIONE 2: SPIA COMPETITOR ---
elif menu == "🕵️ Spia Competitor":
    st.title(f"🕵️ Intelligence Competitor ({status})")
    
    storico_c = dati_piano.get("storico_competitor", [])
    if storico_c:
        df_c = pd.DataFrame(storico_c).set_index("data")
        
        # Sostituiamo "competitor_a" con nomi veri per fare un test visivo che spacca
        df_c = df_c.rename(columns={
            "tuo_prezzo": "Il Tuo Prezzo (€)", 
            "competitor_a": "Amazon (€)", 
            "competitor_b": "Ebay (€)", 
            "competitor_c": "Zalando (€)"
        })
        
        if status == "PIANO BASE":
            st.warning("🔒 Piano BASE: Puoi tracciare un solo concorrente (Amazon) e senza grafici di tendenza storici.")
            # Nel base mostra SOLO LA TABELLA striminzita
            st.dataframe(df_c, use_container_width=True)
            st.markdown("👉 *Passa al **Piano PRO** per sbloccare tutti gli altri store e i grafici predittivi sui prezzi.*")
        else:
            st.success("🔓 Piano PRO: Tracciamento globale attivo. Tutti i competitor monitorati in tempo reale.")
            # Nel PRO mostra il GRAFFICO INTERATTIVO con tutte le linee incrociate
            st.line_chart(df_c)
            st.dataframe(df_c, use_container_width=True)
    else:
        st.info("Nessun dato competitor elaborato. Prova a cliccare su 'Sincronizza Dati Ora'.")
