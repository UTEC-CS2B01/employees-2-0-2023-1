import unittest
from config.qa import config
from app.models import Employee, Department
from app import create_app
from flask_sqlalchemy import SQLAlchemy
import json
import io

class EmployeesTests(unittest.TestCase):

    # POST - test of employees

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

        # POST - test of department

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

        
    # GET - testing of employees
    def test_get_employees_success(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('data',data)

    def test_get_employees_failed_404(self):
        search_query = '*'
        response = self.client.get(f'/employees?search={search_query}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])


     # GET - testing of departments
    def test_get_departments_success(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('data', data)

    def test_get_departments_failed_404(self):
        search_query = 'centraldepartament/*'
        response = self.client.get(f'/departments?search={search_query}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
    

    # Testing of /employees/<employee_id>/department
    def test_get_employee_department_success(self):
        employee_id = '...'
        response = self.client.get(f'/employees/{employee_id}/department')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('department', data)
        self.assertIn('employee', data)

    def test_get_employee_department_failed_404(self):
        employee_id = '1234'
        response = self.client.get(f'/employees/{employee_id}/department')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    
    # Testing of /departments/<department_id>/employees
    def test_get_department_employees_success(self):
        department_id = '...'
        response = self.client.get(f'/departments/{department_id}/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('employees', data)

    def test_get_department_employees_failed_404(self):
        department_id = '1234'
        response = self.client.get(f'/departments/{department_id}/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
   
    # Testing of /departments/search
    def test_search_departments_success(self):
        arguments = {
        'short_name': 'UTEC',
        }
        response = self.client.get('/departments/search', query_string=arguments)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('departments', data)

    def test_search_departments_failed_400(self):
        response = self.client.get('/departments/search')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_search_departments_failed_404(self):
        arguments = {
        'short_name': 'Not departament',
        }
        response = self.client.get('/departments/search', query_string=arguments)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])


   
    # PATCH - testing of /departments/<department_id>
    def test_update_department_success(self):
        department_id = '59131844-cae9-43d1-a714-f3e29472d668'
        form_data = {'name': 'BCRP'}
        response = self.client.patch(f'/departments/{department_id}', content_type='multipart/form-data', data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_update_department_404(self):
        department_id = '23452'
        response = self.client.patch(f'/departments/{department_id}')
        self.assertEqual(response.status_code, 404)


    def tearDown(self):
        pass