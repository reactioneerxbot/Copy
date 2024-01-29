import io
import json
import requests
from itertools import islice

BOT_TOKEN = '6773788903:AAHKjSPGVF3NZhl-mtsZ8R9b_qRrTkM90Wo'
ALLOWED_UPDATES = ['message', 'message_reaction']
ADMIN = 5934725286
last_update_id = -1
GOOD = ['👍', '🤣', '❤', '🔥', '🥰', '👏', '😁', '🎉', '🙏', '🕊', '🤩', '🐳', '💯', '😍', '❤️', '💋', '😇', '🤗', '💘', '😘', '🏆', '⚡', '🤝', '👨‍💻', '🫡', '😘', '😎']
BAD = ['👎', '😱', '🤬', '😢', '🤮', '💩', '😭', '😈', '😴', '😡', '🤔', '🤯', '🎃', '👻', '🥱', '🥴', '🌭', '🤣', '🍌', '💔', '🍓', '🍾', '🖕', '😨', '🙄', '🌚', '🤪', '💊']

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
                            set1 = {}
                            set2 = {}
                            set3 = {}
                            set4 = {}
                            with open('user.txt', 'r') as file:
                                lines = file.readlines()
                            for l in lines:
                                with open(f"{l.split()[0]}.txt", 'r') as f:
                                    line = f.readline().split()
                                set3[l.split()[1] + " -> "] = int(line[3])
                                set1[l.split()[1] + " -> "] = int(line[1])
                                set2[l.split()[1] + " -> "] = int(line[2])
                                set4[l.split()[1] + " -> "] = int(line[4])
                            set1 = dict(sorted(set1.items(), key=lambda item: item[1], reverse=True))
                            set2 = dict(sorted(set2.items(), key=lambda item: item[1], reverse=True))
                            set3 = dict(sorted(set3.items(), key=lambda item: item[1], reverse=True))
                            set4 = dict(sorted(set4.items(), key=lambda item: item[1], reverse=True))
                            ret = '\n<strong>TOP admired users:</strong>'
                            for key, value in islice(set1.items(), 3):
                                ret += '\n<em>' + key + '</em>' + str(value)
                            ret += '\n\n<strong>TOP hated users:</strong>'
                            for key, value in islice(set2.items(), 3):
                                ret += '\n<em>' + key + '</em>' + str(value)
                            ret += '\n\n<strong>TOP reaction makers:</strong>'
                            for key, value in islice(set3.items(), 3):
                                ret += '\n<em>' + key + '</em>' + str(value)
                            ret += '\n\n<strong>TOP neutrally reacted users:</strong>'
                            for key, value in islice(set4.items(), 3):
                                ret += '\n<em>' + key + '</em>' + str(value)
                            broadcast(update['message']['from']['id'], update['message']['from']['first_name'],update['message']['chat']['id'], ret)
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
                    elif update['message']['text'] == '/INITIALIZE' and update['message']['from']['id'] == ADMIN:
                        initialize()
                        broadcast(ADMIN, 'Admin', update['message']['chat']['id'], '<strong>System restarted!</strong>')
                    elif update['message']['text'].split()[0] == '/RETURN' and update['message']['from']['id'] == ADMIN:
                        send_file(update['message']['text'].split()[1])
                    elif update['message']['text'].split()[0] == '/MESSAGES' and update['message']['from']['id'] == ADMIN:
                        messages()
                    elif update['message']['text'].split()[0] == '/USERS' and update['message']['from']['id'] == ADMIN:
                        users()
                append(f"{update['message']['message_id']} {update['message']['from']['id']}")
            elif 'message_reaction' in update:
                if 'chat' in update['message_reaction'] and (update['message_reaction']['chat']['type'] == 'group' or update['message_reaction']['chat']['type'] == 'supergroup') and included(update['message_reaction']['user']['id']):
                    case = fetch(update['message_reaction']['message_id'])
                    for reaction in update['message_reaction']['new_reaction']:
                        if reaction.get('type') != 'emoji':
                            broadcast(update['message_reaction']['user']['id'], update['message_reaction']['user']['first_name'], update['message_reaction']['chat']['id'],'<strong>I will count it as a neutral reaction!</strong>')
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
                            broadcast(update['message_reaction']['from']['id'], update['message_reaction']['from']['first_name'], update['message_reaction']['chat']['id'],'<strong>I will count it as a neutral reaction!</strong>')
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
    id_to_react = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params).json().get('result').get('message_id')
    print(id_to_react)
    params = {
        'chat_id': group,
        'message_id': id_to_react,
        'is_big': True,
        'old_reaction': [],
        'new_reaction': [{'type': 'emoji', 'emoji': '🔥'}]
    }
    print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/setMessageReaction', params=params).json())

def is_admin(chat_id, user_id):
        if user_id == ADMIN or requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={chat_id}&user_id={user_id}').json()['result']['status'] in ['administrator', 'creator']:
            return True
        else:
            return False

def initialize():
    with open('messages.txt', 'w') as file:
        file.write('1234 7777777777\n')
def send_file(user_id):
    with open(f'{user_id}.txt', 'r') as file:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", params={'chat_id': ADMIN},files={'document': (f'{user_id}.txt', io.StringIO(''.join(file.readlines())))})
    file.close()
    return
def messages():
    with open(f'messages.txt', 'r') as file:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", params={'chat_id': ADMIN},files={'document': ('Messages.txt', io.StringIO(''.join(file.readlines())))})
    file.close()
    return
def users():
    with open(f'user.txt', 'r') as file:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", params={'chat_id': ADMIN},files={'document': ('Users.txt', io.StringIO(''.join(file.readlines())))})
    file.close()
    return

if __name__ == "__main__":
    main()
