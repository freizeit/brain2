# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4


"""
Various utility functions concerned with configuration.
"""

import ConfigParser
import os


def get_twitter_config():
    return dict(
        twitter_token=os.environ.get("EP11_CONSUMER_KEY"),
        twitter_secret=os.environ.get("EP11_CONSUMER_SECRET"),
        oauth_token=os.environ.get("EP11_ACCESS_TOKEN_KEY"),
        oauth_token_secret=os.environ.get("EP11_ACCESS_TOKEN_SECRET"))


def singleton(cls):
    """This class decorator facilitates the definition of singletons."""
    instances = {}

    def getinstance():
        """
        Return an instance from the cache if present, create one otherwise.
        """
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class Config(object):
    cfg = dict()

    def __init__(self):
        self.load_from_file()

    def set(self, name, value):
        self.cfg[name] = value

    def get(self, name):
        return self.cfg.get(name)

    def load_from_file(self):
        config = ConfigParser.SafeConfigParser()
        default_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "brain2.cfg"))
        path = os.environ.get("BRAIN2_CONFIG_PATH", default_path)
        config.readfp(open(path))
        for section in config.sections():
            self.cfg[section] = dict(config.items(section))


def set(name, value):
    Config().set(name, value)


def get(name):
    return Config().get(name)
