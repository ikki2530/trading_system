from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase, Client
from django.urls import reverse
from trading.models import *
import json


class TestViews(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(username='testuser', password='testuser30')
        self.client = Client()
        # user = get_user_model().objects.create_user(username='testuser', password="betspoker30")


    def test_index_GET(self):
        url = reverse('home')
        login = self.client.login(username='testuser', password='testuser30')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './index.html')

    # def test_registerPage_loggedin_GET(self):
    #     url = reverse('register')
    #     print("url", url)
    #     login = self.client.login(username='testuser', password='testuser30')
    #     print("login register", login)
    #     response = self.client.get(url)
        
    #     print("response", response)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, './index.html')

    def test_registerPage_loggedout_GET(self):
        url = reverse('register')
        # login = self.client.login(username='testuser', password='testuser30')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './register.html')

    # test test_loginPage_loggedin_GET

    def test_loginPage_loggedout_GET(self):
        url = reverse('login')
        # login = self.client.login(username='testuser', password='testuser30')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './login.html')

    # def test_logoutUser_loggedin_GET(self):
    #     url = reverse('logout')
    #     # login = self.client.login(username='testuser', password='testuser30')
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, './login.html')

    def test_trading_history_create_loggedout_GET(self):
        url = reverse('add_order')
        login = self.client.login(username='testuser', password='testuser30')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './history_form.html')

    # def test_trading_history_update_loggedout_GET(self):
    #     url = reverse('edit_order', args=[10])
    #     print("url", url)
    #     login = self.client.login(username='testuser', password='testuser30')
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, './history_form.html')

    # def test_trading_history_delete_loggedin_GET(self):
    #     url = reverse('delete_order', args=[10])
    #     login = self.client.login(username='testuser', password='testuser30')
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, './delete.html')