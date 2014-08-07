from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component.hooks import getSite

from .api import json_api_call


class TopNavigation(BrowserView):

    @json_api_call
    def __call__(self):
        portal = getSite()
        catalog = getToolByName(portal, 'portal_catalog')
        portal_path = '/'.join(portal.getPhysicalPath())
        return [
            {
                'id': brain.id,
                'title': brain.Title,
                'description': brain.description,
                'url': brain.getPath().replace(
                    portal_path, ''
                ).lstrip('/')
            }
            for brain in catalog({
                'path': {
                    'query': '/'.join(portal.getPhysicalPath()),
                    'depth': 1
                },
                'portal_type': 'Folder',
                'sort_on': 'getObjPositionInParent'
            }) if brain.exclude_from_nav is not True
        ]


class NavigationTree(BrowserView):

    @json_api_call
    def __call__(self):
        portal = getSite()
        catalog = getToolByName(portal, 'portal_catalog')
        portal_path = '/'.join(portal.getPhysicalPath())

        def _get_children(context):
            return [
                {
                    'id': brain.id,
                    'title': brain.Title,
                    'description': brain.description,
                    'url': brain.getPath().replace(
                        portal_path, ''
                    ).lstrip('/'),
                    'children': []
                } for brain in catalog({
                    'path': {'query': context.getPath(), 'depth': 1},
                    'sort_on': 'getObjPositionInParent',
                    }
                ) if brain.exclude_from_nav is not True
            ]
        return [
            {
                'id': brain.id,
                'title': brain.Title,
                'description': brain.description,
                'url': brain.getPath().replace(
                    portal_path, ''
                ).lstrip('/'),
                'children': _get_children(brain)
            }
            for brain in catalog(
                {
                    'path': {'query': portal_path, 'depth': 1},
                    'sort_on': 'getObjPositionInParent',
                }
            ) if brain.exclude_from_nav is not True
        ]
