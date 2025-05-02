# signal_scoring.py

def score_signal(indicators, trend="neutral", is_moon=False):
    score = 0

    if indicators['rsi'] < 30 or indicators['rsi'] > 70:
        score += 1
    if indicators['ema_short'] > indicators['ema_long']:
        score += 1
    if trend in ["up", "down"]:
        score += 1
    if is_moon:
        score += 2

    return score  # Max = 5
