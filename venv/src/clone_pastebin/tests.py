from datetime import datetime
from urllib import response
from venv import create

import pytz
from django.test import Client, TestCase

from .forms import PastebinForm
from .models import PastebinClone

# Create your tests here.

class TestViews(TestCase):
    
    def postPastebin(self):
        self.client.post('/pastebins/new/', {'title': 'test-title', 'body': 'test-body'}, follow=True)

    def testPostPastebin(self):
        response = self.client.post('/pastebins/new/', {'title': 'test-title', 'body': 'test-body'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/pastebins/1/')
        pastebin = PastebinClone.objects.get(pk=1)
        self.assertEqual(pastebin.title, 'test-title')
        self.assertEqual(pastebin.body, 'test-body')
    
    def testPostLongTitlePastebinNotAllowed(self):
        response = self.client.post('/pastebins/new/', {'title': 't' * 256, 'body': 'test-body'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Location' in response.headers.keys())

    def testGetNewPastebin(self):
        response = self.client.get('/pastebins/new/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.redirect_chain)
    
    def testGetPastebinDetailView(self):
        self.postPastebin()
        response = self.client.get('/pastebins/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Title: test-title' in response.content.decode('UTF-8'))
        self.assertTrue('Content: test-body' in response.content.decode('UTF-8'))

    def testGetEditPage(self):
        self.postPastebin()
        response = self.client.get('/pastebins/1/edit/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.redirect_chain)
    
    def testPostEditPage(self):
        self.postPastebin()
        response = self.client.post('/pastebins/1/edit/', {'title': 'new-title', 'body': 'new-body'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/pastebins/1/')
        pastebin = PastebinClone.objects.get(pk=1)
        self.assertEqual(pastebin.title, 'new-title')
        self.assertEqual(pastebin.body, 'new-body')
    
    def testPostEditPageLongTitle(self):
        self.postPastebin()
        response = self.client.post('/pastebins/1/edit/', {'title': 't' * 256, 'body': 'new-body'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Location' in response.headers.keys())
        pastebin = PastebinClone.objects.get(pk=1)
        self.assertEqual(pastebin.title, 'test-title')
        self.assertEqual(pastebin.body, 'test-body')
    
    def testPostEditPageShortTitle(self):
        self.postPastebin()
        response = self.client.post('/pastebins/1/edit/', {'title': 't', 'body': 'new-body'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Location' in response.headers.keys())
        pastebin = PastebinClone.objects.get(pk=1)
        self.assertEqual(pastebin.title, 'test-title')
        self.assertEqual(pastebin.body, 'test-body')
    
    def testPostEditPageShortBody(self):
        self.postPastebin()
        response = self.client.post('/pastebins/1/edit/', {'title': 'test-title', 'body': 't'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Location' in response.headers.keys())
        pastebin = PastebinClone.objects.get(pk=1)
        self.assertEqual(pastebin.title, 'test-title')
        self.assertEqual(pastebin.body, 'test-body')
    
    def testDeletePastebin(self):
        self.postPastebin()
        self.assertEqual(len(PastebinClone.objects.all()), 1)
        response = self.client.post('/pastebins/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(PastebinClone.objects.all()), 0)

class TestModels(TestCase):
    def create_PastebinClone(self, title='test-title', body='test-body'):
        return PastebinClone.objects.create(title=title, body=body)
    
    def testPastebinCloneCreation(self):
        pastebin = self.create_PastebinClone()
        self.assertTrue(isinstance(pastebin, PastebinClone))
        self.assertEqual(pastebin.__str__(), pastebin.title)

class TestForms(TestCase):
    def testValidForm(self):
        pastebin = PastebinClone.objects.create(title="test-title", body="test-body")
        data = {'title': pastebin.title, 'body': pastebin.body}
        form = PastebinForm(data=data)
        self.assertTrue(form.is_valid())
    
    def testShortTitleFormNotAllowed(self):
        pastebin = PastebinClone.objects.create(title="t", body="test-body")
        data = {'title': pastebin.title, 'body': pastebin.body}
        form = PastebinForm(data=data)
        self.assertFalse(form.is_valid())

    def testShortBodyFormNotAllowed(self):
        pastebin = PastebinClone.objects.create(title="test-title", body="t")
        data = {'title': pastebin.title, 'body': pastebin.body}
        form = PastebinForm(data=data)
        self.assertFalse(form.is_valid())
    
    def testLongTitleFormNotAllowed(self):
        pastebin = PastebinClone.objects.create(title="t" * 256, body="test-body")
        data = {'title': pastebin.title, 'body': pastebin.body}
        form = PastebinForm(data=data)
        self.assertFalse(form.is_valid())
    