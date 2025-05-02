from exchange import exchange

def get_total_assets_debug():
    """Liefert detaillierte Aufschlüsselung über Spot + Funding + Gesamtwert (für Bybit)."""
    try:
        balance = exchange.fetch_balance()
        parts = {
            "spot": float(balance['USDT']['free']) if 'USDT' in balance else 0.0,
            "funding": 0.0,
            "total": 0.0
        }

        # Funding extrahieren – nur wenn vorhanden
        if 'info' in balance and 'result' in balance['info']:
            try:
                for item in balance['info']['result']['list']:
                    if item.get('coin') == 'USDT':
                        parts['funding'] += float(item.get('availableToWithdraw', 0))
            except Exception as e:
                print(f"[WARNUNG] Funding konnte nicht gelesen werden: {e}")

        parts["total"] = round(parts["spot"] + parts["funding"], 2)
        return parts

    except Exception as e:
        print(f"[FEHLER] Balance-Analyse fehlgeschlagen: {e}")
        return { "spot": 0.0, "funding": 0.0, "total": 0.0 }
