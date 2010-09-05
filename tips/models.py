# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.template.defaultfilters import slugify
from django.conf import settings

from middleware import threadlocals

from tagging.fields import TagField
from tagging.models import Tag


class Tip(models.Model):
    author = models.ForeignKey(User, editable=False, default=threadlocals.get_current_user) 
    title = models.CharField(max_length=50)
    slug_title = models.SlugField(max_length=150, blank=True, null=True)
    body = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    enable_comments = models.BooleanField(default=True)
    hits = models.IntegerField(default=0)
    tags = TagField()
    
    class Meta:
        ordering = ['-pub_date',]
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return '/tips/read/%s' % self.slug_title
    
    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)    

 
def tip_pre_save(signal, instance, sender, **kwargs):
    #if not instance.slug_title:
    slug = slugify(instance.title)
    new_slug = slug
    counter = 0

    while Tip.objects.filter(slug_title=new_slug).exclude(id=instance.id).count() > 0:
        counter += 1
        new_slug = '%s-%d'%(slug, counter)

    instance.slug_title = new_slug
signals.pre_save.connect(tip_pre_save, sender=Tip)
    

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    tip = models.ForeignKey(Tip)
    mark_date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s by %s (bookmarked in %s)' % (self.tip, self.user, self.mark_date)


class Rating(models.Model):
    user = models.ForeignKey(User)
    tip = models.ForeignKey(Tip)
    useful = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % self.useful
    
    def get_rating(self):
        if self.useful:
            return u'useful'
        return u'not useful'


