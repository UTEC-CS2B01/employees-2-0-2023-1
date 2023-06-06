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

        self.new_file = {
            'employee_id': '4b1da77d-69ed-4c0e-98f9-df29b83c85d3',
            'filename': 'test.jpg'
        }
        
        self.invalid_new_file = {
            'employee_id': '4b1da77d-69ed-4c0e-98f9-df29b83c85d3',
            'filename': 'test.txt'
        }

        self.new_department_employee = {
            'name': 'Test Department',
            'short_name': 'TD',
        }

        self.invalid_new_department_employee = {
            'name': None,
            'short_name': 'asklcnaslkndlkandlasdnalkdnlasdnlasndlkasndlksandlksandlksandaslknd',
        }

    #POST METHODS TEST 

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
            'selectDepartment': '1234',
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_file_success(self):
        response = self.client.post('/files', json=self.new_file)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_create_file_failed_400(self):
        response=self.client.post('/files', json=self.invalid_new_file)
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_file_failed_500(self):
        response=self.client.post('/files', json={
            'employee_id': '1234',
            'filename': 'test.jpg'
        })
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_departament_for_employee_success(self):
        response=self.client.post('/employees/4b1da77d-69ed-4c0e-5385-df29b83c85d3/departments', json=self.new_department_employee)
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['department_id'])
        self.assertTrue(data['employee_id'])

    def test_create_departament_for_employee_failed_400(self):
        response=self.client.post('/employees/4b1da77d-69ed-4c0e-5385-df29b83c85d3/departments', json=self.invalid_new_department_employee)
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_departament_for_employee_failed_500(self):
        response=self.client.post('/employees/1234/departments', json=self.new_department_employee)
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    #GET METHODS TEST

    def test_get_employees_success(self):
        response=self.client.get('/employees')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])
    
    def test_get_employees_failed_404(self):
        response=self.client.get('/employees?search=1234')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_departments_success(self):
        response=self.client.get('/departments')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])
    
    def test_get_departments_failed_404(self):
        response = self.client.get('/departments?search=nonexistent')        
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_departments_failed_500(self):
        response = self.client.get('/departments?search=1234')        
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_employee_departament_success(self):
        response=self.client.get('/employees/4b1da77d-69ed-4c0e-5385-df29b83c85d3/department')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])

    def test_get_employee_departament_failed_404(self):
        response=self.client.get('/employees/1234/department')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_employee_departament_failed_500(self):
        response=self.client.get('/employees/1234/department')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_departament_employees_success(self):
        response=self.client.get('/departments/4b1da77d-69ed-4c0e-98f9-df29b83c85d3/employees')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])
    
    def test_get_departament_employees_failed_404(self):
        response=self.client.get('/departments/1234/employees')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_departament_employees_failed_500(self):
        response=self.client.get('/departments/1234/employees')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_search_employees_success(self):
        response=self.client.get('/employees?search=Bianca')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])
    
    def test_get_search_employees_failed_404(self):
        response=self.client.get('/employees?search=')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_search_employees_failed_500(self):
        response=self.client.get('/employees?search=1234')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_search_departments_success(self):
        response=self.client.get('/departments?search=Information')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])

    def test_get_search_departments_failed_404(self):
        response=self.client.get('/departments?search=')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_search_departments_failed_500(self):
        response=self.client.get('/departments?search=1234')
        data=json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def tearDown(self):
        pass
