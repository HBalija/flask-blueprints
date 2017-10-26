import unittest
from flask import url_for

from app import create_app
from app.models import db, User
from config import test


class SiteTestCase(unittest.TestCase):

    def setUp(self):
        """
        Creates app environment with test settings.
        """
        self.app = create_app(test, db)
        self.client = self.app.test_client()
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()
        self.user = User(name='test_user', description='testing')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.app_ctx.pop()

    def test_list_users_suceeds(self):
        resp = self.client.get(url_for('site.users'))
        self.assertEqual(resp.status_code, 200)

    def test_get_user_details_suceeds(self):
        resp = self.client.get(url_for('site.user_details', id=self.user.id))
        self.assertEqual(resp.status_code, 200)

    def test_return_404_if_user_does_not_exist(self):
        resp = self.client.get(url_for('site.user_details', id=24))
        self.assertEqual(resp.status_code, 404)

    def test_get_index(self):
        resp = self.client.get(url_for('site.index'))
        self.assertEqual(resp.status_code, 200)

    def test_create_user(self):
        resp = self.client.post(url_for(
            'site.index', data=dict(name='test_name2', description='desc')))
        self.assertEqual(resp.status_code, 200)

    def test_user_delete_succeeds(self):
        resp = self.client.post(url_for('site.user_delete', id=self.user.id))
        self.assertEqual(resp.status_code, 302)
