import json
import logging
import os
import time
import requests
from typing import Dict, List, Any, Optional

# ---------------------------------------------------------------------------
# Configurazione Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ShopifyOrchestrator")

# ---------------------------------------------------------------------------
# Configurazione Ambiente (Dinamica)
# ---------------------------------------------------------------------------
MODALITA_TEST: bool = os.getenv("MODALITA_TEST", "True").lower() in ("true", "1", "t", "yes")

def _recupera_token_sicuro() -> str:
    """Recupera il token da Env, Streamlit Secrets o file .streamlit/secrets.toml"""
    env_token = os.getenv("SHOPIFY_TOKEN")
    if env_token:
        return env_token

    try:
        import streamlit as st
        if "SHOPIFY_TOKEN" in st.secrets:
            return st.secrets["SHOPIFY_TOKEN"]
    except ImportError:
        pass  # Streamlit non installato nell'ambiente corrente

    base_dir = os.path.dirname(os.path.abspath(__file__))
    percorso_toml = os.path.join(base_dir, ".streamlit", "secrets.toml")

    if os.path.exists(percorso_toml):
        try:
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib

            with open(percorso_toml, "rb") as f:
                secrets = tomllib.load(f)
                return secrets.get("SHOPIFY_TOKEN", "")
        except Exception as e:
            logger.error(f"Errore nella lettura di secrets.toml: {e}")

    return ""


class ShopifyOrchestrator:
    """
    Orchestratore per la gestione dell'integrazione con Shopify REST API.
    Gestisce paginazione cursore, retry automatici e generazione JSON.
    """

    def __init__(
        self, 
        shop_name: Optional[str] = None, 
        api_token: Optional[str] = None, 
        api_version: str = "2024-04"
    ):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.shop_name = shop_name or os.getenv("SHOPIFY_SHOP_NAME", "orcmay")
        self.api_token = api_token or _recupera_token_sicuro()
        self.api_version = api_version
        self.base_url = f"https://{self.shop_name}.myshopify.com/admin/api/{self.api_version}"

        if MODALITA_TEST:
            logger.info("🧪 Orchestratore avviato in MODALITÀ TEST (dati simulati).")
        else:
            logger.info("🚀 Orchestratore avviato in MODALITÀ PRODUZIONE.")
            if not self.shop_name or not self.api_token:
                logger.error("❌ Credenziali Shopify mancanti! Verifica SHOPIFY_SHOP_NAME e SHOPIFY_TOKEN.")

    def _get_headers(self) -> Dict[str, str]:
        return {
            "X-Shopify-Access-Token": self.api_token,
            "Content-Type": "application/json"
        }

    def fetch_all_orders(self, status: str = "any", limit: int = 250) -> List[Dict[str, Any]]:
        """
        Recupera TUTTI gli ordini gestendo in automatico la paginazione cursore 
        (header 'Link') e i retry in caso di Rate Limit (HTTP 429).
        """
        if MODALITA_TEST:
            return self._get_mock_orders()

        orders: List[Dict[str, Any]] = []
        url: Optional[str] = f"{self.base_url}/orders.json?status={status}&limit={limit}"
        
        logger.info("⏳ Inizio scaricamento ordini da Shopify...")

        while url:
            success = False
            
            # Ciclo di Retry più pulito (max 3 tentativi per pagina)
            for attempt in range(1, 4):
                try:
                    response = requests.get(url, headers=self._get_headers(), timeout=10)
                    
                    if response.status_code == 429:
                        logger.warning(f"⚠️ Rate limit Shopify raggiunto. Tentativo {attempt}/3. Attesa 2s...")
                        time.sleep(2)
                        continue

                    response.raise_for_status()

                    data = response.json()
                    batch = data.get("orders", [])
                    orders.extend(batch)
                    
                    logger.info(f"Scarico batch di {len(batch)} ordini. (Totale parziale: {len(orders)})")

                    # Paginazione cursore
                    link_header = response.headers.get("Link")
                    url = self._extract_next_link(link_header)
                    success = True
                    break  # Esce dal loop di retry, passa alla pagina successiva

                except requests.exceptions.RequestException as e:
                    logger.error(f"❌ Errore HTTP (Tentativo {attempt}/3): {e}")
                    time.sleep(2)

            # Se fallisce 3 volte di fila sulla stessa pagina, interrompe per evitare loop infiniti
            if not success:
                logger.error("❌ Impossibile recuperare la pagina dopo 3 tentativi. Interruzione download.")
                break

        logger.info(f"✅ Download completato! Totale ordini recuperati: {len(orders)}")
        return orders

    def _extract_next_link(self, link_header: Optional[str]) -> Optional[str]:
        if not link_header:
            return None

        links = link_header.split(",")
        for link in links:
            if 'rel="next"' in link:
                raw_url = link.split(";")[0].strip()
                return raw_url.lstrip("<").rstrip(">")
        return None

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Elabora gli ordini e restituisce le metriche KPI di sintesi."""
        orders = self.fetch_all_orders()
        
        total_revenue = sum(float(o.get("total_price") or 0) for o in orders)
        order_count = len(orders)
        avg_order_value = (total_revenue / order_count) if order_count > 0 else 0.0

        return {
            "total_orders": order_count,
            "total_revenue": round(total_revenue, 2),
            "average_order_value": round(avg_order_value, 2),
            "currency": orders[0].get("currency", "EUR") if orders else "EUR"
        }

    def salva_json_sistemi(self, metrics: Dict[str, Any]):
        """Genera i file JSON richiesti dalla Dashboard Streamlit e dal Bot Telegram."""
        
        # Output per Bot Telegram
        bot_data = {
            "metriche_finanziarie": {
                "mrr_netto_stimato": metrics["total_revenue"],
                "ltv_stimato": 450.0, # TODO: Valore hardcodato. Sostituire con logica reale se necessario.
                "valore_totale_attivi": metrics["total_orders"]
            },
            "performance_marketing_reale": {
                # TODO: Sostituire i prossimi 3 valori integrando Meta/Google Ads API
                "efficienza_pubblicitaria_roi": 393.87,
                "costo_acquisizione_cliente_cac_euro": 41.67,
                "tasso_conversione_sito": 2.8
            },
            "indicatori_ceo": {
                "carrello_medio": metrics["average_order_value"],
                "valuta": metrics["currency"],
                "stato_salute_asset": "Ottimo"
            }
        }
        
        bot_path = os.path.join(self.dir_path, "report_orchestra_holding.json")
        with open(bot_path, "w", encoding="utf-8") as f:
            json.dump(bot_data, f, indent=4, ensure_ascii=False)
        logger.info(f"✅ JSON Telegram salvato in: {bot_path}")

        # Output per Dashboard Streamlit
        dash_data = {
            "PIANO BASE": {
                "kpi": {
                    "fatturato": metrics["total_revenue"],
                    "ordini": metrics["total_orders"],
                    "cac": 41.67,
                    "roi": 393.87
                }
            },
            "PIANO PRO": {
                "kpi": {
                    "fatturato": metrics["total_revenue"],
                    "ordini": metrics["total_orders"],
                    "cac": 41.67,
                    "roi": 393.87
                }
            }
        }

        dash_path = os.path.join(self.dir_path, "dati_dashboard.json")
        with open(dash_path, "w", encoding="utf-8") as f:
            json.dump(dash_data, f, indent=4, ensure_ascii=False)
        logger.info(f"✅ JSON Dashboard salvato in: {dash_path}")

    def _get_mock_orders(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1001,
                "name": "#1001",
                "total_price": "149.90",
                "currency": "EUR",
                "financial_status": "paid",
                "created_at": "2026-07-22T08:30:00+02:00"
            },
            {
                "id": 1002,
                "name": "#1002",
                "total_price": "89.50",
                "currency": "EUR",
                "financial_status": "paid",
                "created_at": "2026-07-22T09:15:00+02:00"
            }
        ]


if __name__ == "__main__":
    orchestrator = ShopifyOrchestrator()
    metrics = orchestrator.get_summary_metrics()
    
    print("\n--- RIEPILOGO DATI ELABORATI ---")
    print(f"Ordini Totali : {metrics['total_orders']}")
    print(f"Fatturato     : {metrics['total_revenue']} {metrics['currency']}")
    print(f"Carrello Medio: {metrics['average_order_value']} {metrics['currency']}")
    
    # Salva i file per dashboard e bot
    orchestrator.salva_json_sistemi(metrics)
