#-*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from tips.models import Tip
import datetime

class LatestTipSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Tip.objects.filter(is_public=True, approved=True).order_by('-pub_date')

    def lastmod(self, obj):
        # convert date to datetime format
        d =  obj.pub_date
        return datetime.datetime.combine(d, datetime.time())
