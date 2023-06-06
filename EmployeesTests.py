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


    # POST - test of department
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
    

    # Testing of /files
    class TestFileUpload(unittest.TestCase):
        def setUp(self):
            with open('static/Testing_Images/...', 'rb') as file:
                self.file_content = file.read()

    def test_upload_file_success(self):
        form_data = {
            'employee_id': '...',
            'image': (io.BytesIO(self.file_content), '...'),
             }

        response = self.client.post('/files', data=form_data, content_type='multipart/form-data')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_upload_file_failed_400(self):
        response = self.client.post('/files', data={}, content_type='multipart/form-data')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_upload_file_failed_500(self):
        form_data = {
            'employee_id': '1234',
            'image': (io.BytesIO(self.file_content), 'test.png'),
        }

        response = self.client.post('/files', data=form_data, content_type='multipart/form-data')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


     # Testing of /employees/<employee_id>/departments
    class TestAddDepartmentToEmployee(unittest.TestCase):
        def test_add_department_to_employee_success(self):
            data = {
            'name': 'FBI',
            'short_name': 'TEC',
            }
            response = self.send_request(data)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response['success'], True)
            self.assertTrue(response['message'])

    def test_add_department_to_employee_failed_400(self):
        data = {
            'name': 'FBI',
        }
        response = self.send_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['success'], False)
        self.assertTrue(response['message'])

    def test_add_department_to_employee_failed_500(self):
        data = {
            'name': 'Agency Employee',
            'short_name': 'TEC', 
        }
        response = self.send_request(data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response['success'], False)
        self.assertTrue(response['message'])

    def send_request(self, data):
        endpoint = '/employees/...'
        content_type = 'multipart/form-data'
        response = self.client.post(endpoint, content_type=content_type, data=data)
        return json.loads(response.data)
        
        
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
   

    # Testing of /employees/search
    def test_search_employees_success(self):
        arguments = {
        'firstname': 'Bianca',
        'lastname': 'Aguinaga',
        'age': 16,
        }
        response = self.client.get('/employees/search', query_string=arguments)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('employees', data)

    def test_search_employees_failed_400(self):
        response = self.client.get('/employees/search')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_search_employees_failed_404(self):
        arguments = {
        'firstname': 'Not name',
        'lastname': 'Not lastname',
        'age': 0
        }
        response = self.client.get('/employees/search', query_string=arguments)
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


    # PATCH - testing of /employees/<employee_id>
    def test_update_employee_success(self):
        with open('static/Testing_Images/testing.png', 'image') as file:
            file_content = file.read()
        form_data = {
        'age': '24',
        'selectDepartment': '21052cd1-957d-41f8-ae73-0a2bda45bd4e',
        'image': (io.BytesIO(file_content), 'testing.png')
        }
        response = self.client.patch('/employees/77f70f49-5166-402a-8842-82d5beb9ba53', data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_update_employee_failed_400(self):
        response = self.client.patch('/employees/77f70f49-5166-402a-8842-82d5beb9ba53', data={}, content_type='multipart/form-data')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_employee_failed_500(self):
        with open('static/testImages/test.png', 'image') as file:
            file_content = file.read()
        form_data = {
        'age': '19',
        'selectDepartment': '1234', 
        'image': (io.BytesIO(file_content), 'testing.png')
        }
        response = self.client.patch('/employees/', data=form_data, content_type='multipart/form-data')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertFalse(data['success'])
        self.assertIn('message', data)


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

    
    # PATCH  - testing of /employees/<employee_id>/departments
    def test_update_employee_department_success(self):
        form_data = {
        'department_id': '58e97761-c362-4d33-a214-fceed4f063b4',
        }
        response = self.client.patch('/employees/8a0c11f6-417a-44c5-ba62-63ceb83ed9b2', json=form_data)
        self.assertEqual(response.status_code, 200)

    def test_update_employee_department_400(self):
        response = self.client.patch('/employees/8a0c11f6-417a-44c5-ba62-63ceb83ed9b2/departments')
        self.assertEqual(response.status_code, 400)

    def test_update_employee_department_404(self):
        form_data = {
        'department_id': '58e97761-c362-4d33-a214-fceed4f063b4',
        }
        response = self.client.patch('/employees/1234/departments', json=form_data)
        self.assertEqual(response.status_code, 404)


     # PATCH  - testing of /employees/<employee_id>
    def test_delete_employee_success(self):
        employee_id = '59131844-cae9-43d1-a714-f3e29472d668'
        response = self.client.delete(f'/employees/{employee_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_employee_failed_400(self):
        employee_id = '59131844-cae9-43d1-a714-f3e29472d668'
        response = self.client.delete(f'/employees/{employee_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_employee_failed_500(self):
        employee_id = '59131844-cae9-43d1-a714-f3e29472d668'
        response = self.client.delete(f'/employees/{employee_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
    
    def tearDown(self):
        pass