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

        self.assign_employee_department = {
            'name': 'Marketing',
            'short_name': 'MT',
        }

        self.invalid_assign_employee_department = {
            'name': 'Marketing',
            'short_name': '',
        }
        self.update_employee_department ={
            'department_id': '87fd2288-4dd9-4901-bfa8-e31d3407090a',
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

    # def test_create_file_success(self):
    #     response = self.client.post('/files', json=self.new_file)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['id'])

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
        response = self.client.patch('/departments/ad216f8a-f196-4173-85d1-2707a9f3deed', json=self.change_department)
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
        response = self.client.patch('/departments/321', json=self.change_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])                


    
    def test_change_employee_success(self):
        response = self.client.patch('/employees/d806e1fa-7f6d-4fcf-8b5e-18249bc3524b', json=self.change_employee)
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
        response = self.client.delete('/departments/32159')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # def test_delete_department_error_500(self):

    #     response = self.client.delete('/departments/edbc59e8-d86e-4f48-978c-8c7fe8f14e6f')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])


    def test_delete_employee_success(self):
       response = self.client.delete('/employees/028c77a0-eefa-49d0-baa5-c71e426f008e')
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

    def test_get_departments_success(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
    



#employees_department #POST

    def test_post_employees_department_success(self):
        response = self.client.post('/employees/081fd298-78e3-40b0-ac6a-ee2cd2ac7eed/departments', data=self.assign_employee_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_post_employee_department_error_404(self):
        response = self.client.post('/employees/321/departments', data=self.assign_employee_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_post_employee_department_error_500(self):
        response = self.client.post('/employees/081fd298-78e3-40b0-ac6a-ee2cd2ac7eed/departments', data=self.invalid_assign_employee_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

#employees_department #PATCH

    def test_patch_employees_department_success(self):
        response = self.client.patch('/employees/e4261db0-2952-49c0-88ff-08e0998fc3e1/departments', data=self.update_employee_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_patch_employee_department_error_404(self):
        response = self.client.patch('/employees/321/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_patch_employee_department_error_500(self):
        pass
  

#employees_department #DELETE

    # def test_delete_employees_department_success(self):
    #     response = self.client.delete('/employees/d806e1fa-7f6d-4fcf-8b5e-18249bc3524b/departments')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    def test_delete_employee_to_department_error_400(self):
        response = self.client.delete('/employees/321/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # def test_delete_employee_to_department_error_500(self):
    #     response = self.client.delete('/employees/d806e1fa-7f6d-4fcf-8b5e8249bc3524b/departments')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    #department_employee #GET

    def test_get_department_employees_success(self):
        response = self.client.get('/employees/081fd298-78e3-40b0-ac6a-ee2cd2ac7eed/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)    
    
    #SEARCH

    def test_search_departments_success(self):
        response = self.client.get('/departments/search', query_string={'name': 'Information Technology'})
        data = json.loads(response.data)

        print('data: ', data)
        print('response: ', response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_employees_success(self):
        response = self.client.get('/employees/search', query_string={'age': 16})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def tearDown(self):
        pass

