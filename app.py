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
        update = json.loads(request.get_data())
        main(update)
    except Exception as e:
        print(f"Error handling request: {e}")
        return 'error'
if __name__ == '__main__':
    app.run(debug=True)
