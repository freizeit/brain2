# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4


import re
import urllib2


"""
Various utility functions concerned with URLs.
"""


URL_RE = re.compile('(http://\S+)')


def sanitize_urls(tweet):
    """Find all URLs in the given tweet and sanitize/expand them.

    Tweets are likely to use URL shorteners but we want the actual URLs.

    :param str tweet: the original tweet
    :returns: str -- the tweet with URLs expanded and sanitized
    """
    segs = []
    for seg in URL_RE.split(tweet):
        seg = seg.strip()
        if not seg:
            continue
        if URL_RE.match(seg):
            seg = actual_url(seg)
        segs.append(seg)
    return ' '.join(segs)


def actual_url(url):
    """Return the actual URL, follow any redirections."""
    result = None
    try:
        u = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        result = "%s (%s)" % (url, e.code)
    except urllib2.URLError:
        result = "%s (500)" % url
    else:
        result = u.geturl()
    return result
