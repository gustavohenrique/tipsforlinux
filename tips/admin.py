# -*- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin
from django.contrib.sitemaps import ping_google
from django.conf import settings
from django.core.mail import EmailMessage

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
    actions = ['approve', 'reject', 'post_twitter']

    def _notificate_user_about_rejection_for(self, tip):
        
        message_pt_br = u"""\
        Desculpe.
        
        A dica %s foi rejeitada no site tipsforlinux.com.
        Há 2 possíveis motivos para isso:

        1. A dica talvez tenha sido duplicada ou há outro dica muito parecida.
        2. A dica é inapropriada. O assunto não tem relação com o tipo de conteúdo do site.

        Agradecemos pela compreensão!
        """ % tip.title

        message_en_us = u"""\
        Sorry.

        The tip %s has been rejected on tipsforlinux.com.
        There are two possible reasons for this:

        1. The tip was maybe duplicated or there is another tip very similar.
        2. The tip is inappropriate. The subject is not on the contents of the site.

        Thank you for understanding!
        """ % tip.title

        subject = 'Your tip has been rejected on tipsforlinux.com website'
        message = "%s\n\n----------------------------\n\n\n%s" % (message_pt_br, message_en_us)
        mail = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [tip.author.email, ])
        mail.send()
        
    def approve(self, request, queryset):
        queryset.update(approved=True)
        try:
            ping_google()
        except Exception:
            pass
    approve.short_description = 'Approve'

    def reject(self, request, queryset):
        queryset.update(approved=False)
        first_tip = [ tip for tip in queryset ][0]
        try:
            self._notificate_user_about_rejection_for(first_tip)
            ping_google()
        except Exception:
            pass
    reject.short_description = 'Reject'
    
    def post_twitter(self, request, queryset):
        for tip in queryset:
            url = "http://%s%s" % (request.get_host(), tip.get_absolute_url())
            short_url = tinyurl.get_tiny_url(url)
            
            POST_MESSAGE = u"%s %s" % (tip.title, short_url)
            try:
                POST_MESSAGE = POST_MESSAGE.encode('utf-8')
            except:
                pass
                
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
