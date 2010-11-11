# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.forms import forms
from django.conf import settings
from django.forms.widgets import TextInput
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.forms.widgets import HiddenInput
from django.forms.fields import IntegerField
from django.core.mail import EmailMessage

from tagging.forms import TagField
from tagging.models import Tag
from tips.models import Tip


class AutoCompleteTagInput(TextInput):
    
    class Media:
        css = {
            'all': ('%s/js/jquery/jquery.autocomplete.css' % settings.MEDIA_URL,)
        }
        js = (
            '%s/js/jquery.js' % settings.MEDIA_URL,
            '%s/js/jquery/lib/jquery.bgiframe.min.js' % settings.MEDIA_URL,
            '%s/js/jquery/lib/jquery.ajaxQueue.js' % settings.MEDIA_URL,
            '%s/js/jquery/jquery.autocomplete.js' % settings.MEDIA_URL
        )

    def render(self, name, value, attrs=None):
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)
        #page_tags = Tag.objects.usage_for_model(Lancamento)
        page_tags = Tag.objects.all()
        tag_list = simplejson.dumps([tag.name for tag in page_tags],
                                    ensure_ascii=False)
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                width: 150,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
                });
            </script>''' % (name, tag_list))


class TipForm(ModelForm):
    id = IntegerField(required=False, widget=HiddenInput())
    tags = TagField(max_length=50, label='Tags', required=False, widget=AutoCompleteTagInput())
    
    class Meta:
        model = Tip
        exclude = ['author', 'slug_title', 'pub_date', 'hits', 'approved']
        
    def __init__(self, *args, **kwargs):
        super(TipForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.initial['tags'] = ' '.join([item.name for item in Tag.objects.get_for_object(self.instance)])
    
    def save(self, *args, **kwargs):        
        self.instance.approved = settings.APPROVE_NEW_TIPS_AUTOMATICALY
        super(TipForm, self).save(*args, **kwargs)
        
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [mail_tuple[1] for mail_tuple in settings.ADMINS]
        
        subject = '[TIP] %s' % self.instance.slug_title
        message = "Author: %s \nE-mail: %s\n\n%s\n\n%s" % (self.instance.author, self.instance.author.email, self.instance.title, self.instance.body)
        mail = EmailMessage(subject, message, from_email, recipient_list)
        try:
            mail.send()
        except:
            pass

