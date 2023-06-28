import unittest  # libreria de python para realizar test
from config.qa import config
from app.models import Employee, Department, User
from app.authentication import authorize
from app import create_app
from flask_sqlalchemy import SQLAlchemy
import json
import io as io
import random
import string


def random_username(char_num):
    return ''.join(random.choice(string.ascii_lowercase)
                   for _ in range(char_num))


class EmployeesTests(unittest.TestCase):
    def setUp(self):
        database_path = config['DATABASE_URI']
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client()

        self.new_department = {
            'name': 'DepPrueba',
            'short_name': 'DP'
        }

        self.invalid_new_department = {
            'name': None,
            'short_name': 'asklcnaslkndlkandlasdnalkdnlasdnlasndlkasndlksandlksandlksandaslknd',
        }

        self.new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
            'selectDepartment': 'c8d29a66-f718-45fe-9a4c-d70013d7fdc6',
        }

        self.invalid_new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
        }

        self.new_authenticated_user = {
            'username': random_username(10),
            'password': '147258369',
            'confirmationPassword': '147258369'
        }

        response_user = self.client.post(
            '/users', json=self.new_authenticated_user)
        data_user = json.loads(response_user.data)
        self.user_valid_token = data_user['token']

    # /users

    # /departments

    def test_create_department_success(self):

        response = self.client.post('/departments', json=self.new_department, headers={
                                    'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['department']['id'])

    def test_create_department_failed_400(self):
        response = self.client.post('/departments', json={}, headers={
                                    'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_department_failed_500(self):
        response = self.client.post(
            '/departments', json=self.invalid_new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
