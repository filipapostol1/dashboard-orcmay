import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# Configurazione Pagina & CSS Personalizzato (Light Enterprise Theme)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="E-com Intel - Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS per forzare lo stile Light Mode Enterprise senza emoji
st.markdown("""
    <style>
    /* Sfondo principale chiaro */
    .stApp {
        background-color: #F8F9FA;
        color: #1E293B;
    }
    
    /* Stile della Topbar */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        padding: 12px 24px;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 24px;
        border-radius: 8px;
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
        padding: 4px 12px;
        border-radius: 12px;
    }

    /* Card delle metriche */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Nasconde elementi inutili di default */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_javascript=True)

# ---------------------------------------------------------------------------
# TOPBAR SUPERIORE
# ---------------------------------------------------------------------------
col_title, col_status, col_cta = st.columns([3, 2, 2])

with col_title:
    st.markdown('<div class="topbar-title">E-COM INTEL &nbsp;|&nbsp; <span style="font-size: 14px; font-weight: normal; color: #64748B;">Workspace: Orcmay Store</span></div>', unsafe_allow_javascript=True)

with col_status:
    st.markdown('<span class="topbar-badge">SYSTEM ONLINE &nbsp;•&nbsp; PIANO PRO</span>', unsafe_allow_javascript=True)

with col_cta:
    # Pulsante che rimanda al sito principale per i piani/abbonamenti
    st.link_button("Gestisci Abbonamento ↗", "https://tuosito.com/pricing", type="primary", use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# SIDEBAR LATERALE
# ---------------------------------------------------------------------------
st.sidebar.title("NAVIGAZIONE")
menu_scelto = st.sidebar.radio(
    "Seleziona Modulo:",
    ["Panoramica Store", "Intelligence Competitor", "Analisi Ordini", "Impostazioni"],
    index=1
)

st.sidebar.markdown("---")
st.sidebar.caption("Account: admin@orcmay.com")
st.sidebar.caption("Versione API: v2024-04")

# ---------------------------------------------------------------------------
# CONTENUTO PRINCIPALE (INTELLIGENCE COMPETITOR)
# ---------------------------------------------------------------------------
if menu_scelto == "Intelligence Competitor":
    st.subheader("Intelligence Competitor")
    st.caption("Monitoraggio in tempo reale del posizionamento prezzi sui marketplace principali.")

    # Dati di esempio
    data = [
        {"Data": "2026-07-10", "Il Tuo Prezzo (€)": 39.99, "Amazon (€)": 41.20, "Ebay (€)": 38.90, "Zalando (€)": 35.00},
        {"Data": "2026-07-11", "Il Tuo Prezzo (€)": 39.99, "Amazon (€)": 40.90, "Ebay (€)": 39.50, "Zalando (€)": 34.50},
        {"Data": "2026-07-12", "Il Tuo Prezzo (€)": 39.99, "Amazon (€)": 40.90, "Ebay (€)": 37.90, "Zalando (€)": 34.00},
        {"Data": "2026-07-13", "Il Tuo Prezzo (€)": 39.99, "Amazon (€)": 42.00, "Ebay (€)": 37.90, "Zalando (€)": 36.00},
    ]
    df = pd.DataFrame(data)

    # KPI Summary Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Miglior Prezzo", "Zalando", "€ 36.00")
    kpi2.metric("Prezzo Medio Amazon", "€ 41.25", "+1.2%")
    kpi3.metric("Differenziale Tuo Prezzo", "-€ 2.01", "vs Amazon")
    kpi4.metric("Competitor Tracciati", "3 Piattaforme", "Attivi")

    st.write("")

    # Grafico Linee
    st.markdown("##### Storico Variazione Prezzi")
    df_chart = df.set_index("Data")
    st.line_chart(df_chart, height=320)

    # Tabella Dati
    st.markdown("##### Dati Dettagliati")
    st.dataframe(df, use_container_width=True, hide_index=True)
