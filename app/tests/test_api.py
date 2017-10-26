import unittest
import json
from flask import url_for

from app import create_app
from app.models import db, User
from config import test


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        """
        Create app environment with test settings
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

    def test_users_succeeds(self):
        """
        SERVER_NAME = 'any string' environment variable needs
        to be set for url_for to work
        """
        resp = self.client.get(url_for('api.list_users'))
        self.assertEqual(resp.status_code, 200)

        response_data = json.loads(resp.get_data(as_text=True))

        users = {
            'users': [{
                'id': 1,
                'name': 'test_user',
                'description': 'testing',
            }]
        }
        self.assertEqual(users, response_data)

    def test_get_user_by_id_suceeds(self):
        resp = self.client.get(url_for('api.get_user', id=self.user.id))
        self.assertEqual(resp.status_code, 200)

        response_data = json.loads(resp.get_data(as_text=True))

        users = {
            'user': [{
                'id': 1,
                'name': 'test_user',
                'description': 'testing',
            }]
        }
        self.assertEqual(users, response_data)

    def test_get_user_returns_404_if_does_not_exist(self):
        resp = self.client.get(url_for('api.get_user', id=555))
        self.assertEqual(resp.status_code, 404)

    def test_create_user_succeeds(self):
        data = {'name': 'test_user2'}

        resp = self.client.post(
            'api/users', data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_create_user_fails_if_name_exists(self):
        data = {'name': 'test_user'}
        resp = self.client.post(
            'api/users', data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_delete_user_suceeds(self):
        resp = self.client.delete(url_for('api.get_user', id=self.user.id))
        self.assertEqual(resp.status_code, 204)

    def test_delete_user_returns_404_if_does_not_exist(self):
        resp = self.client.delete(url_for('api.get_user', id=555))
        self.assertEqual(resp.status_code, 404)

    def test_update_user_suceeds(self):
        data = {'name': 'test_user2'}
        resp = self.client.put(
            'api/users/1', data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_update_user_returns_404_if_does_not_exist(self):
        data = {'name': 'test_user2'}
        resp = self.client.put(
            'api/users/555', data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 404)
