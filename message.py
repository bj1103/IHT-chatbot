import json
from linebot.models import TextSendMessage, FlexSendMessage
from data.text import *

SELECTOR_TEMPLATE_PATH="./data/selector.json"
SCORE = { 'A' : 1, 'B' : -1 }
with open(SELECTOR_TEMPLATE_PATH) as f:
    selector = json.load(f)

class Chatbot:
    def __init__(self, event, line_bot_api):
        self.problem_num = 0
        self.score = 0
        self.state = 0
        messages = TextSendMessage(text=start_message)
        self.send_message(event, messages, line_bot_api)

    def generate_selector_flex(self, selection_a, selection_b):
        selector['footer']['contents'][0]['action']['label'] += selection_a
        selector['footer']['contents'][1]['action']['label'] += selection_b
        flex_message = FlexSendMessage(
            alt_text="Question",
            contents=selector
        )
        return flex_message

    def send_message(self, event, messages, line_bot_api):
        line_bot_api.reply_message(
            event.reply_token,
            messages
        )
    
    def next_state(self, event, line_bot_api):
        if self.state == 0 and event.message.text == '開始':
            self.state = 1
            self.problem_num += 1
            selector = self.generate_selector_flex("", "")
            messages = [
                TextSendMessage(text="A or B ?"), 
                selector
            ]
            self.send_message(event, messages, line_bot_api)

        elif self.state == 1:
            if (event.message.text == 'A' or event.message.text == 'B'):
                if self.problem_num < 5:
                    self.score += SCORE[event.message.text]
                    self.problem_num += 1
                    selector = self.generate_selector_flex("", "")
                    messages = [
                        TextSendMessage(text="A or B ?"), 
                        selector
                    ]
                    self.send_message(event, messages, line_bot_api)
                else:
                    self.score += SCORE[event.message.text]
                    if self.score > 0:
                        messages = TextSendMessage(text= "你是A！！")
                    else:
                        messages = TextSendMessage(text= "你是B！！")
                    self.send_message(event, messages, line_bot_api)
                    self.state = 2
            else:
                pass
        else:
            pass


