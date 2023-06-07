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
            'firstname': 'John',
            'lastname': 'Smith',
            'age': 30,
            'selectDepartment': 'f6451aec-e421-482d-b606-7e6932b66f71',
        }

        self.invalid_new_employee = {
            'firstname': 'John',
            'lastname': 'Doe',
            'age': 30,
        }

    # POST
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
            'firstname': 'John',
            'lastname': 'Doe',
            'age': 30,
            'selectDepartment': '1234',
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_department_from_employee_success(self):
        response = self.client.post('/employees/9c969220-3338-421d-9e0d-0b0e9b4fb474/departments',
                                    json={
                                        "name": "Servicio",
                                        "short_name": "ss"})
        data = json.loads(response.data)
        print('data: ', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_create_department_from_employee_failed_404(self):
        response = self.client.post('/employees/1234/departments', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_department_from_employee_failed_400(self):
        response = self.client.post('/employees/39c6d33f-62ff-4740-b712-aedc4f98f7e2/departments',
                                    json={
                                        "short_name": "ss"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # def test_create_department_from_employee_failed_500(self):
    #     response = self.client.post('/departments', json=self.invalid_new_department)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    def test_create_image_success(self):
        response = self.client.post('/files',
                                    data={"image": (open("james_bond.jpg", "rb"),
                                                    "james_bond.jpg"),
                                          'employee_id': '64aa2f9a-2eb9-4b2e-8c2f-d17c84ed04ae',
                                          })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['success'], True)

    def test_create_image_failed_400(self):
        response = self.client.post('/files', json={
            'employee_id': 'e02268b7-9a5d-47c1-87fa-a92c6451cb61',
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_image_failed_500(self):
        response = self.client.post('/files',
                                    data={"image": (open("james_bond.jpg", "rb"),
                                                    "james_bond.jpg"),
                                          'employee_id': '1234',
                                          })

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['success'], False)

    # GET
    ###########################################################################################

    def test_get_department_success(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_department_failed_404(self):
        response = self.client.get('/departments?search=nothing_at_all')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # def test_get_department_failed_500(self):
    #     response = self.client.get('/departments/')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    def test_get_employee_success(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_employee_failed_404(self):
        response = self.client.get('/employees?search=nothing_at_all')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # def test_get_employee_failed_500(self):
    #     response = self.client.get('/employees/')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    def test_get_department_from_employee_success(self):
        response = self.client.post('/departments', json=self.new_department)
        data_department = json.loads(response.data)
        department_id = data_department['id']

        response = self.client.post('/employees', json={
            'firstname': 'Rick',
            'lastname': 'Blaine',
            'age': 42,
            'selectDepartment': department_id
        })

        data_employee = json.loads(response.data)
        employee_id = data_employee['id']

        response = self.client.get('/employees/' + employee_id + "/departments")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_department_from_employee_failed_404(self):
        response = self.client.post('/departments', json=self.new_department)
        data_department = json.loads(response.data)
        department_id = data_department['id']

        response = self.client.get("/employees/1234/departments",
                                    json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_department_from_employee_failed_500(self):
        response = self.client.patch('/employees/9d0d68a7-979e-4c95-98d0-863964555250/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # DELETE
    ###########################################################################################

    def test_delete_employee_success(self):
        response = self.client.post('/employees', json=self.new_employee)
        data = json.loads(response.data)
        employee_id = data["id"]

        path = '/employees/' + employee_id
        response = self.client.delete(path)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_employee_failed_404(self):
        response = self.client.delete('/employees/1234')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # def test_delete_employee_failed_500(self):
    #     response = self.client.delete('/employees', json={
    #         'firstname': 'Bianca',
    #         'lastname': 'Aguinaga',
    #         'age': 16,
    #         'selectDepartment': '1234',
    #     })

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    def test_delete_department_success(self):
        response = self.client.delete('/departments/6ab0bf63-8988-4281-ad6d-ed62e72868a7')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_department_failed_404(self):
        response = self.client.delete('/departments/1234')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # def test_delete_department_failed_500(self):
    #     response = self.client.delete('/departments', json={
    #         'firstname': 'Bianca',
    #         'lastname': 'Aguinaga',
    #         'age': 16,
    #         'selectDepartment': '1234',
    #     })

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    # PATCH
    ###########################################################################################

    def test_change_department_success(self):
        response = self.client.patch('/departments/0d625df7-e618-4057-bc17-849a7f155f1d', json={
            'name': 'Intelligence and development',
            'short_name': 'I+D',
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_change_department_failed_404(self):
        response = self.client.patch('/departments/1234', json={
            'short_name': 'I+D',
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    def test_change_department_failed_500(self):
        response = self.client.patch('/departments/b25b36e2-90b7-4cca-b04b-fb4e77ad1048', json={
            'name': 'Human resources',
            'short_name': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_change_employee_success(self):
        response = self.client.patch('/employees/64aa2f9a-2eb9-4b2e-8c2f-d17c84ed04ae', json={
            'firstname': 'James',
            'lastname': 'Bond',
            'age': 25,
        })
        data = json.loads(response.data)
        print("\n\n\n\n\n\n", data["message"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_change_employee_failed_404(self):
        response = self.client.patch('/employees/1234', json={
            'firstname': 'James',
            'lastname': 'Bond',
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # def test_change_employee_failed_500(self):
    #     response = self.client.patch('/employees/b25b36e2-90b7-4cca-b04b-fb4e77ad1048', json={
    #         'firstname': 'James',
    #         'lastname': 'Bond',
    #         'age': 'ssfas25',
    #     })

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    def test_change_department_from_employee_success(self):
        response = self.client.post('/departments', json=self.new_department)
        data_department = json.loads(response.data)
        department_id = data_department['id']

        response = self.client.post('/employees', json=self.new_employee)
        data_employee = json.loads(response.data)
        employee_id = data_employee['id']

        response = self.client.patch('/employees/' + employee_id + "/departments",
                                    json={
                                        "department_id": department_id})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_change_department_from_employee_failed_404(self):
        response = self.client.post('/departments', json=self.new_department)
        data_department = json.loads(response.data)
        department_id = data_department['id']

        response = self.client.patch("/employees/1234/departments",
                                    json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_change_department_from_employee_failed_500(self):
        response = self.client.patch('/employees/9d0d68a7-979e-4c95-98d0-863964555250/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # This test will fail bacause it leaves the employee without departmen_id
    # def test_delete_department_from_employee_success(self):
    #     response = self.client.post('/departments', json=self.new_department)
    #     data_department = json.loads(response.data)
    #     department_id = data_department['id']

    #     response = self.client.post('/employees', json={
    #         'firstname': 'John',
    #         'lastname': 'Doe',
    #         'age': 27,
    #         'selectDepartment': department_id
    #     })
    #     data_employee = json.loads(response.data)
    #     employee_id = data_employee['id']

    #     response = self.client.delete('/employees/' + employee_id + "/departments")
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    def test_delete_department_from_employee_failed_404(self):
        response = self.client.post('/departments', json=self.new_department)
        data_department = json.loads(response.data)
        department_id = data_department['id']

        response = self.client.delete("/employees/1234/departments",
                                    json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_department_from_employee_failed_500(self):
        response = self.client.patch('/employees/9d0d68a7-979e-4c95-98d0-863964555250/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    def tearDown(self):
        pass
