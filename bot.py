import time
import config
from exchange import get_total_assets, exchange
from balance_manager import (
    load_start_snapshot, save_start_snapshot, get_current_snapshot,
    record_deposit, get_manual_adjustments
)
from market_analyzer import analyze_best_coins, decide_action, multi_timeframe_confirmation
from execution_manager import open_long, open_short, apply_trailing_stop
from allocation_manager import (
    calculate_trade_allocation_dynamic,
    determine_dynamic_leverage,
    calculate_adaptive_position_size
)
from trade_logic import check_dynamic_partial_take_profit
from position_manager import close_stale_positions, auto_exit_stagnant_positions, manage_spot_wallet
from risk_manager import emergency_stop_loss, dynamic_reserve_profit, set_start_balance
from indicators import calculate_indicators
from learning_manager import update_coin_score
from grid_manager import setup_grid, execute_grid
from dca_manager import check_dca_opportunity
from telegram_manager import send_telegram_message
from webhook_server import start_webhook_server
from moon_coin_detector import detect_moon_candidates
from signal_scoring import score_signal
from trade_logger import log_trade
from scalping_engine import detect_scalping_opportunity
from trade_cooldown import is_coin_on_cooldown, mark_coin_traded
from momentum_detector import detect_momentum_break
from grid_engine import is_sideways
from dashboard_export import export_bot_state
from reinforcement_tracker import update_strategy_score as reinforce_update, get_strategy_score, get_success_rate, decay_scores
from strategy_matrix_manager import update_strategy_score, get_best_strategy, print_matrix_summary
from phase21_debugger import run_phase_21_debug
from cluster_manager import run_cluster_diagnose
from spot_manager import safe_spot_exit
from logger import log_event, log_trade_event
from log_archiver import archive_and_send_logs_if_due
from gpt_signal_evaluator import evaluate_signal_with_gpt

initial_balance = None
active_grids = {}

def print_profit_loss():
    live_balance = get_current_snapshot()
    adjustments = get_manual_adjustments()
    pnl = live_balance - initial_balance - adjustments
    pnl_percent = (pnl / initial_balance) * 100 if initial_balance > 0 else 0
    symbol = "+" if pnl >= 0 else "-"
    result = f"[ERGEBNIS] Gewinn/Verlust: {symbol}{abs(pnl):.2f} USDT ({symbol}{abs(pnl_percent):.2f}%)"
    print(result)
    log_event(result)
    send_telegram_message(result)

def main():
    global initial_balance, active_grids

    print("\n[START] Bot wird gestartet...")
    log_event("Botstart")
    send_telegram_message("🚀 BOT wurde gestartet!")
    start_webhook_server()
    print("[INFO] Webhook-Server für TradingView gestartet auf Port 5000.")
    print(f"[INFO] Aktive Börse: {'Bybit' if config.USE_BYBIT else 'Binance'}")

    snapshot = load_start_snapshot()
    current_assets = get_total_assets()
    record_deposit(current_assets)
    run_cluster_diagnose(["BTC/USDT:USDT", "ETH/USDT:USDT"])

    if snapshot and snapshot > 10:
        initial_balance = snapshot
        log_event(f"Startguthaben geladen: {initial_balance:.2f} USDT")
    else:
        initial_balance = current_assets
        save_start_snapshot(initial_balance)
        log_event(f"Neues Startguthaben gesetzt: {initial_balance:.2f} USDT")

    set_start_balance(initial_balance)
    manage_spot_wallet()

    top = analyze_best_coins(limit=5)
    for sym in top:
        run_phase_21_debug(sym)

    while True:
        try:
            total_assets = get_total_assets()
            record_deposit(total_assets)
            print_profit_loss()

            emergency_stop_loss()
            dynamic_reserve_profit()
            close_stale_positions()
            auto_exit_stagnant_positions()

            if active_grids:
                for sym, data in list(active_grids.items()):
                    current_price = exchange.fetch_ticker(sym)['last']
                    execute_grid(sym, current_price)

            best_coins = analyze_best_coins()
            moon_candidates = detect_moon_candidates()
            if moon_candidates:
                for coin in moon_candidates:
                    if coin not in best_coins:
                        best_coins.append(coin)

            if config.DRY_MODE:
                best_coins = [sym for sym in best_coins if sym in config.TEST_SYMBOLS]
                log_event(f"Dry-Run aktiv: {best_coins}")

            if not best_coins:
                log_event("Keine geeigneten Coins gefunden.")
                time.sleep(60)
                continue

            session_log = []
            for symbol in best_coins:
                if is_coin_on_cooldown(symbol):
                    continue

                indicators = calculate_indicators(symbol)
                if not indicators:
                    continue

                timeframe_trend = multi_timeframe_confirmation(symbol)
                is_moon = symbol in moon_candidates

                if timeframe_trend == "neutral" and not is_moon:
                    continue

                signal = decide_action(indicators)
                scalp_signal = detect_scalping_opportunity(symbol)
                if signal == "Neutral" and scalp_signal != "Neutral":
                    signal = scalp_signal

                if is_sideways(symbol):
                    active_grids[symbol] = setup_grid(symbol)
                    continue

                momentum = detect_momentum_break(symbol)
                if momentum == "neutral" and not is_moon:
                    continue

                strategy = get_best_strategy(symbol)
                signal_score = score_signal(indicators, trend=timeframe_trend, is_moon=is_moon)
                if signal_score < 3 and not is_moon:
                    continue

                base_amount = calculate_trade_allocation_dynamic(total_assets, signal_score)
                if base_amount > total_assets * config.MAX_EQUITY_USAGE:
                    continue
                if total_assets - base_amount < config.MIN_EQUITY_LEFT:
                    continue

                leverage = determine_dynamic_leverage(indicators)
                amount = calculate_adaptive_position_size(total_assets, base_amount, signal_score, signal_score)

                signal_data = {
                    "symbol": symbol,
                    "trend": timeframe_trend,
                    "signal": signal,
                    "momentum": momentum,
                    "score": signal_score,
                    "indicators": indicators
                }

                from gpt_usage_guard import gpt_guard

                if gpt_guard(symbol):
                    gpt_result = evaluate_signal_with_gpt(signal_data)
                    send_telegram_message(f"📊 GPT-Empfehlung für {symbol}:\n{gpt_result}")
                
                else:
                    send_telegram_message(f"⚠️ GPT-Analyse deaktiviert oder Limit erreicht.")

                success = False
                if signal == "Long" and timeframe_trend == "up":
                    success = open_long(symbol, amount, leverage)
                elif signal == "Short" and timeframe_trend == "down":
                    success = open_short(symbol, amount, leverage)
                elif is_moon:
                    leverage = min(leverage, 2)
                    amount *= 0.5
                    success = open_long(symbol, amount, leverage)

                if not success:
                    send_telegram_message(f"❌ Kein Einstieg für {symbol}.")
                    continue

                update_strategy_score(symbol, strategy, success, trend=timeframe_trend, signal_score=signal_score)
                reinforce_update(symbol, strategy, success)

                quote = get_success_rate(symbol, strategy)
                send_telegram_message(f"📊 Quote für {symbol}/{strategy}: {quote * 100:.1f}%")

                log_trade_event(symbol, f"{symbol}: {signal} | {strategy} | {leverage}x | {amount} USDT | Score={signal_score}")
                send_telegram_message(f"✅ {signal} gestartet: {symbol} ({leverage}x) – {amount:.2f} USDT")

                entry = {
                    "symbol": symbol,
                    "signal": signal,
                    "score": signal_score,
                    "trend": timeframe_trend,
                    "momentum": momentum,
                    "leverage": leverage,
                    "amount": amount,
                    "status": "executed" if success else "skipped"
                }
                session_log.append(entry)

                apply_trailing_stop(symbol)
                check_dynamic_partial_take_profit(symbol, exchange.fetch_ticker(symbol)['last'])
                update_coin_score(symbol, signal, success=True)
                active_grids[symbol] = setup_grid(symbol)
                check_dca_opportunity(symbol, exchange.fetch_ticker(symbol)['last'])
                save_start_snapshot(get_current_snapshot())
                log_trade(symbol, signal, signal_score, leverage, amount, success)
                mark_coin_traded(symbol)

            if not session_log:
                session_log.append({
                    "symbol": "n/a", "signal": "none", "score": 0, "trend": "-",
                    "momentum": "-", "leverage": 0, "amount": 0, "status": "no trade"
                })
                update_strategy_score("n/a", "core", False)
                reinforce_update("n/a", "core", False)

            export_bot_state(session_log)
            print_matrix_summary()
            decay_scores()
            archive_and_send_logs_if_due()
            time.sleep(60)

        except Exception as e:
            log_event(f"[CRASH] Hauptschleife abgestürzt: {e}")
            send_telegram_message(f"❌ BOT-Fehler: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
