import unittest
from config.qa import config
from app.models import Employee, Department
from app import create_app
from flask_sqlalchemy import SQLAlchemy
import json

class EmployeesTests(unittest.TestCase):

    def setUp(self):
        database_path = config['DATABASE_URI']
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client()

        self.new_department = {
            'name': 'Information Technology',
            'short_name': 'IT'
        }

        self.invalid_new_department = {
            'name': None,
            'short_name': 'asklcnaslkndlkandlasdnalkdnlasdnlasndlkasndlksandlksandlksandaslknd',
        }

        self.new_employee = {
            'firstname': 'John',
            'lastname': 'Smith',
            'age': 30,
            'selectDepartment': 'f6451aec-e421-482d-b606-7e6932b66f71',
        }

        self.invalid_new_employee = {
            'firstname': 'John',
            'lastname': 'Doe',
            'age': 30,
        }

    # POST
    ###########################################################################################
    # def test_create_department_success(self):
    #     response = self.client.post('/departments', json=self.new_department)
    #     data = json.loads(response.data)
    #     print('data: ', data)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['id'])


    def test_create_department_failed_400(self):
        response = self.client.post('/departments', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_department_failed_500(self):
        response = self.client.post('/departments', json=self.invalid_new_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # def test_create_employee_success(self):
    #     response = self.client.post('/employees', json=self.new_employee)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['id'])


    def test_create_employee_failed_400(self):
        response = self.client.post('/employees', json=self.invalid_new_employee)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    
    def test_create_employee_failed_500(self):
        response = self.client.post('/employees', json={
            'firstname': 'John',
            'lastname': 'Doe',
            'age': 30,
            'selectDepartment': '1234',
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # DELETE
    ###########################################################################################

    def test_delete_employee_success(self):
        response = self.client.delete('/employees/7e97c61c-b9c2-4927-ad9e-7b55364b253b')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_employee_failed_404(self):
        response = self.client.delete('/employees/1234')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # def test_delete_employee_failed_500(self):
    #     response = self.client.delete('/employees', json={
    #         'firstname': 'Bianca',
    #         'lastname': 'Aguinaga',
    #         'age': 16,
    #         'selectDepartment': '1234',
    #     })

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    def test_delete_department_success(self):
        response = self.client.delete('/departments/6ab0bf63-8988-4281-ad6d-ed62e72868a7')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_department_failed_404(self):
        response = self.client.delete('/departments/1234')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # def test_delete_department_failed_500(self):
    #     response = self.client.delete('/departments', json={
    #         'firstname': 'Bianca',
    #         'lastname': 'Aguinaga',
    #         'age': 16,
    #         'selectDepartment': '1234',
    #     })

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])



    def tearDown(self):
        pass
