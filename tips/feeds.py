#-*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from tips.models import Tip
import datetime

class LatestTipFeed(Feed):
    title = "Tips For Linux site news"
    link = "/tips/"
    description = "Updates on changes and additions to tipsforlinux.com."

    def items(self):
        return Tip.objects.filter(is_public=True, approved=True).order_by('-pub_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[:140]
        
    def item_author_name(self, item):
        return item.author
    
    def item_pubdate(self, item):
        # convert date to datetime format
        d =  item.pub_date
        return datetime.datetime.combine(d, datetime.time())

