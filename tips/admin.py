# -*- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin
from django.contrib.sitemaps import ping_google
from django.conf import settings

import twitter
import tinyurl

from tips.models import Tip, Rating, Bookmark
from tips.forms import TipForm

class TipAdmin(ModelAdmin):
    search_fields = ('title', 'body')
    list_display = ('title', 'id', 'author', 'pub_date', 'hits', 'enable_comments', 'is_public', 'approved')
    list_filter = ('author', 'enable_comments', 'is_public', 'approved')
    list_per_page = 20
    date_hierarchy = 'pub_date'
    ordering = ('-id', '-pub_date')
    actions = ['approve', 'post_twitter']
    
    def approve(self, request, queryset):
        queryset.update(approved=True)
        try:
            ping_google()
        except Exception:
            pass
    approve.short_description = 'Approve'
    
    def post_twitter(self, request, queryset):
        for tip in queryset:
            url = "http://%s%s" % (request.get_host(), tip.get_absolute_url())
            short_url = tinyurl.get_tiny_url(url)
            POST_MESSAGE = "%s %s" % (tip.title, short_url)
            
            CONSUMER_KEY = getattr(settings, "TWITTER_CONSUMER_KEY", "")
            CONSUMER_SECRET = getattr(settings, "TWITTER_CONSUMER_SECRET", "")
            TOKEN_KEY = getattr(settings, "TWITTER_ACCESS_TOKEN_KEY", "")
            TOKEN_SECRET = getattr(settings, "TWITTER_ACCESS_TOKEN_SECRET", "")
            try:
                api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, TOKEN_KEY, TOKEN_SECRET)
                api.PostUpdate(POST_MESSAGE)
            except:
                pass
            
    post_twitter.short_description = 'Post in Twitter'
    
site.register(Tip, TipAdmin)

class RatingAdmin(ModelAdmin):
    list_display = ('id', 'tip', 'user', 'useful')
site.register(Rating, RatingAdmin)

site.register(Bookmark)
