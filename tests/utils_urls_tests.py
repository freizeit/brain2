# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4


import mock
import unittest
import urllib2

from utils import urls


class TestActualUrl(unittest.TestCase):
    """Tests for utils.urls.actual_url()"""

    def test_http_error(self):
        """urllib2.urlopen() throws a urllib2.HTTPError exception."""
        url = "http://t.co/iuZW573"
        code = 404
        with mock.patch("urllib2.urlopen", mocksignature=True) as m:
            m.side_effect=urllib2.HTTPError(url, code, "Blam!", {}, None)
            self.assertEquals("%s (%s)" % (url, code), urls.actual_url(url))

    def test_url_error(self):
        """urllib2.urlopen() throws a urllib2.URLError exception."""
        url = "http://t.co/iuZW573"
        with mock.patch("urllib2.urlopen", mocksignature=True) as m:
            m.side_effect=urllib2.URLError("Bang!")
            self.assertEquals("%s (500)" % url, urls.actual_url(url))

    def test_good_case(self):
        """urllib2.urlopen() does not throw an exception."""
        url = "http://t.co/iuZW573"
        sanitized_url = "http://example.com/a/b/c.html"
        m1 = mock.Mock()
        m1.geturl.side_effect = lambda: sanitized_url
        with mock.patch("urllib2.urlopen", mocksignature=True) as m2:
            m2.side_effect = lambda _url, _data, _proxies: m1
            self.assertEquals(sanitized_url, urls.actual_url(url))


class TestSanitizeUrls(unittest.TestCase):
    """Tests for utils.urls.sanitize_urls()"""

    def test_no_urls(self):
        """
        utils.urls.actual_url will not be called if the tweet contains no
        URLs.
        """
        with mock.patch("utils.urls.actual_url", mocksignature=True) as m:
            urls.sanitize_urls("abc")
            self.assertEquals(0, m.call_count)

    def test_single_url(self):
        """
        utils.urls.actual_url will be called once if the tweet contains a
        single URL.
        """
        data = ("http://www.example.com/1/2",  "http://a.b.c/x/y/z")
        with mock.patch("utils.urls.actual_url", mocksignature=True) as m:
            m.side_effect = lambda _: data[1]
            r = urls.sanitize_urls("see: %s" % data[0])
            self.assertEquals(1, m.call_count)
            self.assertEquals("see: %s" % data[1], r)

    def test_multi_url(self):
        """
        utils.urls.actual_url will be called once per URL contained in
        the tweet.
        """
        data = (("http://a.com/1/2",  "http://x.org/x/y"),
                ("http://b.com/3/4",  "http://y.net/o/p"))
        data = dict(data)
        inputs = tuple(data.keys())
        results = data.values()
        with mock.patch("utils.urls.actual_url", mocksignature=True) as m:
            m.side_effect = lambda _: results.pop(0)
            r = urls.sanitize_urls("see: %s and %s" % inputs)
            self.assertEquals(len(data), m.call_count)
            self.assertEquals("see: %s and %s" % tuple(data.values()), r)
