import json
from linebot.models import TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction
from data.text import *

SELECTOR_TEMPLATE_PATH="./data/selector.json"
SCRIPT_PATH="./data/script.json"
SCORE = { 'A' : 1, 'B' : -1 }
with open(SELECTOR_TEMPLATE_PATH) as f:
    selector = json.load(f)
with open(SCRIPT_PATH) as f:
    script = json.load(f)
script = script['script']

class Chatbot:
    def __init__(self, event, line_bot_api):
        self.problem_num = 0
        self.score = 0
        self.state = 0
        messages = TextSendMessage(
            text=start_message,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="start", text="start"))
                ]
            )
        )
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
    def generate_message(self, contents):
        messages = []
        for content in contents:
            if content['type'] == 'text':
                messages.append(TextSendMessage(text=content["content"]))
            elif content['type'] == 'text_question':
                option_items = []
                for option in ['A', 'B']:
                    option_items.append(QuickReplyButton(action=MessageAction(label=option, text=option)))
                messages.append(
                    TextSendMessage(
                        text=content["content"],
                        quick_reply=QuickReply(items=option_items)
                    )
                )
            elif content['type'] == 'text_continue':
                
                messages.append(
                    TextSendMessage(
                        text=content["content"],
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(action=MessageAction(label="continue", text="continue"))
                            ]
                        )
                    )
                )
            else:
                pass
        return messages

    
    def next_state(self, event, line_bot_api):
        if self.state == 0 and event.message.text == 'start':
            self.state = 1
            try:
                answer_script = script[self.problem_num][event.message.text]
            except KeyError:
                return
            messages = self.generate_message(answer_script['contents'])
            self.send_message(event, messages, line_bot_api)
            self.problem_num += 1

        elif self.state == 1:
            try:
                answer_script = script[self.problem_num][event.message.text]
            except KeyError:
                print(self.state)
                print(self.problem_num)
                print(script[self.problem_num])
                print(event.message.text)
                print(script[self.problem_num][event.message.text])
                return
            if answer_script['pass']:
                return
            self.score += answer_script['weight']
            messages = self.generate_message(answer_script['contents'])
            self.send_message(event, messages, line_bot_api)
            self.problem_num += 1
        else:
            pass


