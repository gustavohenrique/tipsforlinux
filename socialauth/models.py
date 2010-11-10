from django.db import models
from django.contrib.auth.models import User
from django.db import connection, transaction
from django.core.mail import EmailMessage
from django.conf import settings

class CustomerUser(User):
    class Meta:
        proxy = True
        
    def _send_mail_to_admin(self):
        subject = '[USER] New user registered on tipsforlinux.com'
        message = 'Name: %s %s\nUsername: %s\nE-mail: %s' % (self.first_name, self.last_name, self.username, self.email)

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [mail_tuple[1] for mail_tuple in settings.ADMINS]
        
        mail = EmailMessage(subject, message, from_email, recipient_list)
        try:
            mail.send()
        except:
            pass
        
    def save(self, *args, **kwargs):
        if not self.id:
            self._send_mail_to_admin()
        super(User, self).save(*args, **kwargs)
        
        

class AuthMeta(models.Model):
    """Metadata for Authentication"""
    def __unicode__(self):
        return '%s - %s' % (self.user, self.provider)
    
    user = models.OneToOneField(User)
    provider = models.CharField(max_length = 30)
    is_email_filled = models.BooleanField(default = False)
    is_profile_modified = models.BooleanField(default = False)

class OpenidProfile(models.Model):
    """A class associating an User to a Openid"""
    openid_key = models.CharField(max_length=200,unique=True)
    
    user = models.ForeignKey(User)
    is_username_valid = models.BooleanField(default = False)
    #Values which we get from openid.sreg
    email = models.EmailField()
    nickname = models.CharField(max_length = 100)
    
    
    def __unicode__(self):
        return unicode(self.openid_key)
    
    def __repr__(self):
        return unicode(self.openid_key)
    

class TwitterUserProfile(models.Model):
    """
    For users who login via Twitter.
    """
    screen_name = models.CharField(max_length = 200, unique = True)
    
    user = models.ForeignKey(User)
    access_token = models.CharField(max_length=255, blank=True, null=True, editable=False)
    profile_image_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)

    def __str__(self):
            return "%s's profile" % self.user
        

class FacebookUserProfile(models.Model):
    """
    For users who login via Facebook.
    """
    facebook_uid = models.CharField(max_length = 20, unique = True)
    
    user = models.ForeignKey(User)
    profile_image_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    about_me = models.CharField(max_length=160, blank=True, null=True)
    
    



