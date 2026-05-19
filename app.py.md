from flask import Flask, request  
import requests  
import os  
  
app = Flask(__name__)  
  
  
TOKEN = "EAAOiPZCHOfPwBRYf8FtBszGEZC7OqOsrlWIQZAcYVfh37aHZAndZCPwtIbFZCC5jCUZC8oIwc5FL80co87ZBnCzDAiWw3NKPVTbnnLnEcKRC1mbmJQQbhFAA0GZAU6VjZBAipb99IhPS5kJDz69zp51saXiFxGBaF3636Yq9WL2RGtUjJgR4XiXZBF1AgghcT5buGZBfHHojPqRL8IEcQDjqYwZC59idTfql9JbL3MZBukC2LuS9kUsW8lgFOf7AZDZD"  
PHONE_ID = "1169292899596436"  
VERIFY_TOKEN = "porquim123" # Invente qualquer senha pra verificação  
  
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
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:  
            return request.args.get("hub.challenge")  
        return "Token errado", 403  
      
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
    app.run(host="0.0.0.0", port=10000)  
