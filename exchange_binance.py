# exchange_binance.py

import ccxt
import config

exchange = ccxt.binance({
    'apiKey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',  # Binance Futures
    }
})

def get_exchange():
    return exchange
