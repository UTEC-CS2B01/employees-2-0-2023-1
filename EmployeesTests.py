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
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
            'selectDepartment': '4b1da77d-69ed-4c0e-98f9-df29b83c85d3',
        }

        self.invalid_new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
        }

    def test_create_department_success(self):
        response = self.client.post('/departments', json=self.new_department)
        data = json.loads(response.data)
        print('data: ', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

        
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


    def test_create_employee_success(self):
        response = self.client.post('/employees', json=self.new_employee)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])


    def test_create_employee_failed_400(self):
        response = self.client.post('/employees', json=self.invalid_new_employee)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    
    def test_create_employee_failed_500(self):
        response = self.client.post('/employees', json={
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
            'selectDepartment': '1',
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_departments_success(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])


    def test_get_departments_failed_404(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    def test_get_employees_success(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])


    def test_get_employees_failed_404(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    def test_update_department_success(self):
        response = self.client.patch('/departments/364388e8-c09e-4359-8be8-cbee1ad76f83', json={
            'name': 'Information Technology',
            'short_name': 'IITT'
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])


    def test_update_department_failed_404(self):
        response = self.client.patch('/departments/1234', json={
            'name': 'Information Technology',
            'short_name': 'IT'
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_update_department_failed_500(self):
        response = self.client.patch('/departments/4b1da77d-69ed-4c0e-98f9-df29b83c85d3', json={
            'name': None,
            'short_name': 'IITT'
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_employee_success(self):
        response = self.client.patch('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3', json={
            'firstname': 'Aldo',
            'lastname': 'Cucho',
            'age': 17,
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_update_employee_failed_404(self):
        response = self.client.patch('/employees/1234', json={
            'firstname': 'Aldo',
            'lastname': 'Cucho',
            'age': 17,
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_employee_failed_500(self):
        response = self.client.patch('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3', json={
            'firstname': 'Aldo',
            'lastname': 'Cucho',
            'age': None,
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_department_success(self):
        response = self.client.delete('/departments/364388e8-c09e-4359-8be8-cbee1ad76f83')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_delete_department_failed_404(self):
        response = self.client.delete('/departments/1234')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_employee_success(self):
        response = self.client.delete('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_delete_employee_failed_404(self):
        response = self.client.delete('/employees/1234')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def tearDown(self):
        pass
