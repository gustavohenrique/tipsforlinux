# -*- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin

from django.contrib.sitemaps import ping_google

from tips.models import Tip, Rating, Bookmark
from tips.forms import TipForm

class TipAdmin(ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'hits', 'enable_comments', 'is_public', 'approved')
    list_filter = ('author', 'enable_comments', 'is_public', 'approved')
    actions = ['approve', ]
    
    def approve(self, request, queryset):
        queryset.update(approved=True)
        try:
            ping_google()
        except Exception:
            pass
        
    approve.short_description = 'Approve'
    
site.register(Tip, TipAdmin)

class RatingAdmin(ModelAdmin):
    list_display = ('id', 'tip', 'user', 'useful')
site.register(Rating, RatingAdmin)

site.register(Bookmark)
