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
            'selectDepartment': '1234',
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # test images 

    def test_upload_image_success(self):
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()
        fom_data = {
            'employee_id': '4b1da77d-69ed-4c0e-98f9-df29b83c85d3',
            'image': (file_content, 'test.png')
            }
        response = self.client.post('/files', data=fom_data, content_type='multipart/form-data')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_upload_image_failed_400(self):
        response = self.client.post('/files', data={}, content_type='multipart/form-data')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_upload_image_failed_500(self):
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()
        fom_data = {
            'employee_id': '1234',
            'image': (file_content, 'test.png')
            }
        response = self.client.post('/files', data=fom_data, content_type='multipart/form-data')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_add_department_to_employee_success(self):
        data = {
            'name': 'Information Technology',
            'short_name': 'IT'
        }
        response  = self.clientt.post('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3/department', json=data)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_add_department_to_employee_failed_400(self):
        data = {
            'name': 'Information Technology',
            'short_name': 'IT'
        }
        response  = self.clientt.post('/employees/1234/department', json=data)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # test employees

    def test_get_employees_success(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])
    
    def test_get_employees_failed_404(self):
        response = self.client.get('/employees?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # test departments

    def test_get_departments_success(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])
    
    def test_get_departments_failed_404(self):
        response = self.client.get('/departments?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    # test employees/employee_id/department

    def test_get_employee_department_success(self):
        response = self.client.get('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['department'])
    
    def test_get_employee_department_failed_404(self):
        response = self.client.get('/employees/1234/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # test departemnts/department_id/employees

    def test_get_department_employees_success(self):
        response = self.client.get('/departments/1/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])
    
    def test_get_department_employees_failed_404(self):
        response = self.client.get('/departments/1234/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    # test search employees

    def test_search_employees_success(self):
        response = self.client.get('/employees/search?term=bianca')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])


    
    def test_search_employees_failed_400(self):
        response = self.client.get('/employees/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_search_employees_failed_404(self):
        response = self.client.get('/employees/search?term=123')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # test search departments

    def test_search_departments_success(self):
        response = self.client.get('/departments/search?term=IT')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])
    
    def test_search_departments_failed_400(self):
        response = self.client.get('/departments/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_search_departments_failed_404(self):
        response = self.client.get('/departments/search?term=123')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # test patch employee

    def test_patch_employee_success(self):
        data = {
            'name': 'Bianca',
            'last_name': 'Bianca',
            'email': ''
        }
        response = self.client.patch('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_employee_failed_400(self):
        response =  self.client.patch('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3', data = data, ontent_type='multipart/form-data')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_patch_employee_failed_500(self):
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()
            
        form_data = {
            'age' : '19',
            'selectDepartment': 'wasedfg',
            'image': (file_content, 'test.png')
        }

        response =  self.client.patch('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3', data = form_data, content_type='multipart/form-data')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    #test delete employee/employee_id

    def test_delete_employee_success(self):
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'age': '20',
            'selectDepartment': '/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3',
            'image': (file_content, 'test.png')
        }
        response = self.client.patch('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3', content_type = 'multipart/form-data', data=form_data)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_employee_failed_400(self):
        response = self.client.patch('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_delete_employee_failed_500(self):
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'age': '20',
            'selectDepartment': '123',
            'image': (file_content, 'test.png')
        }
        response = self.client.patch('/employees/4b1da77d-69ed-4c0e-98f9-df29b83c85d3', content_type = 'multipart/form-data', data=form_data)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)














        
