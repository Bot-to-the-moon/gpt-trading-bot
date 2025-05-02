# trade_logger.py

import datetime

def log_trade(symbol, signal, score, leverage, amount, success):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{time_now}] {symbol} {signal.upper()} Score={score} L={leverage} Amt={amount} {'✅' if success else '❌'}\n"
    with open("trade_log.txt", "a") as f:
        f.write(line)
# trade_logger.py

import datetime

def log_trade(symbol, signal, score, leverage, amount, success):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{time_now}] {symbol} {signal.upper()} Score={score} L={leverage} Amt={amount} {'✅' if success else '❌'}\n"
    with open("trade_log.txt", "a") as f:
        f.write(line)
