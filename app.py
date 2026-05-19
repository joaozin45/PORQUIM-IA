from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "EAAOiPZCHOfPwBRVN1kcQUAaQBjxRkVnlxnAizcnFqZAaSHTYtnooj0F9pETifTsiHTusvtBMQlLyJMkH6ZBRUQvqhrp1jS16EOxW9w4lVD5rBjxbWv0c84sKgxZALj9ZCfX2HlZA3zjkMZCCZAqTkxrZBimsaIZBK1CONLBfOuUfH2G90vVowATXNCaiAZCdIh05meD5lPod2HOt4HPuAhEPP4axdh8pQ3nZAzJ7MTBnnrz1paFDgpPafJr4tAZDZD"
PHONE_ID = "1169292899596436"
VERIFY_TOKEN = "porquim123"

def enviar_msg(numero, texto):
    url = f"https://graph.facebook.com/v25.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET": # Verificação da Meta
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200 # Meta exige status 200
        else:
            return "Forbidden", 403
      
    if request.method == "POST": # Mensagem chegando
        data = request.get_json()
        try:
            msg = data['entry'][0]['changes'][0]['value']['messages'][0]
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
        except:
            pass
        return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
