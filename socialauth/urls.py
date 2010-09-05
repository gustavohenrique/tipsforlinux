from django.conf.urls.defaults import *
from openid_consumer.views import begin, complete, signout
from django.views.generic.simple import direct_to_template

from django.conf import settings

#Login Views
urlpatterns = patterns('socialauth.views',
    url(r'^facebook_login/xd_receiver.htm$', direct_to_template, {'template':'socialauth/xd_receiver.htm'}, name='socialauth_xd_receiver'),
    url(r'^facebook_login/$', 'facebook_login_done', name='socialauth_facebook_login_done'),
    url(r'^login/$', 'login_page', name='socialauth_login_page'),
    url(r'^openid_login/$', 'openid_login_page', name='socialauth_openid_login_page'),
    url(r'^twitter_login/$', 'twitter_login', name='socialauth_twitter_login'),
    url(r'^twitter_login/done/$', 'twitter_login_done', name='socialauth_twitter_login_done'),
    url(r'^yahoo_login/$', 'yahoo_login', name='socialauth_yahoo_login'),
    url(r'^yahoo_login/complete/$', complete, name='socialauth_yahoo_complete'),
    url(r'^gmail_login/$', 'gmail_login', name='socialauth_google_login'),
    url(r'^gmail_login/complete/$', complete, name='socialauth_google_complete'),
    url(r'^openid/$', 'openid_login', name='socialauth_openid_login'),
    url(r'^openid/complete/$', complete, name='socialauth_openid_complete'),
    url(r'^openid/signout/$', signout, name='openid_signout'),
    url(r'^openid/done/$', 'openid_done', name='openid_openid_done'),
)

#Other views.
urlpatterns += patterns('socialauth.views',
    url(r'^edit/profile/$', 'editprofile',  name='socialauth_editprofile'),                    
    url(r'^logout/$', 'social_logout',  name='socialauth_social_logout'),
    url(r'^common/signin/$', 'signin_common',  name='socialauth_signin_common'),
    url(r'^common/login/$', 'login_common',  name='socialauth_login_common'),
    url(r'^common/signin/confirm/(?P<user_id>.+)/(?P<hash>.+)/$', 'signin_common_confirm', name='socialauth_confirm_signin_common'),
    
    url(r'^common/signin/success/$', direct_to_template, {'template':'socialauth/messages/signin_common_success.html'},  name='socialauth_success_signin_common'),
    url(r'^common/signin/confirmation/success/$', direct_to_template, {'template':'socialauth/messages/signin_common_confirm_success.html'},  name='socialauth_success_signin_common_confirmation'),
    url(r'^common/signin/confirmation/error/$', direct_to_template, {'template':'socialauth/messages/signin_common_confirm_error.html'},  name='socialauth_error_signin_common_confirmation'),
    
) 

