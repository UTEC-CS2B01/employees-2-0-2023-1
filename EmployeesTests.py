import unittest
from config.qa import config
from app.models import Employee, Department
from app import create_app
from flask_sqlalchemy import SQLAlchemy
import json
from unittest.mock import patch

class EmployeesTests(unittest.TestCase):

    def setUp(self):
        database_path = config['DATABASE_URI']
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client()

        self.new_department = {
            'name': 'Information Technology',
            'short_name': 'IT',
        }

        self.change_department = {
            'name': 'Human Resources',
            'short_name': 'HR',
        }

        self.new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
            'selectDepartment': 'a8c58ba5-936c-40b6-909f-abd657418436',
        }

        self.change_employee = {
            'firstname': 'Maria',
            'lastname': 'Rojas',
            'age': 35,
            'selectDepartment': 'a8c58ba5-936c-40b6-909f-abd657418436',
        }

        self.invalid_new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
        }
        self.new_file = {
            'employee_id': '6fe0e7b3-9955-4fea-bc88-55f22080d283',
            'image': open(r"C:\Users\Fabrizzio\Downloads\Peter_Castle.jpg", 'rb')
        }
        self.invalid_new_file = {
            'employee_id': '1234',
            'image': open(r"C:\Users\Fabrizzio\Downloads\Peter_Castle.jpg", 'rb')
        }
        self.assign_employee_to_department = {
            'name': 'Marketing',
            'short_name': 'MKT',
        }
        self.invalid_assign_employee_to_department = {
            'name': 'Marketing',
            'short_name': 'abcdefghijklmnopqrstuvwxyz',
        }
        self.update_employee_to_department ={
            'department_id': '420d3c9d-c9dc-4dec-a622-a6a1fec45987',
        }
        self.update_employee = {
            'age': 34,
            'selectDepartment': '698be35a-aff2-4030-93e3-dabc410dfd95',
            'image': open(r"C:\Users\Fabrizzio\Downloads\Peter_Castle.jpg", 'rb')
        }
        self.invalid_update_employee = {
            'age': 'hola',
            'selectDepartment': '698be35a-aff2-4030-93e3-dabc410dfd95',
            'image': open(r"C:\Users\Fabrizzio\Downloads\Peter_Castle.jpg", 'rb')
        }
        self.search_employee = {
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
            'selectDepartment': '1234',
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_file_success(self):
        response = self.client.post('/files', data = self.new_file)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
    
    def test_create_file_failed_400(self):
        response = self.client.post('/files', data = {})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_file_failed_500(self):
        response = self.client.post('/files', data = self.invalid_new_file)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_employees_success(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
    
    def test_get_employees_error_404(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False) # only works if there is no data in the database
    
    def test_get_employees_error_500(self):
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.get('/employees')
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertTrue(data['message'])
    
    def test_patch_department_success(self):
        response = self.client.patch('/departments/a8c58ba5-936c-40b6-909f-abd657418436', json=self.change_department)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_department_error_404(self):
        response = self.client.patch('/departments/nonexistent_id', json=self.change_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_update_department_error_500(self):
        #It does not matter if you use a json form that contains an invalid short name or name, it will never return a 500 error
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.patch('/departments/department_id', json=self.change_department)
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertTrue(data['message'])

    def test_delete_department_success(self):
        response = self.client.delete('/departments/1460b888-0607-45f7-8395-a7e308fbea78')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)  
                
    def test_delete_department_error_404(self):
        response = self.client.delete('/departments/departmento_que_no_existe')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_department_error_500(self):
        #It fails when the department has employees due to foreign key constraint

        response = self.client.delete('/departments/a8c58ba5-936c-40b6-909f-abd657418436')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_assign_employee_to_department_success(self):
        response = self.client.post('/employees/3286046d-d7f7-43c8-85f5-4e75bf05512a/departments', data=self.assign_employee_to_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_assign_employee_to_department_error_404(self):
        response = self.client.post('/employees/nonexistent_id/departments', data=self.assign_employee_to_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_assign_employee_to_department_error_500(self):
        response = self.client.post('/employees/3286046d-d7f7-43c8-85f5-4e75bf05512a/departments', data=self.invalid_assign_employee_to_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_employee_to_department_success(self):
        response = self.client.patch('/employees/3286046d-d7f7-43c8-85f5-4e75bf05512a/departments', data=self.update_employee_to_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])
        
    def test_update_employee_to_department_error_404(self):
        response = self.client.patch('/employees/nonexistent_id/departments', data=self.update_employee_to_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_employee_to_department_error_500(self):
        #It does not matter if you use a json form that contains an invalid short name or name, it will never return a 500 error
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.patch('/employees/3286046d-d7f7-43c8-85f5-4e75bf05512a/departments', json=self.invalid_update_employee_to_department)
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertTrue(data['message'])
    
    def test_delete_employees_by_department_success(self):
        #success case is imposible due to foreign key constraint
        response = self.client.delete('/departments/3286046d-d7f7-43c8-85f5-4e75bf05512a/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_employee_to_department_error_400(self):
        response = self.client.patch('/employees/nonexistent_id/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_employee_to_department_error_500(self):
        response = self.client.delete('/employees/3286046d-d7f7-43c8-85f5-4e75bf05512a/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_update_employee_id(self):
        response = self.client.patch('/employees/92542f45-5d1c-49cc-92e7-06a9b396c3de', data=self.update_employee)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_employee_id_error_404(self):
        response = self.client.patch('/employees/nonexistent_id', data=self.update_employee)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_update_employee_id_error_500(self):
        response = self.client.patch('/employees/92542f45-5d1c-49cc-92e7-06a9b396c3de', data=self.invalid_update_employee)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_get_departments_success(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
    
    def test_get_departments_error_404(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False) # only works if there is no data in the database
    
    def test_get_departments_error_500(self):
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.get('/departments')
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertTrue(data['message'])

    def test_get_employee_department_success(self):
        response = self.client.get('/employees/92542f45-5d1c-49cc-92e7-06a9b396c3de/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_employee_department_error_404(self):
        response = self.client.get('/employees/nonexistent_id/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_get_employee_department_error_500(self):
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.get('/employees/92542f45-5d1c-49cc-92e7-06a9b396c3de/department')
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertEqual(data['success'], False)

    def test_get_departments_by_employee_success(self):
        response = self.client.get('/departments/a8c58ba5-936c-40b6-909f-abd657418436/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_departments_by_employee_error_404(self):
        response = self.client.get('/departments/nonexistent_id/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_get_departments_by_employee_error_500(self):
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.get('/departments/a8c58ba5-936c-40b6-909f-abd657418436/employees')
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertEqual(data['success'], False)

    def test_search_employees_success(self):
        response = self.client.get('/employees/search', query_string={'age': 16})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_search_employees_error_400(self):
        response = self.client.get('/employees/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
    
    def test_search_employees_error_404(self):
        response = self.client.get('/employees/search', query_string={'age': 100})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_search_employees_error_500(self):
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.get('/employees/search', query_string={'age': 16})
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertEqual(data['success'], False)

    def test_search_departments_success(self):
        response = self.client.get('/departments/search', query_string={'name': 'Marketing'})
        data = json.loads(response.data)

        print('data: ', data)
        print('response: ', response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_search_departments_error_400(self):
        response = self.client.get('/departments/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
    
    def test_search_departments_error_404(self):
        response = self.client.get('/departments/search', query_string={'name': 'Ingenieria'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_search_departments_error_500(self):
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.get('/departments/search', query_string={'name': 'Marketing'})
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertEqual(data['success'], False)
    
    def tearDown(self):
        pass
