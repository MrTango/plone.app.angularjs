# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import getMultiAdapter

from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING


class TestAppIndex(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_view_is_registered(self):
        self.assertTrue(
            getMultiAdapter(
                (self.portal, self.request),
                name="index.html"
            )
        )
