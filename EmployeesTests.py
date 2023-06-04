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
            'selectDepartment': 'a2c84846-ed40-4f0f-9968-52f5d8003e6a',
        }

        self.invalid_new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
        }
        
        self.new_file = {
            'filename': 'imagen.png',
            'employee_id': '1f0565ad-32f2-40e3-9881-172ca97854b9',
        }

        self.invalid_new_file = {
            'filename': 'imagen.png',
            'employee_id': '1234',
        }

        self.change_department = {
            'name': 'Departamento de gente chevere',
            'short_name': 'DGC'
        }

        self.change_employee = {
            'firstname': 'Bi',
            'lastname': 'Agui',
            'age': 17,
            'selectDepartment': 'a2c84846-ed40-4f0f-9968-52f5d8003e6a',
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
        response = self.client.post('/files', json=self.new_file)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_create_file_failed_400(self):
        response = self.client.post('/files', json={
            'filename': 'imagen.png'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # def test_create_file_failed_500(self):
    #     response = self.client.post('/files', json=self.invalid_new_file)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])
    
# PATCH 

    def test_change_department_success(self):
        response = self.client.patch('/departments/9a45ffca-0a93-4c83-88b0-cc5c7d457782', json=self.change_department)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_change_department_error_404(self):
        response = self.client.patch('/employees/9a45ffca-0a93-4c83-88b0-cc5c7d457782', json=self.change_department)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_change_department_error_500(self):
        response = self.client.patch('/departments/non-existent-department', json=self.change_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])                


    
    def test_change_employee_success(self):
        response = self.client.patch('/employees/e8e2aa3e-23e2-4959-a71f-d72de7cd16d6', json=self.change_employee)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_change_employee_error_404(self):
        response = self.client.patch('/employees/321', json=self.change_employee)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


    # def test_change_employee_error_500(self):
    #     response = self.client.patch('/employees/321', json= {})
    #     data = json.loads(response.data)
        
    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)



# DELETE 

    def test_delete_department_success(self):
       response = self.client.delete('/departments/edbc59e8-d86e-4f48-978c-8c7fe8f14e6f')
       data = json.loads(response.data)
       
       self.assertEqual(response.status_code, 200)
       self.assertEqual(data['success'], True)

    def test_delete_department_error_404(self):
        response = self.client.delete('/departments/321')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # def test_delete_department_error_500(self):

    #     response = self.client.delete('/departments/ac5b5692-a211-4bb3-9625-db99dfd26971')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])


    def test_delete_employee_success(self):
       response = self.client.delete('/employees/52c4ea68-3643-4e6b-8fa4-ac51a7064a42')
       data = json.loads(response.data)
       
       self.assertEqual(response.status_code, 200)
       self.assertEqual(data['success'], True)

    def test_delete_employee_error_400(self):
        response = self.client.patch('/employees/321')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # def test_delete_employee_error_500(self):
    #     response = self.client.delete('/employees/ed03633a-32f9-4fc9-a6bc-934d94815f02')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    #GET



    def test_post_employees_department_success(self):
        pass
    def test_patch_employees_department_success(self):
        pass
    def test_delete_employees_department_success(self):
        pass
    def test_get_department_employees_success(self):
        pass
    
    #SEARCH

    def test_search_departments_success(self):
        pass

    def test_search_employees_success(self):
        pass

    def tearDown(self):
        pass

