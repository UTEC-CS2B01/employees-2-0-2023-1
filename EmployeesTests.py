import unittest #libreria de python para realizar test
from config.qa import config 
from app.models import Employee, Department 
from app import create_app 
from flask_sqlalchemy import SQLAlchemy 
import json
import io as io


class EmployeesTests(unittest.TestCase):
#el test se corre con el comando python -m unittest "EmployeesTests.py"
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
            'selectDepartment': 'c8d29a66-f718-45fe-9a4c-d70013d7fdc6',
        }

        self.invalid_new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
        }


    # test of /departments

    def test_create_department_success(self):
        response = self.client.post('/departments', json=self.new_department)
        data = json.loads(response.data)


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


    # test of /employees

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


    # test of /files

    def test_upload_file_success(self):
        # Abre la imagen
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'employee_id': '508ec843-213b-47ec-9052-46154d4007c2',
            'image': (io.BytesIO(file_content), 'test.png'),
        }

        response = self.client.post('/files', data=form_data, content_type='multipart/form-data')

        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])





    # test of /employees/<employee_id>

    def test_update_employee_success(self):
        # Abre la imagen
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()


        form_data = {
            'age': '20',
            'selectDepartment': '7cf0cb5d-c255-4bd2-b98f-23aae79952cf',
            'image': (io.BytesIO(file_content), 'test.png') #io es una libreria de python para manejar archivos binarios
        }


        response = self.client.patch('/employees/508ec843-213b-47ec-9052-46154d4007c2', data=form_data)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


    def test_update_employee_failed_400(self):
        response = self.client.patch('/employees/508ec843-213b-47ec-9052-46154d4007c2', data={}, content_type='multipart/form-data')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    def test_update_employee_failed_500(self):
        # Abre la imagen
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()


        form_data = {
            'age': '20',
            'selectDepartment': '1234', #departamento invalido
            'image': (io.BytesIO(file_content), 'test.png')
        }

        response = self.client.patch('/employees/508ec843-213b-47ec-9052-46154d4007c2', data=form_data, content_type='multipart/form-data')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # test of /employees/<employee_id>

    def tearDown(self):
        pass



    #test para la ruta 1