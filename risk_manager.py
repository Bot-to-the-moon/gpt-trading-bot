# risk_manager.py

start_balance = None

def set_start_balance(balance):
    """Startguthaben setzen."""
    global start_balance
    start_balance = balance

def emergency_stop_loss(current_balance):
    """Stoppt den Bot, falls der Verlust 25 % überschreitet."""
    global start_balance
    if start_balance is None:
        print("[WARNUNG] Startguthaben nicht definiert, kann Risiko nicht bewerten.")
        return False

    loss_percentage = ((start_balance - current_balance) / start_balance) * 100

    print(f"[CHECK] Aktueller Verlust: {loss_percentage:.2f}%")

    if loss_percentage >= 25:
        print("[NOTFALL] Verlust über 25 %, Trading wird gestoppt!")
        exit()

def reserve_profit(current_balance):
    """Reserviert Gewinne ab 10 % Anstieg."""
    global start_balance
    if start_balance is None:
        return

    gain_percentage = ((current_balance - start_balance) / start_balance) * 100

    if gain_percentage >= 10:
        print(f"[GEWINN] Gewinn von {gain_percentage:.2f}% erreicht. Gewinne sichern empfohlen!")
# risk_manager.py (Erweiterung)

from exchange import get_balance

start_balance = None

def set_start_balance(balance):
    """Setzt das Startguthaben für Gewinn-/Verlustberechnung."""
    global start_balance
    start_balance = balance

def emergency_stop_loss():
    """Beendet den Bot, wenn der Verlust größer als 25% wird."""
    global start_balance
    current_balance = get_balance()

    if start_balance is None or current_balance is None:
        return

    loss_percentage = ((start_balance - current_balance) / start_balance) * 100
    print(f"[CHECK] Aktueller Verlust: {loss_percentage:.2f}%")

    if loss_percentage >= 25:
        print("[ALARM] Verlust über 25%! Bot stoppt.")
        exit()

def dynamic_reserve_profit():
    """Sichert automatisch Teilgewinne bei +5%, +10%, +20%."""
    global start_balance
    current_balance = get_balance()

    if start_balance is None or current_balance is None:
        return

    gain_percentage = ((current_balance - start_balance) / start_balance) * 100

    if gain_percentage >= 20:
        print(f"[GEWINN] +20% Gewinn erreicht! Gewinne sichern empfohlen!")
    elif gain_percentage >= 10:
        print(f"[GEWINN] +10% Gewinn erreicht! Gewinne sichern empfohlen!")
    elif gain_percentage >= 5:
        print(f"[GEWINN] +5% Gewinn erreicht! Gewinne sichern empfohlen!")
