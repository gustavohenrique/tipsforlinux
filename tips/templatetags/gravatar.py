import urllib, hashlib
from django import template

register = template.Library()

@register.simple_tag
def gravatar(email, size=48):
    """
    Simply gets the Gravatar for the commenter. There is no rating or
    custom "not found" icon yet. Used with the Django comments.
    
    If no size is given, the default is 48 pixels by 48 pixels.
    
    Template Syntax::
    
        {% gravatar comment.user_email [size] %}
        
    Example usage::
        
        {% gravatar comment.user_email 48 %}
    
    """
    
    url = "http://www.gravatar.com/avatar.php?"
    url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(), 
        'size': str(size)
    })
    
    return """<img src="%s" width="%s" height="%s" alt="" class="avatar avatar-48 photo avatar-default" border="0" />""" % (url, size, size)
