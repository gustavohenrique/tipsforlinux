# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.contrib.comments.views.comments import post_comment
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404

from tagging.models import Tag, TaggedItem
from tips.forms import TipForm
from tips.models import Tip, Bookmark

        

def _show_tips_in_home(request, tips=None, tag=None):
    if tips is None:
        tips = Tip.objects.filter(is_public=True, approved=True)
    
    if not tag is None:
        tips = TaggedItem.objects.get_by_model(tips, tag)
    
    context = {'tips': tips, 'active_menu':'home'}
    return direct_to_template(request, 'index.html', context)
    

def show_latest(request):
    return _show_tips_in_home(request)


def by_tag(request, slug):
    try:
        tag = Tag.objects.get(slug=slug)
        return _show_tips_in_home(request, None, tag)
    except:
        raise Http404
        

def read_more(request, slug):
    tip = get_object_or_404(Tip, slug_title=slug)
    
    if not tip.author == request.user:
        tip.hits = tip.hits + 1
        tip.save()
    
    context = {'tip': tip, 'active_menu':'home'}
    try:
        rating = tip.rating_set.get(user=request.user)
        context.update({'rating': rating})
    except:
        pass
        
    try:
        bookmark = tip.bookmark_set.get(user=request.user)
        context.update({'bookmark': bookmark})
    except:
        pass
    
    return direct_to_template(request, 'read.html', context)


def simple_search(request):
    if 'text' in request.GET:
        text = request.GET['text']
        
        tips = get_list_or_404(Tip, Q(title__icontains=text) | Q(body__icontains=text))
        return _show_tips_in_home(request, tips, None)
    
    return HttpResponseRedirect(reverse('tip-latest'))


@login_required
def mytips(request, form=None):
    if form == None:
        form = TipForm()
    tips = Tip.objects.filter(author=request.user)
    bookmarked_tips = Bookmark.objects.filter(user=request.user)
    
    context = {'tips':tips, 'bookmarked_tips': bookmarked_tips, 'form': form, 'active_menu':'mytips'}
    return direct_to_template(request, 'mytips.html', context)


@login_required
def add_tip(request):
    if request.POST:
        form = TipForm(request.POST)
        try:
            form.save()
            return HttpResponseRedirect(reverse('tip-mytips'))
        except:
            pass
            
        return mytips(request, form)
    return HttpResponseRedirect(reverse('tip-mytips'))


@login_required
def delete_tip(request, id):
    tip = get_object_or_404(Tip, id=id, author=request.user)
    tip.delete()
    return HttpResponseRedirect(reverse('tip-mytips'))


@login_required
def show_edit_form(request, id):
    tip = get_object_or_404(Tip, id=id, author=request.user)
    context = {'form': TipForm(instance=tip), 'active_menu':'mytips'}
    return direct_to_template(request, 'edit.html', context)


@login_required
def update_tip(request):
    if request.POST:
        id = request.POST.get('id')
        tip = get_object_or_404(Tip, id=id, author=request.user)
        form = TipForm(request.POST, instance=tip)
        try:
            form.save()
            return HttpResponseRedirect(reverse('tip-mytips'))
        except:
            pass
            
    context = {'form':form , 'active_menu':'mytips'}
    return direct_to_template(request, 'edit.html', context)


@login_required
def rate_tip(request, id):
    if 'score' in request.GET:
        is_useful = (request.GET.get('score') == 'up')
        tip = get_object_or_404(Tip, id=id)
        
        if not request.user == tip.author:
            try:
                rating = tip.rating_set.get(user=request.user)
                rating.useful = is_useful
                rating.save()
            except:
                rating = tip.rating_set.create(user=request.user, useful=is_useful)
            
            try:
                if '/tips/read/' in request.META['HTTP_REFERER']:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except:
                pass
            
    return HttpResponseRedirect(reverse('tip-mytips'))


@login_required
def bookmark_tip(request, id):
    if 'action' in request.GET:
        tip = get_object_or_404(Tip, pk=id)
        
        if not request.user == tip.author:
            action = request.GET.get('action')
            if action == 'add':
                bookmarked_tip = tip.bookmark_set.get_or_create(user=request.user)
                
            elif action == 'delete':
                try:
                    bookmarked_tip = tip.bookmark_set.get(user=request.user)
                    bookmarked_tip.delete()
                except:
                    pass

            try:
                if '/tips/read/' in request.META['HTTP_REFERER']:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except:
                pass

    return HttpResponseRedirect(reverse('tip-mytips'))
