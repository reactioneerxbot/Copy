import json
import requests

BOT_TOKEN = '6773788903:AAHKjSPGVF3NZhl-mtsZ8R9b_qRrTkM90Wo'
ALLOWED_UPDATES = ['message', 'message_reaction']
ADMIN = 5934725286
last_update_id = -1
GOOD = ['👍', '❤', '🔥', '🥰', '👏', '😁', '🎉', '🤩', '💯', '😍', '❤️', '💋', '😇', '🤗', '💘', '😘', '🏆', '⚡', '🤝']
BAD = ['👎', '😱', '🤬', '😢', '🤮', '💩', '😭', '😈', '😴', '😡', '🤔', '🤯', '🎃', '👻', '🥱', '🥴', '🐳', '🌭', '🤣', '🍌', '💔', '🍓', '🍾', '🖕', '😨', '🙄']

def main():
    global last_update_id
    while True:
        updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id}&allowed_updates={json.dumps(ALLOWED_UPDATES)}").json().get('result', [])
        for update in updates:
            if 'message' in update:
                if 'text' in update['message'] and 'chat' in update['message'] and (update['message']['chat']['type'] == 'group' or update['message']['chat']['type'] == 'supergroup'):
                    if update['message']['text'] == '/include@reactioner_bot':
                        if included(update['message']['from']['id']) == 1:
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'], update['message']['chat']['id'], '<em>You have already enrolled.</em>')
                        elif included(update['message']['from']['id']) == 0:
                            with open(f"{update['message']['from']['id']}.txt", 'r') as file:
                                line = file.readline().split()
                            with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                                file.write(f"I {line[1]} {line[2]} {line[3]} {line[4]}")
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'], update['message']['chat']['id'],'<em>Welcome back. You enrolled successfully.</em>')
                            with open('user.txt', 'a') as file:
                                file.write(f"{update['message']['from']['id']} {update['message']['from']['first_name']}\n")
                        else:
                            with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                                file.write(f"I {0} {0} {0} {0}")
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'], update['message']['chat']['id'], '<em>You enrolled successfully.</em>')
                            with open('user.txt', 'a') as file:
                                file.write(f"{update['message']['from']['id']} {update['message']['from']['first_name']}\n")
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
                    elif update['message']['text'] == '/exclude@reactioner_bot':
                        if included(update['message']['from']['id']) == 1:
                            with open(f"{update['message']['from']['id']}.txt", 'r') as file:
                                line = file.readline().split()
                            with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                                file.write(f"E {line[1]} {line[2]} {line[3]} {line[4]}")
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'], update['message']['chat']['id'],'<em>Bye you stopped enrolling.</em>')
                            with open('user.txt', 'r') as file:
                                lines = file.readlines()
                            updated = [line for line in lines if update['message']['from']['id'] not in line]
                            with open('user.txt', 'w') as file:
                                file.writelines(updated)
                        elif included(update['message']['from']['id']) == 0:
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'], update['message']['chat']['id'],'<em>You have already stopped enrolling.</em>')
                        else:
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'], update['message']['chat']['id'],'<em>You have not started enrolling at all.</em>')
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
                    elif update['message']['text'] == '/show@reactioner_bot':
                        if included(update['message']['from']['id']) == 1:
                            with open(f"{update['message']['from']['id']}.txt", 'r') as file:
                                line = file.readline().split()
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'], update['message']['chat']['id'], f"<strong>Your statistics:</strong>\n\n<em>Positive reactions:</em> {line[1]}\n<em>Negative reactions:</em> {line[2]}\n<em>Neutral reactions:</em> {line[4]}\n\n<strong>Total reactions you got:</strong> {int(line[1]) + int(line[2]) + int(line[4])}\n<strong>Total reactions you put:</strong> {line[3]}")
                        else:
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'], update['message']['chat']['id'], f"<strong>You have not included.</strong>\n<em>Please /include@reactioner_bot</em>")
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
                    elif update['message']['text'] == '/show_all@reactioner_bot':
                        if is_admin(update['message']['chat']['id'], update['message']['from']['id']):
                            ret = ''
                            with open('user.txt', 'r') as file:
                                lines = file.readlines()
                            for line in lines:
                                with open(f"{line.split()[0]}.txt", 'r') as f:
                                    record = f.readline().split()[4]
                                ret = ret + line.split()[1] + " -> " + record + "\n"
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'],update['message']['chat']['id'], f"\n<strong>TOP reaction makers:</strong>\n<em>{ret}</em>")
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
                    elif update['message']['text'] == '/INITIALIZE' and update['message']['from']['id'] == ADMIN:
                        initialize()
                        broadcast(ADMIN, 'Admin', update['message']['chat']['id'], '<strong>System restarted!</strong>')
                append(f"{update['message']['message_id']} {update['message']['from']['id']}")
            elif 'message_reaction' in update:
                print(update['message_reaction'])
                if 'chat' in update['message_reaction'] and (update['message_reaction']['chat']['type'] == 'group' or update['message_reaction']['chat']['type'] == 'supergroup') and included(update['message_reaction']['user']['id']):
                    case = fetch(update['message_reaction']['message_id'])
                    for reaction in update['message_reaction']['new_reaction']:
                        if reaction.get('type') != 'emoji':
                            broadcast(update['message_reaction']['user']['id'], update['message_reaction']['user']['first_name'], update['message_reaction']['chat']['id'],'<strong>I dont support premium emojis for now.</strong>')
                            break
                        type = is_good(reaction.get('emoji', 'UNKNOWN'))
                        try:
                            with open(f"{update['message_reaction']['user']['id']}.txt", 'r') as file:
                                line = file.readline().split()
                            with open(f"{str(update['message_reaction']['user']['id']).strip()}.txt", 'w') as file:
                                file.write(f"I {line[1]} {line[2]} {str(int(line[3]) + 1)} {line[4]}")
                            if case != -1:
                                with open(f"{case}.txt", 'r') as file:
                                    line = file.readline().split()
                                with open(f"{case}.txt", 'w') as file:
                                    if type == -1:
                                        file.write(f"{line[0]} {line[1]} {str(int(line[2]) + 1)} {line[3]} {line[4]}")
                                    elif type == 1:
                                        file.write(f"{line[0]} {str(int(line[1]) + 1)} {line[2]} {line[3]} {line[4]}")
                                    else:
                                        file.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {str(int(line[4]) + 1)}")
                        except:
                            pass
                    for reaction in update['message_reaction']['old_reaction']:
                        if reaction.get('type') != 'emoji':
                            broadcast(update['message_reaction']['from']['id'], update['message_reaction']['from']['first_name'], update['message_reaction']['chat']['id'],'<strong>I dont support premium emojis for now</strong>')
                            break
                        type = is_good(reaction.get('emoji', 'UNKNOWN'))
                        try:
                            with open(f"{update['message_reaction']['user']['id']}.txt", 'r') as file:
                                line = file.readline().split()
                            with open(f"{str(update['message_reaction']['user']['id']).strip()}.txt", 'w') as file:
                                file.write(f"I {line[1]} {line[2]} {str(int(line[3]) - 1)} {line[4]}")
                            if case != -1:
                                with open(f"{case}.txt", 'r') as file:
                                    line = file.readline().split()
                                with open(f"{case}.txt", 'w') as file:
                                    if type == -1:
                                        file.write(f"{line[0]} {line[1]} {str(int(line[2]) - 1)} {line[3]} {line[4]}")
                                    elif type == 1:
                                        file.write(f"{line[0]} {str(int(line[1]) - 1)} {line[2]} {line[3]} {line[4]}")
                                    else:
                                        file.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {str(int(line[4]) - 1)}")
                        except:
                            pass
            last_update_id = update['update_id'] + 1
def included(user_id):
    try:
        with open(f"{user_id}.txt", 'r') as file:
            if file.readline().split()[0] == 'I':
                return 1
            else:
                return 0
    except:
        return -1
def append(line):
    # Read the current number of lines in the file
    with open('messages.txt', 'r') as file:
        lines = file.readlines()
    # If the number of lines exceeds 100, remove the oldest line
    if len(lines) >= 1000:
        lines.pop(0)
    # Append the new line
    with open('messages.txt', 'a') as file:
        file.write(line + '\n')
def fetch(message_id):
    with open('messages.txt', 'r') as file:
        for line in file.readlines():
            if str(line.split()[0]) == str(message_id):
                return line.split()[1]
    return -1
def is_good(emoji):
    for sample in GOOD:
        if emoji == sample:
            return 1
    for sample in BAD:
        if emoji == sample:
            return -1
    return 0
def broadcast(user_id, name, group, message):
    m = f"<a href='tg://user?id={user_id}'>{name}</a> ! "
    params = {
        'chat_id': group,
        'text': m + message,
        'parse_mode': 'HTML',
    }
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params)

def is_admin(chat_id, user_id):
        if user_id == ADMIN or requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={chat_id}&user_id={user_id}').json()['result']['status'] in ['administrator', 'creator']:
            return True
        else:
            return False

def initialize():
    with open('messages.txt', 'w') as file:
        file.write('1234 7777777777\n')

if __name__ == "__main__":
    main()
