#!flask/bin/python
import os
import unittest
from . import app, db, models, forms
from flask import url_for
from test_base import BaseTestCase
from .models import Teachers
import datetime


class UserViewsTests(BaseTestCase):
    def test_users_can_login(self):
        with self.client:
            Teachers.create(name='Joe', email='joe@joes.com', password='12345')

            response = self.client.post(url_for('login'),
                                        data={'email': 'joe@joes.com', 'password': '12345', 'name': 'Joe'})

            self.assert_redirects(response, url_for('dashboard'))
            self.assertTrue(current_user.name == 'Joe')
            self.assertFalse(current_user.is_anonymous())

    def test_users_can_signup(self):
        with self.client:
            Teachers.create(name='Joe', email='joe@joes.com', password='12345', registered_on=datetime.datetime.utcnow())

            response = self.client.post(url_for('signup'),
                                        data={'email': 'joe@joes.com', 'password': '12345', 'name': 'Joe'})

            self.assert_redirects(response, url_for('login'))
            self.assertTrue(current_user.name == 'Joe')
            self.assertTrue(current_user.is_anonymous())

    def test_users_can_logout(self):  
        with self.client:
            Teachers.create(name="Joe", email="joe@joes.com", password="12345")
            self.client.post(url_for('login'),
                             data={'email': "joe@joes.com",
                                   "password": "12345"})
            self.client.get(url_for('logout'))

            self.assertTrue(current_user.is_anonymous())


