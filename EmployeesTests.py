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



    # POST ------------------------------------------------
    # =====================================================


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

    def test_upload_file_failed_400(self):
        response = self.client.post('/files', data={}, content_type='multipart/form-data')
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

        response = self.client.post('/files', data=form_data, content_type='multipart/form-data')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # test of /employees/<employee_id>/departments

    def test_add_department_to_employee_success(self):
        data = {
            'name': 'Information Technology',
            'short_name': 'IT',
        }
        response = self.client.post('/employees/508ec843-213b-47ec-9052-46154d4007c2/departments', content_type='multipart/form-data', data=data)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])


    def test_add_department_to_employee_failed_400(self):
        data = {
            'name': 'Information Technology',
        }
        response = self.client.post('/employees/508ec843-213b-47ec-9052-46154d4007c2/departments', content_type='multipart/form-data', data=data)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_add_department_to_employee_failed_500(self):
        data = {
            'name': 'Casur Agency',
            'short_name': 'ASLDBASKLDNLKSADNLSKANDLKSNDLSNDLKNA', #Un nombre muy largo
        }
        response = self.client.post('/employees/91d1b904-7583-4af1-a833-5c260fd586f6/departments', content_type='multipart/form-data', data=data)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # GET ------------------------------------------------
    # ====================================================

    # test of /employees

    def test_get_employees_success(self):
        response = self.client.get('/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_get_employees_failed_404(self):

        response = self.client.get('/employees?search=*')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)



    # test of /departments

    def test_get_departments_success(self):
        response = self.client.get('/departments')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_get_departments_failed_404(self):
        response = self.client.get('/departments?search=nnnjb/*')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


    # /employees/<employee_id>/department

    def test_get_employee_department_success(self):
        response = self.client.get('/employees/508ec843-213b-47ec-9052-46154d4007c2/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['department'])
        self.assertTrue(data['employee'])


    def test_get_employee_department_failed_404(self):
        response = self.client.get('/employees/1234/department')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


    # test of /departments/<department_id>/employees

    def test_get_department_employees_success(self):
        response = self.client.get('/departments/c8d29a66-f718-45fe-9a4c-d70013d7fdc6/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])


    def test_get_department_employees_failed_404(self):
        response = self.client.get('/departments/1234/employees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


    # test of /employees/search

    def test_search_employees_success(self):
        args = {
            'firstname': 'Bianca',
            'lastname': 'Aguinaga',
            'age': 16,
        }

        response = self.client.get('/employees/search', query_string=args)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['employees'])
    
    def test_search_employees_failed_400(self):

        response = self.client.get('/employees/search')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_search_employees_failed_404(self):
        args = {
            'firstname': 'NoUsuarioNombre',
            'lastname': 'NoUsuarioApellido',
            'age': 0
        }

        response = self.client.get('/employees/search', query_string=args);

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


    # test of /departments/search

    def test_search_departments_success(self):
        args = {
            'short_name': 'IT',
        }

        response = self.client.get('/departments/search', query_string=args)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['departments'])

    def test_search_departments_failed_400(self): 
        response = self.client.get('/departments/search')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_search_departments_failed_404(self):
        args = {
            'short_name': 'NoDepartamento',
        }

        response = self.client.get('/departments/search', query_string=args)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)



    # PATCH ---------------------------------------------
    # ===================================================

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


    # test of /departments/<department_id>

    def test_update_department_success(self):
        form_data = {
            'name': 'Casur Agency 2',
        }

        response = self.client.patch('/departments/2c495a2a-d223-4e61-b716-43e3a3f5a9c9', content_type = 'multipart/form-data', data=form_data)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


    def test_update_department_404(self):
        response = self.client.patch('/departments/234567')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)


    # test of /employees/<employee_id>/departments

    def test_update_employee_department_success(self):
        form_data = {
            'department_id': '7cf0cb5d-c255-4bd2-b98f-23aae79952cf',
        }

        response = self.client.patch('/employees/508ec843-213b-47ec-9052-46154d4007c2/departments', content_type = 'multipart/form-data', data=form_data)

        data = json.loads(response.data)
    
        self.assertEqual(response.status_code, 200)

    def test_update_employee_department_400(self):

        response = self.client.patch('/employees/508ec843-213b-47ec-9052-46154d4007c2/departments')

        data = json.loads(response.data)
    
        self.assertEqual(response.status_code, 400)

    def test_update_employee_department_404(self):
        form_data = {
            'department_id': '7cf0cb5d-c255-4bd2-b98f-23aae79952cf',
        }

        response = self.client.patch('/employees/1234/departments', content_type = 'multipart/form-data', data=form_data)

        data = json.loads(response.data)
    
        self.assertEqual(response.status_code, 404)

    
    # test of /employees/<employee_id>

    def test_delete_employee_success(self):
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'age': '20',
            'selectDepartment': '7cf0cb5d-c255-4bd2-b98f-23aae79952cf',
            'image': (io.BytesIO(file_content), 'test.png')
        }
        response = self.client.patch('/employees/d366bab5-2973-4ff5-ba25-c2df425596c7', content_type = 'multipart/form-data', data=form_data)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_employee_failed_400(self):
        response = self.client.patch('/employees/d366bab5-2973-4ff5-ba25-c2df425596c7')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_delete_employee_failed_500(self):
        with open('static/testImages/test.png', 'rb') as file:
            file_content = file.read()

        form_data = {
            'age': '20',
            'selectDepartment': '1234',
            'image': (io.BytesIO(file_content), 'test.png')
        }
        response = self.client.patch('/employees/d366bab5-2973-4ff5-ba25-c2df425596c7', content_type = 'multipart/form-data', data=form_data)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)


    # DELETE -----------------------------------------------
    # ======================================================

    # test of /departments/<department_id>

    def test_delete_department_success(self):
        myId = "";

        #obtener todos los departamentos
        response = self.client.get('/departments')
        data = json.loads(response.data)


        #obtener el id de un departamento cualquiera
        myId = data['data'][-1]['id']
        response = self.client.delete('/departments/' + str(myId))

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_department_404(self):
        response = self.client.delete('/departments/1234')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_department_500(self):
        #obtener todos los employees
        response = self.client.get('/employees')
        data = json.loads(response.data)

        #buscar uno que tenga department_id
        myId = ""
        for employee in data['data']:
            if 'department_id' in employee:
                myId = employee['department_id']
                break

        #ahora si intentamos borrar el departamento, no podrá puesto que viola la FK de employees
        # por lo que dará error 500
        response = self.client.delete('/departments/' + str(myId))

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)


    # test of /employees/<employee_id>

    def test_delete_employee_success(self):
        myId = "";

        #obtener todos los employees
        response = self.client.get('/employees')
        data = json.loads(response.data)

        #obtener el id de un employee cualquiera
        myId = data['data'][-1]['id']
        response = self.client.delete('/employees/' + str(myId))

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_employee_404(self):
        response = self.client.delete('/employees/1234')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_delete_employee_500(self):
        # 508ec843-213b-47ec-9052-46154d4007c2 es un id de un empleado con un file
        # da error puesto que no se ha borrado el file (no hay una ruta para ello)
        response = self.client.delete('/employees/508ec843-213b-47ec-9052-46154d4007c2')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)


    # test of /employees/<employee_id>/departments

    def test_delete_employee_department_success(self):
        myId = "";

        #obtener todos los employees
        response = self.client.get('/employees')
        data = json.loads(response.data)

        #obtener el id de un employee cualquiera
        myId = data['data'][-1]['id']
        response = self.client.delete('/employees/' + str(myId) + '/departments')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_employee_department_404(self):
        response = self.client.delete('/employees/1234/departments')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        pass



    #test para la ruta 1

