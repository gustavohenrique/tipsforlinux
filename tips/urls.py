from django.conf.urls.defaults import *
from tips.feeds import LatestTipFeed

urlpatterns = patterns('',
    url(r'^$', 'tips.views.show_latest', name='tip-latest'),    
    url(r'^mytips/$', 'tips.views.mytips', name='tip-mytips'),
    url(r'^read/(?P<slug>[a-zA-Z0-9_.-]+)/$', 'tips.views.read_more', name='tip-read'),
    url(r'^edit/(?P<id>.+)/$', 'tips.views.show_edit_form', name='tip-edit'),
    url(r'^delete/(?P<id>.+)/$', 'tips.views.delete_tip', name='tip-delete'),
    url(r'^add/$', 'tips.views.add_tip', name='tip-add'),
    url(r'^update/$', 'tips.views.update_tip', name='tip-update'),
    url(r'^by/(?P<slug>[a-zA-Z0-9_.-]+)/$', 'tips.views.by_tag', name='tips-by-tag'),
    url(r'^search/$', 'tips.views.simple_search', name='tip-simple-search'),
    url(r'^rate/(?P<id>.+)/$', 'tips.views.rate_tip', name='tip-rate'),
    url(r'^bookmark/(?P<id>.+)/$', 'tips.views.bookmark_tip', name='tip-bookmark'),
    url(r'^feed/$', LatestTipFeed(), name='tip-feed'),

)
