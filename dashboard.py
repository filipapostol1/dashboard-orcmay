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
# --- SEZIONE 2: SPIA COMPETITOR ---
elif menu == "🕵️ Spia Competitor":
    st.title("🕵️ Intelligence Competitor")
    
    storico_comp = dati.get("dati_per_grafici", {}).get("storico_competitor", [])
    
    if storico_comp:
        # Trasformiamo i dati in una tabella pandas
        df_comp = pd.DataFrame(storico_comp).set_index("data")
        
        # Supponiamo che l'orchestratore abbia estratto: Tuo Prezzo, Comp_A, Comp_B, Comp_C, Comp_D
        # (Nel JSON di test di prima avevamo solo A e B, ma espandiamo la logica)
        
        if status == "PIANO BASE":
            st.error("🔒 Piano BASE attivo: puoi vedere solo i primi 2 Competitor.")
            
            # ✂️ TAGLIO DEI DATI: Selezioniamo solo le colonne del Tuo Prezzo e dei primi 2 competitor
            colonne_base = [col for col in df_comp.columns if col in ["tuo_prezzo", "competitor_a", "competitor_b"]]
            df_filtrato = df_comp[colonne_base]
            
            # Mostriamo solo la tabella limitata
            st.dataframe(df_filtrato, use_container_width=True)
            
            # ⚡ IL RECENTE GANCIO COMMERCIALE: Gli facciamo vedere cosa si sta perdendo
            st.markdown("---")
            st.warning("⚠️ **Competitor C** e **Competitor D** stanno modificando i loro prezzi in questo momento! Passa al **Piano PRO** per sbloccare il tracciamento completo e i grafici storici.")
            
        else:
            # PIANO PRO: Sblocca tutto!
            st.success("🔓 Accesso PRO: Tracciamento Completo di tutti i Competitor sbloccato")
            
            # Mostra il grafico a linee con TUTTE le linee di tutti i competitor sovrapposte
            st.line_chart(df_comp)
            
            # Mostra anche la tabella completa sotto per controllo dettagliato
            st.subheader("📋 Tabella Dati Completa")
            st.dataframe(df_comp, use_container_width=True)
    else:
        st.info("Nessun dato sui competitor disponibile.")
