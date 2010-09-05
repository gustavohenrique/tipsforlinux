from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tipsforlinux/', include('tipsforlinux.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),

    #(r'^$', 'socialauth.views.signin_complete'),
    (r'^$', 'tips.views.show_latest'),
    (r'^accounts/', include('socialauth.urls')),
    (r'^tips/', include('tips.urls')),
    (r'^contact/', include('contact_form.urls')),
)

from django.conf import settings
if settings.DEBUG:

    urlpatterns += patterns('',
        # This is for the CSS and static files:
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
