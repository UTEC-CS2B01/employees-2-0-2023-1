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

##GETS:
    def test_get_departments(self):
        res = self.client().get('/departments')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])
        self.assertTrue(len(data['departments']) > 0)

    def test_get_department_by_id(self):
        department = Department(name='IT', short_name='IT')
        department.insert()

        res = self.client().get(f'/departments/{department.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['department']['name'], 'IT')
        self.assertEqual(data['department']['short_name'], 'IT')

    def test_get_department_not_found(self):
        res = self.client().get('/departments/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Department not found')

    def test_get_employees(self):
        res = self.client().get('/employees')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])
        self.assertTrue(len(data['employees']) > 0)

    def test_get_employee_by_id(self):
        employee = Employee(firstname='Pepito', lastname='Perales', age=30, department_id=1)
        employee.insert()

        res = self.client().get(f'/employees/{employee.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['employee']['firstname'], 'Pepito')
        self.assertEqual(data['employee']['lastname'], 'Perales')
        self.assertEqual(data['employee']['age'], 30)
        self.assertEqual(data['employee']['department_id'], 1)

    def test_get_employee_not_found(self):
        res = self.client().get('/employees/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Employee not found')

    def test_get_departments_error(self):
        res = self.client().get('/departments/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid endpoint')

    def test_get_employees_error(self):
        res = self.client().get('/employees/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid endpoint')

    def test_get_departments_internal_server_error(self):
        def mock_get_departments():
            raise Exception('Something went wrong')

        self.app.get_departments = mock_get_departments

        res = self.client().get('/departments')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')

    def test_get_employees_internal_server_error(self):
        def mock_get_employees():
            raise Exception('Something went wrong')
        self.app.get_employees = mock_get_employees

        res = self.client().get('/employees')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')

##PATCH:
    def test_patch_department(self):
        department = Department(name='IT', short_name='IT')
        department.insert()

        res = self.client().patch(f'/departments/{department.id}', json={'name': 'HR'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['department']['name'], 'HR')
        self.assertEqual(data['department']['short_name'], 'IT')

    def test_patch_department_not_found(self):
        res = self.client().patch('/departments/1000', json={'name': 'HR'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Department not found')

    def test_patch_department_invalid_fields(self):
        department = Department(name='IT', short_name='IT')
        department.insert()

        res = self.client().patch(f'/departments/{department.id}', json={'invalid_field': 'Invalid'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid fields')

    def test_patch_employee(self):
        employee = Employee(firstname='Pepito', lastname='Perales', age=30, department_id=1)
        employee.insert()

        res = self.client().patch(f'/employees/{employee.id}', json={'age': 35})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['employee']['age'], 35)

    def test_patch_employee_not_found(self):
        res = self.client().patch('/employees/1000', json={'age': 35})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Employee not found')

    def test_patch_employee_invalid_fields(self):
        employee = Employee(firstname='Pepito', lastname='Perales', age=30, department_id=1)
        employee.insert()

        res = self.client().patch(f'/employees/{employee.id}', json={'invalid_field': 'Invalid'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid fields')

    def test_patch_department_internal_server_error(self):
        def mock_patch_department(department_id, data):
            raise Exception('Something went wrong')
        self.app.patch_department = mock_patch_department

        department = Department(name='IT', short_name='IT')
        department.insert()

        res = self.client().patch(f'/departments/{department.id}', json={'name': 'HR'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')

    def test_patch_employee_internal_server_error(self):
        def mock_patch_employee(employee_id, data):
            raise Exception('Something went wrong')
        self.app.patch_employee = mock_patch_employee

        employee = Employee(firstname='Pepito', lastname='Perales', age=30, department_id=1)
        employee.insert()

        res = self.client().patch(f'/employees/{employee.id}', json={'age': 35})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')

##DELETE:
    def test_delete_department(self):
        department = Department(name='IT', short_name='IT')
        department.insert()

        res = self.client().delete(f'/departments/{department.id}')
        data = json.loads(res.data)

        deleted_department = Department.query.get(department.id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Department deleted successfully')
        self.assertEqual(deleted_department, None)

    def test_delete_department_not_found(self):
        res = self.client().delete('/departments/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Department not found')

    def test_delete_employee(self):
        employee = Employee(firstname='Pepito', lastname='Perales', age=30, department_id=1)
        employee.insert()

        res = self.client().delete(f'/employees/{employee.id}')
        data = json.loads(res.data)

        deleted_employee = Employee.query.get(employee.id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Employee deleted successfully')
        self.assertEqual(deleted_employee, None)

    def test_delete_employee_not_found(self):
        res = self.client().delete('/employees/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Employee not found')

    def tearDown(self):
        pass
