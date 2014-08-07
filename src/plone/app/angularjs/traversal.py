# from zope.component import getUtility
# from plone.app.angularjs.interfaces import IRestApi
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import adapts
from plone.dexterity.interfaces import IDexterityItem
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.app.angularjs.app.index import AngularAppRootView
from plone.app.angularjs.api.traverser import IAPIRequest
from plone.app.angularjs.api.api import ApiDispatcherView, ApiOverview


class AngularAppPortalRootTraverser(DefaultPublishTraverse):
    adapts(IPloneSiteRoot, IBrowserRequest)

    def publishTraverse(self, request, name):
        if IAPIRequest.providedBy(request):
            if name in ['', 'folder_listing', 'front-page']:
                return ApiOverview(self.context, self.request)
            else:
                parameters = []
                while self.hasMoreNames():
                    if not name.startswith('@@'):
                        parameters.append(name)
                        name = self.nextName()

                if not name.startswith('@@'):
                    # don't add the last param if it starts with '@@'
                    parameters.append(name)
                request.set('api_params', parameters)
                return ApiDispatcherView(self.context, request)
        is_front_page = request.URL.endswith('front-page')
        no_front_page = \
            request.URL.endswith('folder_listing') or \
            request.URL.endswith('folder_contents')
        if is_front_page or no_front_page:
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
        return super(AngularAppPortalRootTraverser, self).publishTraverse(
            request,
            name
        )


    def nextName(self):
        """ Pop the next name off of the traversal stack.
        """
        return self.request['TraversalRequestNameStack'].pop()

    def hasMoreNames(self):
        """ Are there names left for traversal?
        """
        return len(self.request['TraversalRequestNameStack']) > 0


class AngularAppRedirectorTraverser(DefaultPublishTraverse):
    adapts(IDexterityItem, IBrowserRequest)
    # XXX: Adapting IContentish works only for Archetypes content objects:
    # from Products.CMFCore.interfaces import IContentish
    # adapts(IContentish, IBrowserRequest)
    #
    # XXX: Adapting to IDexterityContent collides with the traversal in
    # plone.dexterity/plone/dexterity/browser/traversal.py

    def publishTraverse(self, request, name):
        if not IPloneSiteRoot.providedBy(self.context):
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
        return super(AngularAppRedirectorTraverser, self).publishTraverse(
            request,
            name
        )
