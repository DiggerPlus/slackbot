# -*- coding: utf-8 -*-

import time
import re

from slackclient import SlackClient

# config
token = "slack bot token"
bot_name = 'diggerplus-bot'
bot_id = 'slack bot id'

# consts
READ_WEBSOCKET_DELAY = 1

HELP_COMMADN = '!help'
SET_COMMAND = '!set'
EXAMPLE_COMMAND = 'do'
PATTERN = r'!set (\w+) (.*)'

slack_client = SlackClient(token)

##
# Memory dict to store keywords
##
MEMORY_DICT = {}

# This is just to get bot id
"""
api_call = slack_client.api_call("users.list")
if api_call.get('ok'):
    users = api_call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == bot_name:
            print 'bot_id: ', user.get('id')
"""


def handle_command(command, channel):
    """Handler for parser commands."""

    resp = "Not sure what you mean. Try to type `!help` to get help!"
    print 'Current channel: {!r}, command: {!r}'.format(channel, command)
    if command == HELP_COMMADN:
        resp = '`{}`'.format(PATTERN)
    elif command.startswith(SET_COMMAND):
        matchs = re.compile(PATTERN).match(command).groups()
        key, val = matchs
        # if key in MEMORY_DICT:
        #     resp = "Keyword: {!r} is already exists. But I will override it!"
        MEMORY_DICT[key] = val
        resp = "Got it!"
    else:
        key = command.split('!')[1]
        _resp = MEMORY_DICT.get(key)
        if _resp is not None:
            resp = _resp
    slack_client.api_call("chat.postMessage", channel=channel, text=resp,
                          as_user=True)


def parse_slack_uptput(slack_rtm_output):
    """Filter commands by symbol `!`."""

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['text'].startswith('!'):
                return output['text'].lower(), output['channel']
    return None, None


if __name__ == '__main__':
    if slack_client.rtm_connect():
        print "StarterBot conected and running!"
        while True:
            command, channel = parse_slack_uptput(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print "Connection Failed, invalid token?"
