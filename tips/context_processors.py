# -*- coding: utf-8 -*-
from tagging.models import Tag
from tips.models import Tip


def menu(request):
    context = {}
    context.update(tags())
    context.update(top_tips())
    return context
    
    
def tags():
    tags = Tag.objects.all()[:40]
    total_tags = tags.count()
    size_left_list = (total_tags / 2) + (total_tags % 2)
    
    tag_list_left = []
    tag_list_right = []
    counter = 0
    for tag in tags:
        if counter < size_left_list:
            tag_list_left.append(tag)
        else:
            tag_list_right.append(tag)
            
        counter += 1
    
    return {
        'tag_list_left': tag_list_left,
        'tag_list_right': tag_list_right
    }


def top_tips():
    top_tips = Tip.objects.filter(is_public=True, approved=True).order_by('-hits')[:20]
    return {'top_tips': top_tips}
