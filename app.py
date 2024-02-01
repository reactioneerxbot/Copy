from flask import Flask
from flask import request
from flask import Response
import requests
 
TOKEN = "6773788903:AAHKjSPGVF3NZhl-mtsZ8R9b_qRrTkM90Wo"
app = Flask(name)
 
def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id,txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
       
        chat_id,txt = parse_message(msg)
        if txt == "hi":
            tel_send_message(chat_id,"Hello!!")
        else:
            tel_send_message(chat_id,'from webhook')
       
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if name == 'main':
   app.run(debug=True)
