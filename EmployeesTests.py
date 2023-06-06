import unittest
from config.qa import config
from app.models import Employee, Department, File
from app import create_app,db
from flask_sqlalchemy import SQLAlchemy
import json
import unittest.mock as mock
from unittest.mock import patch 
import os
import io
from werkzeug.datastructures import FileStorage


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
            'selectDepartment': '9976f6a6-3264-47ce-8ae3-bc88ec307a7d',
        }

        self.invalid_new_employee = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
        }


        self.invalid_update_employee_data = {
        'age': '30',
        }

        self.update_employee_data = {
        'age': '30',
        'selectDepartment': 'ade0f796-47a5-4605-b5c5-a886fce50a9f',
        'image': open('/Users/bladimiralferez/Desktop/carvajal.jpeg', 'rb'),
        }

    # POST 

    # test  /departments

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

    # test  /employee

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


    # test  /files

    def test_upload_image_success(self):
            with self.app.app_context():
                with open('/Users/bladimiralferez/Desktop/carvajal.jpeg', 'rb') as img:
                    bytes_img = io.BytesIO(img.read())
                    data = {
                        'employee_id': 'b9824dd1-e331-4a17-8f38-41817d47e619',
                        'image': (bytes_img, 'carvajal.jpeg'),
                    }
                    response = self.client.post('/files', content_type='multipart/form-data', data=data)
                    self.assertEqual(response.status_code, 201)
                    self.assertEqual(response.json['success'], True)

    def test_upload_image_error_400(self):
        response = self.client.post('/files', content_type='multipart/form-data', data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['success'], False)


    @patch('werkzeug.datastructures.FileStorage.save')
    def test_upload_image_error_500(self, mock_save):
        mock_save.side_effect = PermissionError("Permission denied")
        
        with self.app.app_context():
            with open('/Users/bladimiralferez/Desktop/carvajal.jpeg', 'rb') as img:
                bytes_img = io.BytesIO(img.read())
                data = {
                    'employee_id': 'b9824dd1-e331-4a17-8f38-41817d47e619',
                    'image': (bytes_img, 'carvajal.jpeg'),
                }
                response = self.client.post('/files', content_type='multipart/form-data', data=data)
                self.assertEqual(response.status_code, 500)
                self.assertEqual(response.json['success'], False)


    # GET 

    # test  /employees

    def test_get_employees_success(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    @patch('flask_sqlalchemy.BaseQuery.all')
    def test_get_employees_error_500(self, mock_all):
        mock_all.side_effect = Exception("Database Error")
        response = self.client.get('/employees')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    
    # PATCH

    # test /departments/<department_id>

    def test_update_department_success(self):
        existing_department_id = 'fcdfbc3b-9acd-49c0-8db1-0ce9352ffae4'  
        response = self.client.patch(f'/departments/{existing_department_id}', json={
            'name': 'Updated Department',
            'short_name': 'UD',
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Department updated successfully')

    def test_update_department_error_404(self):
        non_existent_department_id = '1234'  
        response = self.client.patch(f'/departments/{non_existent_department_id}', json={
            'name': 'Updated Department',
            'short_name': 'UD',
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    @patch('flask_sqlalchemy.BaseQuery.get')
    def test_update_department_error_500(self, mock_get):
        existing_department_id = 'fcdfbc3b-9acd-49c0-8db1-0ce9352ffae4'  
        mock_get.side_effect = Exception("Database Error")
        response = self.client.patch(f'/departments/{existing_department_id}', json={
            'name': 'Updated Department',
            'short_name': 'UD',
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # DELETE

    # test /departments/<department_id>

    def test_delete_department_success(self):
        existing_department_id = 'fa022ba3-9d69-4356-a012-a8e0737dbf2e'   
        response = self.client.delete(f'/departments/{existing_department_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_department_error_404(self):
        non_existent_department_id = 'fcf339ff-1793-4e02-acd6-e12f604e345' 
        response = self.client.delete(f'/departments/{non_existent_department_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    @patch('app.db.session.commit')
    def test_delete_department_error_500(self, mock_db_commit):
        mock_db_commit.side_effect = Exception("Database Error")
        existing_department_id = 'fa022ba3-9d69-4356-a012-a8e0737dbf2e'  
        response = self.client.delete(f'/departments/{existing_department_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # test /employees/<employee_id>


    def test_delete_employee_success(self):
        existing_employee_id = 'f9642a08-6ec5-4e59-bdab-806420b9b47d'  
        response = self.client.delete(f'/employees/{existing_employee_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_employee_error_404(self):
        non_existent_employee_id = '4b4fcr74-2d1b-4853-9d36-2c0fe9c8f32a'  
        response = self.client.delete(f'/employees/{non_existent_employee_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    @patch('app.db.session.commit')
    def test_delete_employee_error_500(self, mock_db_commit):
        mock_db_commit.side_effect = Exception("Database Error")
        existing_employee_id = 'f9642a08-6ec5-4e59-bdab-806420b9b47d'  
        response = self.client.delete(f'/employees/{existing_employee_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # POST

    # test /employees/<employee_id>/departments
    
    def test_assign_employee_department_success(self):
        existing_employee_id = 'f3e592eb-53b1-4a85-bda8-e99ef5c418ae'  \
        response = self.client.post(f'/employees/{existing_employee_id}/departments', data={'name': 'New Department', 'short_name': 'ND'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['department_id'])
        self.assertEqual(data['message'], 'Department assigned to employee successfully!')

    def test_assign_employee_department_error_404(self):
        non_existent_employee_id = 'fcf909ff-1793-4e02-acd6-e12f604e345'  
        response = self.client.post(f'/employees/{non_existent_employee_id}/departments', data={'name': 'New Department', 'short_name': 'ND'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Employee not found')

    @patch('app.db.session.commit')
    def test_assign_employee_department_error_500(self, mock_db_commit):
        mock_db_commit.side_effect = Exception("Database Error")
        existing_employee_id = 'f3e592eb-53b1-4a85-bda8-e99ef5c418ae'  
        response = self.client.post(f'/employees/{existing_employee_id}/departments', data={'name': 'New Department', 'short_name': 'ND'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Error assigning department to employee')

    # PATCH

    # test /employees/<employee_id>/departments

    def test_update_employee_departments_success(self):
        existing_employee_id = 'f086540a-a9eb-4e36-a499-33a753c3db9b'   
        existing_department_id = '0a0181ff-9d98-41c5-a83f-5e53ced8e9a1'  
        response = self.client.patch(f'/employees/{existing_employee_id}/departments', data={'department_id': existing_department_id})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Employee departments updated successfully!')

    def test_update_employee_departments_error_404_employee(self):
        non_existent_employee_id = 'f7b132bd-ofb7-47f9-8db9-5a5b1da82697'  
        existing_department_id = '0a0181ff-9d98-41c5-a83f-5e53ced8e9a1' 
        response = self.client.patch(f'/employees/{non_existent_employee_id}/departments', data={'department_id': existing_department_id})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Employee not found')

    def test_update_employee_departments_error_400_no_department_id(self):
        existing_employee_id = 'f086540a-a9eb-4e36-a499-33a753c3db9b'  
        response = self.client.patch(f'/employees/{existing_employee_id}/departments', data={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Department ID is required')
    
    def test_update_employee_departments_error_404_department(self):
        existing_employee_id = 'f086540a-a9eb-4e36-a499-33a753c3db9b'  
        non_existent_department_id = '0a0181ff-9d58-41c5-a83f-5e53ced8e9a1'  
        response = self.client.patch(f'/employees/{existing_employee_id}/departments', data={'department_id': non_existent_department_id})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Department not found')

    @patch('app.db.session.commit')
    def test_update_employee_departments_error_500(self, mock_db_commit):
        mock_db_commit.side_effect = Exception("Database Error")
        existing_employee_id = 'f086540a-a9eb-4e36-a499-33a753c3db9b'  
        existing_department_id = '0a0181ff-9d98-41c5-a83f-5e53ced8e9a1'   
        response = self.client.patch(f'/employees/{existing_employee_id}/departments', data={'department_id': existing_department_id})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Error updating employee departments')


    # DELETE

    # test /employees/<employee_id>/departments
    

    def test_remove_employee_departments_success(self):
        existing_employee_id = 'c29e9331-f125-47ec-9c81-e2a08e9f8671'  
        response = self.client.delete(f'/employees/{existing_employee_id}/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_remove_employee_departments_error_404(self):
        non_existent_employee_id = 'ebb4k456-9775-451f-bb27-81b5a87be85f' 
        response = self.client.delete(f'/employees/{non_existent_employee_id}/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    @patch('app.db.session.commit')
    def test_remove_employee_departments_error_500(self, mock_db_commit):
        mock_db_commit.side_effect = Exception("Database Error")
        existing_employee_id = 'c29e9331-f125-47ec-9c81-e2a08e9f8671'   
        response = self.client.delete(f'/employees/{existing_employee_id}/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    
    # PATCH
    # test /employees/<employee_id>

    def test_update_employee_success(self):
        employee_id = '6a117ac6-1b36-459d-8026-847857b73114'
        response = self.client.patch(f'/employees/{employee_id}', data=self.update_employee_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Employee updated successfully!')

    def test_update_employee_error_400(self):
        employee_id = '6a117ac6-1b36-459d-8026-847857b73114'
        response = self.client.patch(f'/employees/{employee_id}', data=self.invalid_update_employee_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_employee_error_500(self):
        employee_id = '6a117ac6-1b36-459d-8026-847857b73114'
        with self.assertRaises(Exception):
            response = self.client.patch(f'/employees/{employee_id}', data=self.update_employee_data)
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 500)
            self.assertTrue(data['message'])
    

    # GET
    # test /departments

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
        self.assertEqual(data['success'], False) 

    def test_get_departments_error_500(self):
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.get('/departments')
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertTrue(data['message'])

    
    # test /employees/<employee_id>/department

    def test_get_employee_departments_success(self):
        response = self.client.get('/employees/62bc4d79-b1dc-4fb9-9ba0-6353044958e1/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_employee_departments_error_404(self):
        response = self.client.get('/employees/62bc4d79-b1dc-4fb9-9ba0-6353044958e1/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_employee_departments_error_500(self):
        with self.app.test_client():
            with self.assertRaises(Exception):
                response = self.app.get('/employees/62bc4d79-b1dc-4fb9-9ba0-6353044958e1/department')
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 500)
                self.assertEqual(data['success'], False)
    
    
    # test /departments/<department_id>/employees

    def test_get_department_employees_success(self):
        response = self.client.get('/departments/9976f6a6-3264-47ce-8ae3-bc88ec307a7demployees')  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_department_employees_error_404_no_department(self):
        response = self.client.get('/departments/1234/employees')  
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_department_employees_error_404_no_employees(self):
        response = self.client.get('/departments/22d4bf6d-fc84-4281-ad7b-75d935a41027/employees')  

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_department_employees_error_500(self):
        with mock.patch('sqlalchemy.orm.Query.all', side_effect=Exception):
            response = self.client.get('/departments/22d4bf6d-fc84-4281-ad7b-75d935a41027/employees')  
            data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        
    # test /employees/search

    def test_search_employees_success(self):
        response = self.client.get('/employees/search', query_string={'firstname': 'Pedro', 'lastname': 'Perez'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_employees_error_404(self):
        response = self.client.get('/employees/search', query_string={'firstname': 'No', 'lastname': 'No'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_employees_error_500(self):
        with mock.patch('sqlalchemy.orm.Query.all', side_effect=Exception):
            response = self.client.get('/employees/search', query_string={'firstname': 'Pedro', 'lastname': 'Perez'})
            data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)


    def test_search_departments_success(self):
        response = self.client.get('/departments/search', query_string={'name': 'Information Technology'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_departments_error_400(self):
        response = self.client.get('/departments/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_search_departments_error_404(self):
        response = self.client.get('/departments/search', query_string={'name': 'Hola'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_departments_error_500(self):
        with mock.patch('sqlalchemy.orm.Query.all', side_effect=Exception):
            response = self.client.get('/departments/search', query_string={'name': 'Information Technology'})
            data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        pass

    
