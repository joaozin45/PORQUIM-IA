from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# PEGA DAS VARIÁVEIS DO RAILWAY - NÃO DEIXA HARDCODED
TOKEN = os.environ.get('WHATSAPP_TOKEN')
PHONE_ID = os.environ.get('PHONE_NUMBER_ID')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

def enviar_msg(numero, texto):
    url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages" # v20.0 EXISTE
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "text": {"body": texto}
    }
    r = requests.post(url, headers=headers, json=data)
    print('Resposta da Meta:', r.status_code, r.text) # LOG IMPORTANTE
    return r

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print('Webhook verificado')
            return challenge, 200
        else:
            print('Token errado na verificação')
            return "Forbidden", 403

    if request.method == "POST":
        data = request.get_json()
        print('=== RECEBI DA META ===')
        print(json.dumps(data, indent=2))

        try:
            value = data['entry'][0]['changes'][0]['value']
            if 'messages' in value: # Evita crash com status
                msg = value['messages'][0]
                numero = msg['from']
                texto = msg['text']['body'].lower()

                # LÓGICA DO PORQUIM 👇
                if "oi" in texto or "ola" in texto:
                    resposta = "Opa 🐷 Porquim IA na área! Como posso ajudar?"
                elif "pix" in texto:
                    resposta = "Chave PIX do Porquim: porquim@ia.com 🐷"
                else:
                    resposta = "Recebi aqui! Porquim IA tá processando... 🐷"

                enviar_msg(numero, resposta)
        except Exception as e:
            print('=== ERRO DETALHADO ===')
            print(str(e)) # AGORA VAI MOSTRAR O ERRO REAL

        return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
