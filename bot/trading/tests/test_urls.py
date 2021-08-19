from django.test import SimpleTestCase
from django.urls import reverse, resolve
from trading.views import *

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, index)
    
    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, registerPage)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, loginPage)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)
    
    def test_add_order_url_is_resolved(self):
        url = reverse('add_order')
        self.assertEquals(resolve(url).func, trading_history_create)

    def test_edit_order_url_is_resolved(self):
        url = reverse('edit_order', args=[10])
        self.assertEquals(resolve(url).func, trading_history_update)

    def test_delete_order_url_is_resolved(self):
        url = reverse('delete_order', args=[10])
        self.assertEquals(resolve(url).func, trading_history_delete)
