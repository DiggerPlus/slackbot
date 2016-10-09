# -*- coding: utf-8 -*-

import os

API_TOKEN = os.getenv('SLACK_BOT_TOKEN') or 'your slack token'

DEFAULT_REPLY = "Not sure what you mean."

PLUGINS = [
    'slackbot.plugins',
    'diggerplus-bot',
]
