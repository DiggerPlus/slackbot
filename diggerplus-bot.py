# -*- coding: utf-8 -*-

import re
import random
import redis
import logging

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from google import lucky

logger = logging.getLogger()

r = redis.Redis()

HI_MSGS = [
    'Hello gay!',
    'Are you kidding me?'
]

KEYWORD_PREFIX = 'slackbot:bot:keyword:%s'
ALL_KEYWORDS = 'slackbot:bot:keywords'


@respond_to('^hi$', re.IGNORECASE)
def hi(message):
    message.reply(random.choice(HI_MSGS))
    message.react('+1')


@respond_to('I loven you')
def love(message):
    message.reply('I love you too!')


@listen_to('^help$')
def help(message):
    message.reply("Waht's your problem?")


@respond_to('^!(\w+)$')
@listen_to('^!(\w+)$')
def keyword_lookup(message, keyword):
    logger.info('Loop up for keyword: %s' % keyword)
    resp = r.get(KEYWORD_PREFIX % keyword)
    if not resp:
        return message.send("Not sure what you mean.")
    message.send(resp)


@respond_to('^!set (\w+) (.+)$')
@listen_to('^!set (\w+) (.+)$')
def set_keyword(message, keyword, value):
    logger.info('Set keyword: %s to value: %s' % (keyword, value))
    r.set(KEYWORD_PREFIX % keyword, value)
    message.send('Got it!')
    r.sadd(ALL_KEYWORDS, keyword)


@listen_to("^!list keywords$")
@respond_to("^!list keywords$")
def all_keywords(message):
    message.send(','.join(r.smembers(ALL_KEYWORDS)))


@listen_to("^!google (.*)$")
@respond_to("^!google (.*)$")
def google(message, keyword):
    message.send("http://lmgtfy.com/?q={}".format("+".join(keyword.split())))


@listen_to("^!g (.*)$")
@respond_to("^!g (.*)$")
def google_lucky(message, keyword):
    logger.info('Google for keyword: %s' % keyword)
    r = lucky(keyword)
    if r:
        url, desc = r
        return message.send(u"{} - {}".format(url, desc))
    return message.send('Nothing found!')
