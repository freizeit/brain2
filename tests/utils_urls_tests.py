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
