import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import random
import json
from message import *
import os
import logging
import pickle

LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, datefmt=DATE_FORMAT)

app = Flask(__name__)
try:
    with open('./config.json') as f:
        config = json.load(f)
        line_bot_api = LineBotApi(config['channel_access_token'])
        handler = WebhookHandler(config['channel_secret'])
except FileNotFoundError:
    logging.info('Local config not found')
    line_bot_api = LineBotApi(os.getenv('channel_access_token', None))
    handler = WebhookHandler(os.getenv('channel_secret', None))

all_users = {}
with open('all_users.pkl', 'wb') as f:
    pickle.dump(all_users, f)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        print(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def reply(event):
    user_id = event.source.user_id[-8:]
    with open('all_users.pkl', 'rb') as f:
        all_users = pickle.load(f)
    
    if event.message.text == '== Start ==':
        if all_users.get(user_id):
            del all_users[user_id]
        all_users[user_id] = Chatbot(event, line_bot_api)
    elif event.message.text == '== Rule ==':
        pass
    elif event.message.text == '== Staff member ==':
        pass
    else:
        all_users[user_id].next_state(event, line_bot_api)
    
    with open('all_users.pkl', 'wb') as f:
        pickle.dump(all_users, f)
    # if all_users.get(user_id) == None:
    #     all_users[user_id] = 1
    #     logging.info(f'=== Init user === : {user_id}')
    # else:
    #     logging.info(f'=== I known you === : {user_id}')
if __name__ == "__main__":
    app.run()