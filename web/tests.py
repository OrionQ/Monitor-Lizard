from django.test import TestCase, Client
from django.http import JsonResponse
from django.contrib.auth.models import User
import web.models as models
import web.controllers
import ast

# Create your tests here.


class WebTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('admin', password='pass')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        testHost = models.Host.objects.create(guid="eb651255-e95c-41e8-8bf6-5c405eaf5061")
        testHost.save()
        testTag = models.HostTag.objects.create(name="Unsorted")
        testTag.hosts.set([testHost])

    def testFakeLogin(self):
        c = Client()
        #try logging into a fake user
        response = c.post('/login/', {'username': 'fakeadmin', 'password': 'fakepass'})
        self.assertEqual(response.status_code, 200)
        #assert that we can't access pages, redirect back to login
        response = c.get('/tag/Unsorted/')
        self.assertRedirects(response,'/login/?next=/tag/Unsorted/')

    def testLoginLogout(self):
        c = Client()
        response = c.post('/login/', {'username': 'admin', 'password': 'pass'})
        self.assertEqual(response.status_code, 302)
        response = c.get('/logout/')
        self.assertRedirects(response,'/login/')

    def testTagPage(self):
        c = Client()
        response = c.post('/login/', {'username': 'admin', 'password': 'pass'})
        self.assertEqual(response.status_code, 302)
        response = c.get('/tag/Unsorted/')
        self.assertEqual(response.status_code, 200)

    def testHostPage(self):
        c = Client()
        response = c.post('/login/', {'username': 'admin', 'password': 'pass'})
        self.assertEqual(response.status_code, 302)
        response = c.get('/host/eb651255-e95c-41e8-8bf6-5c405eaf5061/')
        self.assertEqual(response.status_code, 200)

    def testRegisterHost(self):
        c = Client()
        response = c.post('/api/host/')
        self.assertEqual(response.status_code, 200)
        responseJson = ast.literal_eval(response.content.decode("UTF-8"))
        self.assertIn('guid',responseJson)