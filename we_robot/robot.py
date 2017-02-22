from werobot import WeRoBot
from tuling import tuling_robot
from post_api import post_engine
# import os
# import pymongo
# from werobot.session.mongodbstorage import MongoDBStorage
import logging


logger = logging.getLogger(__name__)
# mongodb_url = os.getenv('MONGO_URL')
# logger.debug('The mongodb URL is: %s' % mongodb_url)
# collection = pymongo.MongoClient(mongodb_url)['wechat']['session']
# session_storage = MongoDBStorage(collection)
robot = WeRoBot(token='RICUjs3yNWwp2dUvnoUrp7', enable_session=True)


def reply(source, content, session):
    logger.debug('Reply the message: %s\nFrom the source: %s' % (content, source))

    session_mode = session.get('mode')
    if session_mode:
        if content == '新西兰快递':
            session['mode'] = 'post'
            return u'新西兰快递模式开启\n---------\n\n请直接输入快递单号查询\n\n---------\n回复「退出」退出快递模式'
        elif content == '退出':
            session['mode'] = 'chat'
            return u'萌萌哒小九回来啦\n---------\n\n回复「新西兰快递」开启快递查询模式\n回复「退出」退出功能模式'''

        if session_mode == 'chat':
            return tuling_robot.tuling_robot(source, content)
        elif session_mode == 'post':
            return u'新西兰快递模式开启\n---------\n\n' + post_engine.trace_post(content) + '\n\n---------\n回复「退出」退出快递模式'
        else:
            logger.error('The system cannot handle the user input：%s' % content)
            logger.error('User mode：%s' % session_mode)
            return u'你发了什么？人家还小不明白的啦～'
    else:
        session['mode'] = 'chat'
        return u'''欢迎和小九做朋友，我会无偿陪你聊天喔～
当然啦，小九还会以下技能。小心不要被吓到咯～
如果你喜欢我记得把我介绍给更多的朋友 ❤️
---------

回复「新西兰快递」开启新西兰快递查询
回复「退出」退出功能模式'''


@robot.text
def handle_text(message, session):
    logger.debug('[ text message ]\nuser session: %s\nuser input: %s' % (session, message.raw))

    session['message_type'] = 'text'

    return reply(message.source, message.content, session)


@robot.voice
def handle_voice(message, session):
    logger.debug('[ voice message ]\nuser session: %s\nuser input: %s' % (session, message.raw))

    session['message_type'] = 'voice'

    unicode_recognition = u'' + message.recognition
    content_recognition = unicode_recognition[:-1]
    logger.debug('user voice recognition content: ' + content_recognition)

    session_mode = session.get('mode')
    if session_mode == 'post' and content_recognition.isdigit():
        if len(content_recognition) == 7:
            content_recognition = r'nz' + content_recognition
        elif len(content_recognition) == 9:
            content_recognition = r'zy' + content_recognition + 'nz'

    return u'[%s]\n%s' % (unicode_recognition, reply(message.source, content_recognition, session))


@robot.image
@robot.location
@robot.link
def handle_other_type(message, session):
    session_mode = session.get('mode')
    if not session_mode:
        session['mode'] = 'chat'
    logger.debug('[ other message ]\nuser session: %s\nuser input: %s' % (session, message.raw))
    return u'你发了什么？人家还小不明白的啦～'


@robot.subscribe
def welcome(event, session):
    logger.debug('[ subscribe event ]\nuser session: %s\nuser input: %s' % (session, event.raw))
    session['mode'] = 'chat'
    return u'''欢迎和小九做朋友，我会无偿陪你聊天喔～
当然啦，小九还会以下技能。小心不要被吓到咯～
如果你喜欢我记得把我介绍给更多的朋友 ❤️
---------

回复「新西兰快递」开启新西兰快递查询
回复「退出」退出功能模式'''
