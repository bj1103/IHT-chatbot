import json
from linebot.models import TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageSendMessage
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
        self.flag_b = 0
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
            elif content['type'] == 'image':
                messages.append(
                    ImageSendMessage(
                        original_content_url=content["content"],
                        preview_image_url=content["content"],
                        
                    )
                )
            elif content['type'] == 'image_continue':
                messages.append(
                    ImageSendMessage(
                        original_content_url=content["content"],
                        preview_image_url=content["content"],
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(action=MessageAction(label="continue", text="continue"))
                            ]
                        )
                    )
                )
            else:
                print(content['type'])
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
                return

            while answer_script['pass']:
                self.problem_num += 1
                self.score += answer_script['weight']
                if self.problem_num >= len(script):
                    break
                answer_script = script[self.problem_num]["continue"]
            if self.problem_num >= len(script):
                if self.score > 0:
                    ending = ending_A
                else:
                    ending = ending_B

                messages = TextSendMessage(
                    text=ending,
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=MessageAction(label="continue", text="continue"))
                        ]
                    )
                )
                self.send_message(event, messages, line_bot_api)
                self.state = 2
                return
            message_script = answer_script['contents']
            if self.problem_num == 3 and event.message.text == 'A':
                self.flag_b = 1
            if self.problem_num == 5:
                message_script = message_script[self.flag_b]
            
            self.score += answer_script['weight']
            messages = self.generate_message(message_script)
            self.send_message(event, messages, line_bot_api)
            self.problem_num += 1
        
        elif self.state == 2 and event.message.text == 'end':
            messages = TextSendMessage(
                text=looping_message,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="restart", text="== Start ==")),
                        QuickReplyButton(action=MessageAction(label="quit", text="== Quit =="))
                    ]
                )
            )
            self.send_message(event, messages, line_bot_api)
        else: # should not happen
            pass


