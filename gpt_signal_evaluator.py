# gpt_signal_evaluator.py

import openai
import json

openai.api_key = "DEIN_OPENAI_API_KEY"

def evaluate_signal_with_gpt(signal_data):
    prompt = f"""
Du bist ein Krypto-Trading-Analyst. Analysiere das folgende Signal und gib eine klare Empfehlung:
{json.dumps(signal_data, indent=2)}

Gib bitte folgendes zurück:
- Empfehlung: LONG / SHORT / WAIT
- Begründung in 1–2 Sätzen
- Einschätzung des Risikos (niedrig/mittel/hoch)
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # oder "gpt-4" wenn du Zugang hast
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    answer = response['choices'][0]['message']['content']
    print("[GPT] Empfehlung:")
    print(answer)
    return answer
