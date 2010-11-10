# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core import mail
from django.contrib.auth.models import User

from tips.models import Tip
from tips.forms import TipForm


class NavegationTest(TestCase):
    
    fixtures = ['auth.json', 'tips.json', 'tags.json']
    
    def setUp(self):
        self.c = Client(enforce_csrf_checks=True)

    
    def test_show_main_page(self):
        response = self.c.get('/tips/')
        self.assertEquals(200, response.status_code)


    def test_deny_mytips_page_for_no_logged_users(self):
        response = self.c.get('/tips/mytips/')
        self.assertEquals(302, response.status_code)
    
        
    def test_allow_mytips_page_for_authenticated_user(self):
        self.c.login(username='admin', password='admin')
        response = self.c.get('/tips/mytips/')
        self.assertEquals(200, response.status_code)
    
    
    def test_show_title_and_description_fields_in_new_tip_page(self):
        self.c.login(username='admin', password='admin')
        response = self.c.get('/tips/mytips/')
        form_in_page = response.context['form']
        self.assertEquals(['title', 'body', 'is_public', 'enable_comments', 'tags', 'id'], form_in_page.fields.keys())
    
    
    def test_show_tag_list_with_5_itens_in_sidebar(self):
        response = self.c.get('/')
        tag_list_left = response.context['tag_list_left']
        tag_list_right = response.context['tag_list_right']
        
        self.assertEquals(3, len(tag_list_left))
        self.assertEquals(2, len(tag_list_right))
        
    
    def test_show_top_tip_list_with_5_itens_in_sidebar(self):
        response = self.c.get('/')
        top_tips = response.context['top_tips']
        self.assertEquals(5, len(top_tips))
    
    
    def test_show_full_tip_page(self):
        response = self.c.get('/tips/read/4/other-method-to-restart-samba', follow=True)
        tip = response.context['tip']
        self.assertEquals('Other method to restart samba', tip.title)
        self.assertEquals(4, tip.id)
        self.assertEquals("$ sudo kill -HUP `cat /var/run/samba/smbd.pid`", tip.body)
        self.assertEquals('samba', tip.get_tags()[0].slug)

    
    def test_show_two_tips_in_mytips_page(self):
        self.c.login(username='admin', password='admin')
        response = self.c.get('/tips/mytips/')
        tips = response.context['tips']
        self.assertEquals(5, tips.count())

    
    def test_show_edit_form_for_tip_with_id_equal_one(self):
        self.c.login(username='admin', password='admin')
        response = self.c.get('/tips/edit/1', follow=True)
        form_in_page = response.context['form']      
        self.assertEquals(['title', 'body', 'is_public', 'enable_comments', 'tags', 'id'], form_in_page.fields.keys())
    
    
    def test_simple_search(self):
        response = self.c.get('/tips/search/?text=xorg')
        tips = response.context['tips']
        self.assertEquals(1, len(tips))
    
    
    def test_rating_tip_as_useful(self):
        self.c.login(username='gustavo', password='henrique')
        self.c.get('/tips/rate/2/?score=up', follow=True)
        response = self.c.get('/tips/read/2/configure-x', follow=True)
        rating = response.context['rating']
        self.assertEquals('useful', rating.get_rating())
    
    
    def test_rating_tip_as_not_useful_after_rating_as_useful(self):
        self.c.login(username='gustavo', password='henrique')
        self.c.get('/tips/rate/2/?score=up', follow=True)
        response = self.c.get('/tips/read/2/configure-x', follow=True)
        rating = response.context['rating']
        self.assertEquals('useful', rating.get_rating())
        
        self.c.get('/tips/rate/2/?score=down', follow=True)
        response = self.c.get('/tips/read/2/configure-x', follow=True)
        rating = response.context['rating']
        self.assertEquals('not useful', rating.get_rating())
       
    
    def test_add_tip_on_bookmark(self):
        self.c.login(username='gustavo', password='henrique')
        response = self.c.get('/tips/bookmark/2/?action=add', follow=True)
        bookmarked_tips = response.context['bookmarked_tips']
        self.assertEquals(1, len(bookmarked_tips))
    
    
    def test_do_not_add_duplicated_tip_on_bookmark(self):
        self.c.login(username='gustavo', password='henrique')
        response = self.c.get('/tips/bookmark/2/?action=add', follow=True)
        response = self.c.get('/tips/bookmark/2/?action=add', follow=True)
        bookmarked_tips = response.context['bookmarked_tips']
        self.assertEquals(1, len(bookmarked_tips))
    
    
    def test_delete_tip_on_bookmark(self):
        self.c.login(username='gustavo', password='henrique')
        response = self.c.get('/tips/bookmark/2/?action=delete', follow=True)
        bookmarked_tips = response.context['bookmarked_tips']
        self.assertEquals(0, len(bookmarked_tips))


class TipTest(TestCase):
    
    fixtures = ['auth.json', 'tips.json']
    
    def setUp(self):
        self.user = User.objects.get(username='admin')
    
        
    def test_create_unique_slug_for_each_tip(self):
        t = Tip()
        t.author = self.user
        t.title = 'Solução para Desligamento Rápido'
        t.body = '# halt'
        t.save()
        self.assertEquals('solucao-para-desligamento-rapido', t.slug_title)
        
        t = Tip()
        t.author = self.user
        t.title = 'Solução para Desligamento Rápido'
        t.body = 'Digite halt no terminal'
        t.save()
        self.assertEquals('solucao-para-desligamento-rapido-1', t.slug_title)
    
    
    def test_create_tip_with_two_tags(self):
        t = Tip()
        t.author = self.user
        t.title = 'Share files using samba3'
        t.body = 'Using samba you will can be share files on network.'
        t.tags = 'samba linux'
        t.save()
        self.assertEquals('samba linux', t.tags)
