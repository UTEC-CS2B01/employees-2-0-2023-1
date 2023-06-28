import unittest  # libreria de python para realizar test
from config.qa import config
from app.models import Employee, Department, User
from app.authentication import authorize
from app import create_app
from flask_sqlalchemy import SQLAlchemy
import json
import io as io
import random
import string


def random_username(char_num):
    return ''.join(random.choice(string.ascii_lowercase)
                   for _ in range(char_num))


class EmployeesTests(unittest.TestCase):
    def setUp(self):
        database_path = config['DATABASE_URI']
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client()

        self.new_department = {
            'name': 'DepPrueba',
            'short_name': 'DP'
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

        self.new_authenticated_user = {
            'username': random_username(10),
            'password': '147258369',
            'confirmationPassword': '147258369'
        }

        response_user = self.client.post(
            '/users', json=self.new_authenticated_user)
        data_user = json.loads(response_user.data)
        self.user_valid_token = data_user['token']

    # /departments

    def test_create_department_success(self):
        response = self.client.post('/departments', json=self.new_department, headers={
                                    'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['department']['id'])

    def test_create_department_failed_400(self):
        response = self.client.post('/departments', json={}, headers={
                                    'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_department_failed_500(self):
        response = self.client.post(
            '/departments', json=self.invalid_new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_employee_success(self):
        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']
        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response = self.client.post('/employees', json=self.new_employee, headers={
                                    'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_create_employee_failed_400(self):
        response = self.client.post(
            '/employees', json=self.invalid_new_employee, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
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
        }, headers={
            'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # test of /files

    def test_upload_file_success(self):
        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']
        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response = self.client.post('/employees', json=self.new_employee, headers={
                                    'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)
        emp_tmp_id = data['id']

        # Abre la imagen
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'employee_id': str(emp_tmp_id),
            'image': (io.BytesIO(file_content), 'test.png'),
        }

        response = self.client.post(
            '/files', data=form_data, content_type='multipart/form-data', headers={
                'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_upload_file_failed_400(self):
        response = self.client.post(
            '/files', data={}, content_type='multipart/form-data', headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_upload_file_failed_500(self):
        # Abre la imagen
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'employee_id': '1234',
            'image': (io.BytesIO(file_content), 'test.png'),
        }

        response = self.client.post(
            '/files', data=form_data, content_type='multipart/form-data', headers={
                'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_department_success(self):
        response_temp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_temp = json.loads(response_temp.data)
        id_temp = data_temp['department']['id']

        response = self.client.patch(
            '/departments/{}'.format(id_temp), json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_department_404(self):
        response = self.client.patch('/departments/234567', headers={
            'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_departments_success(self):
        response = self.client.get('/departments', headers={
            'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])

    # /employees

    def test_get_employees_success(self):
        response = self.client.get('/employees', headers={
            'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])

    def test_update_employee_success(self):
        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']

        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response_empl_tmp = self.client.post(
            '/employees', json=self.new_employee, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_empl_tmp = json.loads(response_empl_tmp.data)

        employee_id_tmp = data_empl_tmp['id']

        # Abre la imagen
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'age': '20',
            'selectDepartment': str(dpto_tmp_id),
            # io es una libreria de python para manejar archivos binarios
            'image': (io.BytesIO(file_content), 'test.png')
        }

        response = self.client.patch(
            '/employees/{}'.format(employee_id_tmp), data=form_data, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_employee_failed_400(self):
        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']

        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response_empl_tmp = self.client.post(
            '/employees', json=self.new_employee, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_empl_tmp = json.loads(response_empl_tmp.data)

        employee_id_tmp = data_empl_tmp['id']

        response = self.client.patch(
            '/employees/{}'.format(employee_id_tmp), data={}, content_type='multipart/form-data', headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_employee_failed_500(self):
        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['id']

        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response_empl_tmp = self.client.post(
            '/employees', json=self.new_employee, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_empl_tmp = json.loads(response_empl_tmp.data)

        employee_id_tmp = data_empl_tmp['id']

        # Abre la imagen
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'age': '20',
            'selectDepartment': '1234',  # departamento invalido
            'image': (io.BytesIO(file_content), 'test.png')
        }

        response = self.client.patch(
            '/employees/{}'.format(employee_id_tmp), data=form_data, content_type='multipart/form-data', headers={
                'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_employee_success(self):
        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']

        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response_empl_tmp = self.client.post(
            '/employees', json=self.new_employee, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_empl_tmp = json.loads(response_empl_tmp.data)

        employee_id_tmp = data_empl_tmp['id']

        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'age': '20',
            'selectDepartment': str(dpto_tmp_id),
            'image': (io.BytesIO(file_content), 'test.png')
        }
        response = self.client.patch(
            '/employees/{}'.format(employee_id_tmp), content_type='multipart/form-data', data=form_data, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_employee_failed_400(self):

        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']

        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response_empl_tmp = self.client.post(
            '/employees', json=self.new_employee, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_empl_tmp = json.loads(response_empl_tmp.data)

        employee_id_tmp = data_empl_tmp['id']

        response = self.client.patch('/employees/{}'.format(employee_id_tmp), headers={
            'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_employee_failed_500(self):

        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']

        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response_empl_tmp = self.client.post(
            '/employees', json=self.new_employee, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_empl_tmp = json.loads(response_empl_tmp.data)

        employee_id_tmp = data_empl_tmp['id']

        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'age': '20',
            'selectDepartment': '1234',
            'image': (io.BytesIO(file_content), 'test.png')
        }
        response = self.client.patch(
            '/employees/{}'.format(employee_id_tmp), content_type='multipart/form-data', data=form_data, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_delete_department_success(self):
        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        self.dpto_tmp_id = data_tmp['department']['id']
        response = self.client.delete(
            '/departments/' + str(self.dpto_tmp_id), headers={
                'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_department_404(self):
        response = self.client.delete('/departments/1234', headers={
            'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_department_500(self):

        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']

        response = self.client.delete(
            '/departments/' + str(dpto_tmp_id), headers={
                'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)

        # PARA QUE NO FALLE ( CORREGIR )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # test of /employees/<employee_id>

    def test_delete_employee_success(self):
        response_dpto_tmp = self.client.post(
            '/departments', json=self.new_department, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_tmp = json.loads(response_dpto_tmp.data)
        dpto_tmp_id = data_tmp['department']['id']

        self.new_employee['selectDepartment'] = str(dpto_tmp_id)

        response_empl_tmp = self.client.post(
            '/employees', json=self.new_employee, headers={
                'X-ACCESS-TOKEN': self.user_valid_token})
        data_empl_tmp = json.loads(response_empl_tmp.data)

        employee_id_tmp = data_empl_tmp['id']

        response = self.client.delete('/employees/' + str(employee_id_tmp), headers={
            'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_employee_404(self):
        response = self.client.delete('/employees/1234', headers={
            'X-ACCESS-TOKEN': self.user_valid_token})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        pass
