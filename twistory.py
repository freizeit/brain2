#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4


"""
Read tweets, persist them to a MongoDB store.
"""


import pprint
import pymongo
import sys

from twisted.internet import task
from twisted.internet import reactor
from twisted.python import log

import twython

from utils import config


log.startLogging(sys.stdout)


api = twython.Twython(**config.get_twitter_config())


def get_since_id(coll, user_name):
    since_id = coll.find_one({"user_name": user_name})
    return since_id if since_id else dict(user_name=user_name, id=0)


def pull_and_save_tweets(api):
    conn = pymongo.Connection()
    cfg = config.get("db")
    db = conn[cfg.get("db")]
    messages = db[cfg.get("messages_coll")]
    messages.ensure_index("id")
    maxids = db[cfg.get("maxids_coll")]

    cfg = config.get("twitter")
    since_id = get_since_id(maxids, cfg.get("user_name"))
    log.msg(pprint.pformat(since_id))

    tweets = []
    try:
        if since_id["id"]:
            tweets = api.getHomeTimeline(since_id=since_id["id"], count=199)
        else:
            tweets = api.getHomeTimeline(count=199)
    except ValueError, e:
        log.err(e)

    log.msg(len(tweets))
    if tweets:
        messages.insert(tweets)
        since_id["id"] = max(int(tweet["id"]) for tweet in tweets)
    maxids.save(since_id)


l = task.LoopingCall(pull_and_save_tweets, api)
cfg = config.get("twitter")
l.start(float(cfg.get("interval", 600))) # call every ten minutes

# l.stop() will stop the looping calls
reactor.run()
