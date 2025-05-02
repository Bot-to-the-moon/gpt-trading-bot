# exchange_bybit.py

import ccxt
import config

exchange = ccxt.bybit({
    'apiKey': config.BYBIT_API_KEY,
    'secret': config.BYBIT_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'unified',
    }
})

def get_exchange():
    return exchange
