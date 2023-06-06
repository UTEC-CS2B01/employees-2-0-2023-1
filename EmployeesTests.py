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
            'selectDepartment': '093c3f30-3854-416a-82ee-9ba5474ea64a',
        }

        self.invalid_new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
        }

        self.delete_department = {  
            'id': '08b442b9-0cd7-4197-b540-04b1156a5d17'
        }

        self.delete_not_found_department = {
            'id': '1234'
        }

        self.delete_employee = {  
            'id': '85c1fd57-b58b-403d-9e1f-c6c148072eec'
        }

        self.delete_not_found_employee = {
            'id': '1234'
        }

        self.update_department_s = {
            'id': '0cecb8c3-9b7c-4fab-9915-70f9ad90bcf1',
            'name': 'Cleaning Department', 
            'short_name': 'CD'
        }

        self.update_employee_s = {
            'id': 'a188896c-a9a7-4a38-885a-8034fcc0aca2',
            'is_active': False,
            'selectDepartment': '11fd9866-6cf3-4b33-b53e-d84482b3a432'
        }

        self.update_department_500 = {
            'id' : '0cecb8c3-9b7c-4fab-9915-70f9ad90bcf1',
            'name' : 'asdasdfsdafasjkhksdjfhajfhkadjfhakjdhfakjshdalksdjlckashndlashdklasdlak',
            'short_name': 'Caosjbijsdfnaijdfnk<jdfvkjdzsbldvkjzdjkbvzsjkdfbdsjkfbsdkjfbsdkfbsdkfsdkfsdjbfsdjf'
        }

        self.update_employee_500 = {
            'id': 'a188896c-a9a7-4a38-885a-8034fcc0aca2',
            'firstname': 'Marvin',
            'lastname': 'Abisrror',
            'is_active': False,
            'selectDepartment': '1234',
        }


    # Test Create Department
    ###########################################################################################

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

    # Test Create Employee
    ###########################################################################################

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

    # Test Delete Department
    ###########################################################################################

    def test_delete_department_success(self):
        response = self.client.delete('departments/{}'.format(self.delete_department['id']), json=self.delete_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_delete_department_failed_404(self):
        response = self.client.delete('departments/{}'.format(self.delete_not_found_department['id']), json=self.delete_not_found_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test Delete Employee
    ###########################################################################################

    def test_delete_employee_success(self):
        response = self.client.delete('employees/{}'.format(self.delete_employee['id']), json=self.delete_employee)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_delete_employee_failed_404(self):
        response = self.client.delete('employees/{}'.format(self.delete_not_found_employee['id']), json=self.delete_not_found_employee)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test Update Employee
    ###########################################################################################

    def test_update_employee_success(self):
        response = self.client.patch('employees/{}'.format(self.update_employee_s['id']), json=self.update_employee_s)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_update_employee_failed_404(self):
        response = self.client.patch('employees/{}'.format(self.delete_not_found_employee['id']), json=self.delete_not_found_employee)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_employee_failed_500(self):
        response = self.client.patch('employees/{}'.format(self.update_employee_500['id']), json=self.update_employee_500)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test Update Department
    ###########################################################################################

    def test_update_department_success(self):
        response = self.client.patch('departments/{}'.format(self.update_department_s['id']), json=self.update_department_s)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_update_department_failed_404(self):
        response = self.client.patch('departments/{}'.format(self.delete_not_found_department['id']), json=self.delete_not_found_department)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])    

    def test_update_department_failed_500(self):
        response = self.client.patch('departments/{}'.format(self.update_department_500['id']),json = self.update_department_500)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test Get Employees
    ###########################################################################################

    def test_get_employees_success(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
        
    # Test Get Departments
    ###########################################################################################

    def test_get_departments_success(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])


    def tearDown(self):
        pass