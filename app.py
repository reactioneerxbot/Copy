import json
import requests
from flask import Flask, request

BOT_TOKEN = "6773788903:AAETlP7Hpt1mho2KibSjydZQneF212Jrzt4"
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot6773788903:AAETlP7Hpt1mho2KibSjydZQneF212Jrzt4/'
ADMIN = 5934725286
GOOD = ['👍', '🤣', '❤', '🔥', '🥰', '👏', '😁', '🎉', '🙏', '🕊', '🤩', '🐳', '💯', '😍', '❤️', '💋', '😇', '🤗', '💘', '😘', '🏆', '⚡', '🤝', '👨‍💻', '🫡', '😘', '😎']
BAD = ['👎', '😱', '🤬', '😢', '🤮', '💩', '😭', '😈', '😴', '😡', '🤔', '🤯', '🎃', '👻', '🥱', '🥴', '🌭', '🤣', '🍌', '💔', '🍓', '🍾', '🖕', '😨', '🙄', '🌚', '🤪', '💊']

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_webhook():
    try:
        data = json.loads(request.get_data())
        with open('r.txt', 'w') as file:
            file.write(json.dumps(data))
        # Extract relevant information
        chat_id = data['message']['chat']['id']
        message_text = data.get('message', {}).get('text')

        # Process the message and generate a response
        response_text = process_message(message_text)

        # Construct the response payload
        response_data = {'chat_id': chat_id, 'text': response_text}

        requests.post(BASE_TELEGRAM_URL + 'sendMessage', json=response_data)

    except Exception as e:
        # Handle errors appropriately
        print(f"Error handling request: {e}")
        return 'error'

@app.route('/', methods=['GET'])
def handle():
    try:
        with open('r.txt', 'r') as file:
            return file.readline()
    except Exception as e:
        return e

def process_message(message):
    # Implement your message-handling logic here
    return f"You said: {message}"  # Example echo response

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
