# -*- coding: utf-8 -*-
import json

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.angularjs.interfaces import IRestApi
from zope.component import (
    getMultiAdapter, getGlobalSiteManager)
from zope.component.interfaces import ComponentLookupError
from zope.component.hooks import getSite

import logging
log = logging.getLogger("plone.app.angularjs.api")


def json_api_call(func):
    """ decorator to return all values as json
    """
    def decorator(*args, **kwargs):
        instance = args[0]
        request = getattr(instance, 'request', None)
        request.response.setHeader(
            'Content-Type',
            'application/json; charset=utf-8'
        )
        result = func(*args, **kwargs)
        return json.dumps(result, indent=2, sort_keys=True)

    return decorator


class ApiDispatcherView(BrowserView):
    """ dispatch api calls to api views via lookup on view name and IRestApi
    """
    def __call__(self, context=None, request=None):
        api_params = self.request.get('api_params')
        if api_params:
            name = api_params[0]
        else:
            name = ''
        try:
            view = getMultiAdapter(
                (self.context, self.request),
                IRestApi,
                name=name)
            return view()
        except ComponentLookupError:
            log.debug("No API View found with name '%s'" % name)
        return json.dumps({
            'code': '404',
            'message': "API method '%s' not found." % name,
            'data': ''
        })


class ApiOverview(BrowserView):
    """ Api overview, list all api endpoints.
    """
    template = ViewPageTemplateFile('api.pt')

    def __call__(self):
        return self.template()

    def api_views(self):
        portal_url = getSite().absolute_url()
        gsm = getGlobalSiteManager()
        api_views = []
        for api_adapter in gsm.registeredAdapters():
            if not api_adapter.provided == IRestApi:
                continue
            api_view = {}
            api_view['id'] = api_adapter.name
            view = getMultiAdapter(
                (self.context, self.request),
                IRestApi,
                name=api_adapter.name)
            # XXX this doesn't work because we don't have the original
            # class here. How we can get the original class?
            api_view['description'] = view.__doc__
            api_view['url'] = '%s/++api++v1/%s' % (
                portal_url, api_adapter.name)
            api_views.append(api_view)
        return api_views
