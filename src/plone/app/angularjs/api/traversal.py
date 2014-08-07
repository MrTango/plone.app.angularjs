from Products.Five.browser import BrowserView
from zope.component.hooks import getSite

from .api import json_api_call


class TraversalView(BrowserView):

    @json_api_call
    def __call__(self):
        portal = getSite()
        path = self.request.get('path')
        if not path:
            return
        path = '/'.join(portal.getPhysicalPath()) + '/' + path
        try:
            obj = portal.restrictedTraverse(path)
        except KeyError:
            return {'title': 'Object not found.'}
        try:
            text = obj.getText()
        except AttributeError:
            text = ''
        self.request.response.setHeader("Content-Type", "application/json")
        return {
            'route': path,
            'id': obj.id,
            'title': obj.title,
            'description': obj.Description(),
            'text': text
        }
