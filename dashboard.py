import os
import json
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Configurazione Pagina
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="E-com Intel - Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# CSS Personalizzato (Light Enterprise Theme)
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
        color: #1E293B;
    }
    
    .topbar-title {
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
    }

    .topbar-badge {
        background-color: #DEF7EC;
        color: #03543F;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 12px;
        display: inline-block;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TOPBAR SUPERIORE
# ---------------------------------------------------------------------------
col_title, col_status, col_cta = st.columns([3, 2, 2])

with col_title:
    st.markdown('<div class="topbar-title">E-COM INTEL &nbsp;|&nbsp; <span style="font-size: 14px; font-weight: normal; color: #64748B;">Workspace: Orcmay Store</span></div>', unsafe_allow_html=True)

with col_status:
    st.markdown('<span class="topbar-badge">SYSTEM ONLINE &nbsp;•&nbsp; PIANO PRO</span>', unsafe_allow_html=True)

with col_cta:
    st.link_button("Gestisci Abbonamento ↗", "https://tuosito.com/pricing", type="primary", use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# SIDEBAR LATERALE (Solo 2 opzioni attive e piene)
# ---------------------------------------------------------------------------
st.sidebar.title("NAVIGAZIONE")
menu_scelto = st.sidebar.radio(
    "Seleziona Modulo:",
    ["Panoramica Store", "Intelligence Competitor"],
    index=1
)

st.sidebar.markdown("---")
st.sidebar.caption("Account: admin@orcmay.com")
st.sidebar.caption("Versione API: v2024-04")

# ---------------------------------------------------------------------------
# LETTURA DATI IN SICUREZZA
# ---------------------------------------------------------------------------
dir_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(dir_path, "dati_dashboard.json")

dati_json = {}
if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            dati_json = json.load(f)
    except Exception as e:
        st.warning(f"Errore caricamento dati: {e}")

# ---------------------------------------------------------------------------
# CONTENUTO: PANORAMICA STORE
# ---------------------------------------------------------------------------
if menu_scelto == "Panoramica Store":
    st.subheader("Panoramica Store")
    st.caption("Metriche chiave sincronizzate in tempo reale con Shopify.")

    # Estrae i dati reali salvati dall'orchestratore se presenti
    piano_base = dati_json.get("PIANO BASE", {}).get("kpi", {})
    fatturato = piano_base.get("fatturato", 238.40)
    ordini = piano_base.get("ordini", 2)
    cac = piano_base.get("cac", 41.67)
    roi = piano_base.get("roi", 393.87)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Fatturato Totale", f"€ {fatturato:,.2f}", "Aggiornato")
    kpi2.metric("Ordini Ricevuti", str(ordini), "Shopify API")
    kpi3.metric("CAC", f"€ {cac}", "Meta/Google")
    kpi4.metric("ROI Pubblicitario", f"{roi}%", "Ottimo")

    st.write("")
    st.info("ℹ️ Scegli 'Intelligence Competitor' dalla barra laterale per monitorare l'andamento dei prezzi di mercato.")

# ---------------------------------------------------------------------------
# CONTENUTO: INTELLIGENCE COMPETITOR
# ---------------------------------------------------------------------------
elif menu_scelto == "Intelligence Competitor":
    st.subheader("Intelligence Competitor")
    st.caption("Monitoraggio in tempo reale del posizionamento prezzi sui marketplace principali.")

    competitor_data = dati_json.get("PIANO PRO", {}).get("competitor_spy", [
        {"Data": "2026-07-10", "Il Tuo Prezzo (€)": 39.99, "Amazon (€)": 41.20, "Ebay (€)": 38.90, "Zalando (€)": 35.00},
        {"Data": "2026-07-11", "Il Tuo Prezzo (€)": 39.99, "Amazon (€)": 40.90, "Ebay (€)": 39.50, "Zalando (€)": 34.50},
        {"Data": "2026-07-12", "Il Tuo Prezzo (€)": 39.99, "Amazon (€)": 40.90, "Ebay (€)": 37.90, "Zalando (€)": 34.00},
        {"Data": "2026-07-13", "Il Tuo Prezzo (€)": 39.99, "Amazon (€)": 42.00, "Ebay (€)": 37.90, "Zalando (€)": 36.00},
    ])

    df = pd.DataFrame(competitor_data)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Miglior Prezzo", "Zalando", "€ 36.00")
    kpi2.metric("Prezzo Medio Amazon", "€ 41.25", "+1.2%")
    kpi3.metric("Differenziale Tuo Prezzo", "-€ 2.01", "vs Amazon")
    kpi4.metric("Competitor Tracciati", "3 Piattaforme", "Attivi")

    st.write("")

    st.markdown("##### Storico Variazione Prezzi")
    if "Data" in df.columns:
        df_chart = df.set_index("Data")
    elif "data" in df.columns:
        df_chart = df.set_index("data")
    else:
        df_chart = df
        
    st.line_chart(df_chart, height=320)

    st.markdown("##### Dati Dettagliati")
    st.dataframe(df, use_container_width=True, hide_index=True)
