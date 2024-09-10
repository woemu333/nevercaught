import sys
import requests
import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

class ErrorWebhookHandler:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def write(self, message):
        sys.__stdout__.write(message)
        if message.strip():  # Avoid sending empty messages
            if '[WARNING' in message:
                return
            if 'selfcord.errors.InvalidData: Did not receive a response from Discord' in message:
                return
            if 'We are being rate limited' in message:
                return
            if 'Command error' in message and 'is not found' in message:
                return
            if 'You need to verify your account in order to perform this action.' in message:
                data = {'content': f'`{os.path.basename(__file__)}`: <@{config['your_user_id']}>{os.path.basename(__file__)[:-3]} needs to be verified.'}
            else:
                data = {'content': f'`{os.path.basename(__file__)}`: {message}'}

            # Send message to webhook
            try:
                response = requests.post(self.webhook_url, json=data)
                response.raise_for_status()
            except requests.RequestException as e:
                sys.__stderr__.write(f"Failed to send message to Discord webhook: {e}\n")


    def flush(self):
        sys.__stderr__.flush()


def makeObject(webhookurl):
    return ErrorWebhookHandler(webhookurl)