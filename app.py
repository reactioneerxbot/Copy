import io
import json
import base64
import requests
from itertools import islice
from flask import Flask, request

BOT_TOKEN = "6773788903:AAETlP7Hpt1mho2KibSjydZQneF212Jrzt4"
GIT_TOKEN = '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'
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot6773788903:AAETlP7Hpt1mho2KibSjydZQneF212Jrzt4/'
ADMIN = 5934725286
GOOD = ['👍', '🤣', '❤', '🔥', '🥰', '👏', '😁', '🎉', '🙏', '🕊', '🤩', '🐳', '💯', '😍', '❤️', '💋', '😇', '🤗', '💘', '😘', '🏆', '⚡','🤝', '👨‍💻', '🫡', '😘', '😎']
BAD = ['👎', '😱', '🤬', '😢', '🤮', '💩', '😭', '😈', '😴', '😡', '🤔', '🤯', '🎃', '👻', '🥱', '🥴', '🌭', '🤣', '🍌', '💔', '🍓', '🍾','🖕', '😨', '🙄', '🌚', '🤪', '💊']

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_webhook():
    try:
        process(json.loads(request.get_data()))
        return 'Success!'
    except Exception as e:
        print(e)
        return 'Error'


def process(update):
    if 'message' in update:
        if 'text' in update['message'] and 'chat' in update['message'] and update['message']['chat']['type'] == 'private':
            private(update['message']['from']['id'])
        elif 'text' in update['message'] and 'chat' in update['message'] and (update['message']['chat']['type'] == 'group' or update['message']['chat']['type'] == 'supergroup'):
            if update['message']['text'] == '/include@reactioner_bot':
                if included(update['message']['from']['id']) == 1:
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'], '<em>You have already enrolled.</em>')
                elif included(update['message']['from']['id']) == 0:
                    with open(f"{update['message']['from']['id']}.txt", 'r') as file:
                        line = file.readline().split()
                    with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                        file.write(f"I {line[1]} {line[2]} {line[3]} {line[4]} {line[5]} {line[6]}")
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'], '<em>Welcome back. You enrolled successfully.</em>')
                    with open('user.txt', 'a') as file:
                        file.write(
                            f"{update['message']['from']['id']} {update['message']['from']['first_name'].split()[0]} {update['message']['chat']['id']}\n")
                    git_update('user.txt')
                else:
                    with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                        file.write(f"I {0} {0} {0} {0} {0} {0}")
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'], '<em>You enrolled successfully.</em>')
                    with open('user.txt', 'a') as file:
                        file.write(
                            f"{update['message']['from']['id']} {update['message']['from']['first_name'].split()[0]} {update['message']['chat']['id']}\n")
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
                git_create(f"{update['message']['from']['id']}.txt", 'I {0} {0} {0} {0} {0} {0}')
            elif update['message']['text'] == '/exclude@reactioner_bot':
                if included(update['message']['from']['id']) == 1:
                    with open(f"{update['message']['from']['id']}.txt", 'r') as file:
                        line = file.readline().split()
                    with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                        file.write(f"E {line[1]} {line[2]} {line[3]} {line[4]} {line[5]} {line[6]}")
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'], '<em>Bye you stopped enrolling.</em>')
                    with open('user.txt', 'r') as file:
                        lines = file.readlines()
                    updated = [line for line in lines if str(update['message']['from']['id']) not in line]
                    with open('user.txt', 'w') as file:
                        file.writelines(updated)
                    git_update('user.txt')
                    git_update("update['message']['from']['id']}.txt")
                elif included(update['message']['from']['id']) == 0:
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'], '<em>You have already stopped enrolling.</em>')
                else:
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'], '<em>You have not started enrolling at all.</em>')
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
            elif update['message']['text'] == '/stats@reactioner_bot':
                if included(update['message']['from']['id']) == 1:
                    with open(f"{update['message']['from']['id']}.txt", 'r') as file:
                        line = file.readline().split()
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'],
                              f"<strong>Your statistics:</strong>\n\n<em>Positive reactions:</em> {line[1]}\n<em>Negative reactions:</em> {line[2]}\n<em>Neutral reactions:</em> {line[4]}\n<em>Self reactions:</em> {line[5]}\n\n<strong>Total reactions you got:</strong> {int(line[1]) + int(line[2]) + int(line[4]) + int(line[5])}\n<strong>Total reactions you put:</strong> {line[3]}")
                else:
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'],
                              f"<strong>You have not included.</strong>\n<em>Please /include@reactioner_bot</em>")
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
            elif update['message']['text'] == '/results@reactioner_bot':
                if is_admin(update['message']['chat']['id'], update['message']['from']['id']):
                    group = update['message']['chat']['id']
                    set1 = {}
                    set2 = {}
                    set3 = {}
                    set4 = {}
                    set5 = {}
                    set6 = {}
                    with open('user.txt', 'r') as file:
                        lines = file.readlines()
                    for l in lines:
                        if int(l.split()[2]) == group:
                            with open(f"{l.split()[0]}.txt", 'r') as f:
                                line = f.readline().split()
                            if line[0] == 'E':
                                break
                            set3[l.split()[1] + " -> "] = int(line[3])
                            set1[l.split()[1] + " -> "] = int(line[1])
                            set2[l.split()[1] + " -> "] = int(line[2])
                            set4[l.split()[1] + " -> "] = int(line[4])
                            set5[l.split()[1] + " -> "] = int(line[5])
                            if int(line[3]) != 0 and  int(line[6]) != 0:
                                set6[l.split()[1] + " -> "] = float((int(line[1]) - int(line[2])) / (int(line[3]) * int(line[6])))
                    set1 = dict(sorted(set1.items(), key=lambda item: item[1], reverse=True))
                    set2 = dict(sorted(set2.items(), key=lambda item: item[1], reverse=True))
                    set3 = dict(sorted(set3.items(), key=lambda item: item[1], reverse=True))
                    set4 = dict(sorted(set4.items(), key=lambda item: item[1], reverse=True))
                    set5 = dict(sorted(set5.items(), key=lambda item: item[1], reverse=True))
                    set6 = dict(sorted(set6.items(), key=lambda item: item[1], reverse=True))
                    ret = '\n<strong>TOP admired users:</strong>'
                    for key, value in islice(set1.items(), 5):
                        ret += '\n<em>' + key + '</em>' + str(value)
                    ret += '\n\n<strong>TOP hated users:</strong>'
                    for key, value in islice(set2.items(), 5):
                        ret += '\n<em>' + key + '</em>' + str(value)
                    ret += '\n\n<strong>TOP neutrally reacted users:</strong>'
                    for key, value in islice(set4.items(), 5):
                        ret += '\n<em>' + key + '</em>' + str(value)
                    ret += '\n\n<strong>TOP reaction makers:</strong>'
                    for key, value in islice(set3.items(), 5):
                        ret += '\n<em>' + key + '</em>' + str(value)
                    ret += '\n\n<strong>TOP self reacted users:</strong>'
                    for key, value in islice(set5.items(), 5):
                        ret += '\n<em>' + key + '</em>' + str(value)
                    ret += '\n\n<strong>Value coefficient:</strong>'
                    for key, value in islice(set6.items(), 5):
                        ret += '\n<em>' + key + '</em>' + str(value)
                    broadcast(update['message']['from']['id'], update['message']['from']['first_name'],
                              update['message']['chat']['id'], ret)
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={update['message']['chat']['id']}&message_id={update['message']['message_id']}")
                git_update('user.txt')
                with open('user.txt', 'r') as file:
                    lines = file.readlines()
                for line in lines:
                    git_update(f"{line.split()[0]}.txt")
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
                    print(update['message_reaction']['new_reaction'])
                    return
                    #broadcast(update['message_reaction']['user']['id'],update['message_reaction']['user']['first_name'],update['message_reaction']['chat']['id'],'<strong>I will count it as a neutral reaction!</strong>')
                type = is_good(reaction.get('emoji', 'UNKNOWN'))
                try:
                    if int(case) != update['message_reaction']['user']['id']:
                        with open(f"{update['message_reaction']['user']['id']}.txt", 'r') as file:
                            line = file.readline().split()
                        with open(f"{str(update['message_reaction']['user']['id']).strip()}.txt", 'w') as file:
                            file.write(f"I {line[1]} {line[2]} {str(int(line[3]) + 1)} {line[4]} {line[5]} {line[6]}")
                    else:
                        with open(f"{update['message_reaction']['user']['id']}.txt", 'r') as file:
                            line = file.readline().split()
                        with open(f"{str(update['message_reaction']['user']['id']).strip()}.txt", 'w') as file:
                            file.write(f"I {line[1]} {line[2]} {line[3]} {line[4]} {str(int(line[5]) + 1)} {line[6]}")
                        break
                    if case != -1:
                        with open(f"{case}.txt", 'r') as file:
                            line = file.readline().split()
                        with open(f"{case}.txt", 'w') as file:
                            if type == -1:
                                file.write(f"{line[0]} {line[1]} {str(int(line[2]) + 1)} {line[3]} {line[4]} {line[5]} {line[6]}")
                            elif type == 1:
                                file.write(f"{line[0]} {str(int(line[1]) + 1)} {line[2]} {line[3]} {line[4]} {line[5]} {line[6]}")
                            else:
                                file.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {str(int(line[4]) + 1)} {line[5]} {line[6]}")
                except:
                    pass
            for reaction in update['message_reaction']['old_reaction']:
                if reaction.get('type') != 'emoji':
                    print(update['message_reaction']['old_reaction'])
                    return
                    #broadcast(update['message_reaction']['from']['id'],update['message_reaction']['from']['first_name'],update['message_reaction']['chat']['id'],'<strong>I will count it as a neutral reaction!</strong>')
                type = is_good(reaction.get('emoji', 'UNKNOWN'))
                try:
                    if int(case) != update['message_reaction']['user']['id']:
                        with open(f"{update['message_reaction']['user']['id']}.txt", 'r') as file:
                            line = file.readline().split()
                        with open(f"{str(update['message_reaction']['user']['id']).strip()}.txt", 'w') as file:
                            file.write(f"I {line[1]} {line[2]} {str(int(line[3]) - 1)} {line[4]} {line[5]} {line[6]}")
                    else:
                        with open(f"{update['message_reaction']['user']['id']}.txt", 'r') as file:
                            line = file.readline().split()
                        with open(f"{str(update['message_reaction']['user']['id']).strip()}.txt", 'w') as file:
                            file.write(f"I {line[1]} {line[2]} {line[3]} {line[4]} {str(int(line[5]) - 1)} {line[6]}")
                        break
                    if case != -1:
                        with open(f"{case}.txt", 'r') as file:
                            line = file.readline().split()
                        with open(f"{case}.txt", 'w') as file:
                            if type == -1:
                                file.write(f"{line[0]} {line[1]} {str(int(line[2]) - 1)} {line[3]} {line[4]} {line[5]} {line[6]}")
                            elif type == 1:
                                file.write(f"{line[0]} {str(int(line[1]) - 1)} {line[2]} {line[3]} {line[4]} {line[5]} {line[6]}")
                            else:
                                file.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {str(int(line[4]) - 1)} {line[5]} {line[6]}")
                except:
                    pass

def included(user_id):
    try:
        with open(f"{user_id}.txt", 'r') as file:
            if file.readline().split()[0] == 'I':
                return 1
            else:
                return 0
    except:
        return -1


def append(initial_line):
    with open('messages.txt', 'r') as file:
        lines = file.readlines()
    if len(lines) >= 1000:
        lines.pop(0)
    with open('messages.txt', 'a') as file:
        file.write(initial_line + '\n')
    if included(initial_line.split()[1]):
        with open(f"{initial_line.split()[1]}.txt", 'r') as file:
            line = file.readline().split()
        with open(f"{initial_line.split()[1]}.txt", 'w') as file:
            file.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {line[4]} {line[5]} {str(int(line[6]) + 1)}")
    return


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
    id_to_react = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params).json().get(
        'result').get('message_id')
    params = {
        'chat_id': group,
        'message_id': id_to_react,
        'is_big': True,
        'reaction': json.dumps([{'type': 'emoji', 'emoji': '🔥'}])
    }
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/setMessageReaction', params=params).json()
    return

def private(chat_id):
    params = {"chat_id": chat_id,"text": "ℹ️ In order to use me, you need to add me to your group. Press the button below and select your group.\nℹ️ Чтобы использовать меня, вам нужно добавить меня в свою группу. Нажмите кнопку ниже и выберите свою группу.\nℹ️ Mendan foydalanish uchun siz meni guruhingizga qo'shishingiz kerak. Quyidagi tugmani bosing va guruhingizni tanlang.","reply_markup": json.dumps({"keyboard": [[{"text": "Add | Добавлять | Qo'shish","request_chat": {"request_id": 1, "chat_is_channel": False,"user_administrator_rights": {"can_manage_chat": True,"can_invite_users": True,"can_delete_messages": True,"can_promote_members": True,"can_restrict_members": True,"can_pin_messages": True,"can_manage_topics": True},"bot_administrator_rights": {"can_manage_chat": True,"can_invite_users": True,"can_delete_messages": True,"can_promote_members": True,"can_restrict_members": True,"can_pin_messages": True,"can_manage_topics": True}}}]],"resize_keyboard": True})}
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=params).json()
    return

def is_admin(chat_id, user_id):
    if user_id == ADMIN or requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={chat_id}&user_id={user_id}').json()[
        'result']['status'] in ['administrator', 'creator']:
        return True
    else:
        return False


def initialize():
    with open('messages.txt', 'w') as file:
        file.write('1234 7777777777\n')
    return


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

def git_create(filename, content):
    headers = {
        "Authorization": f"token {GIT_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/reactioneerxbot/Copy/contents/{filename}"
    send_content = base64.b64encode(content.encode()).decode()
    payload = {
        "message": "Create new file",
        "content": send_content
    }
    requests.put(url, headers=headers, data=json.dumps(payload))

def git_update(filename):
    username = "reactioneerxbot"
    repository = "Copy"
    branch = "main"
    with open(filename, "r") as file:
        new_content = file.read()
    new_content_bytes = new_content.encode("utf-8")
    new_content_base64 = base64.b64encode(new_content_bytes).decode("utf-8")
    url = f"https://api.github.com/repos/{username}/{repository}/contents/{filename}"
    headers = {
        "Authorization": f"token {GIT_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    sha = response_data["sha"]
    payload = {
        "message": "Update users.txt",
        "content": new_content_base64,
        "sha": sha,
        "branch": branch
    }
    update_url = f"https://api.github.com/repos/{username}/{repository}/contents/{filename}"
    requests.put(update_url, json=payload, headers=headers)


if __name__ == '__main__':
    app.run(debug=False)
