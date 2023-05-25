from flask import (
    Flask,
    request,
    jsonify
)
from .models import db, setup_db, Employee
from .models import db, setup_db, Department

from flask_cors import CORS
from .utilities import allowed_file

import os
import sys

def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        app.config['UPLOAD_FOLDER'] = 'static/employees'
        setup_db(app)
        CORS(app, origins='*')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        
        return response
    
    # post:
    @app.route('/employees', methods=['POST'])
    def create_employee():
        returned_code= 200
        list_errors = []
        try:
            body = request.form
            if 'firstname' not in body:
                list_errors.append('Nombre es requerido ')
            else:
                firstname = request.form.get('firstname')
            
            if 'lastname' not in body:
                list_errors.append('Apellido es requerido')
            else:
                lastname = request.form.get('lastname') 
            
            if 'age' not in body:
                list_errors.append('Edad es requerida')
            else:
                age = request.form.get('age')
            if 'selectDepartment' not in body:
                list_errors.append('SelecctDepartment es requerido')
            else:
                department_id = request.form.get('selectDepartment')

            if 'image' not in request.files:
                list_errors.append('Imagen es requerida')
            else:
                if 'image' not in request.files:
                    list_errors.append('Imagen es Requerida')
                else:
                    if 'image' not in request.files:
                        return jsonify({'success': False, 'message': 'Imagen no agregada'}),400
                    file = request.files['image']
                    if file.filename == '':
                        return jsonify({'success': False, 'message': 'Imagen no agregada'}),400
                    if not allowed_file(file.filename):
                        return jsonify({'success': False, 'message': 'Imagen no permitida'}), 400
            if len(list_errors) > 0:
                returned_code = 400
            else:
                employee = Employee(firstname, lastname, age, department_id)
                db.session.add(employee)
                db.session.commit()
                employee_id = employee.id
                
                cwd = os.getcwd()
                employee_dir = os.path.join(app.config['UPLOAD_FOLDER'], employee_id)
                os.makedirs(employee_dir, exist_ok=True)

                upload_folder = os.path.join(cwd, employee_dir)
                file.save(os.path.join(upload_folder, file.filename))
                employee.image = file.filename
                db.session.commit()
        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()
        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error al crear empleado', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error al crear empleado'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Empleado creado exitosamente'}), returned_code
        
    @app.route('/departments', methods=['POST'])
    def create_department():
        returned_code= 200
        list_errors = []
        try:
            body = request.form
            if 'name' not in body:
                list_errors.append('Nombre es requerido')
            else:
                name = request.form.get('name')
            if 'short_name' not in body:
                list_errors.append('Short_name es requerido')
            else:
                short_name = request.form.get('short_name')
            if len(list_errors) > 0:
                returned_code = 400
            else:
                department = Department(name, short_name)
                db.session.add(department)
                db.session.commit()
                department_id = department.id

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()
        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error al crear departamento', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error al crear departamento'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Departamento creado exitosamente'}), returned_code
        
    # get:
    @app.route('/employees', methods=['GET'])
    def get_employees():
        returned_code= 200
        error_message = ''
        list_errrors = []
        try:
            search_query = request.args.get('search_query', None)
            if search_query:
                employees = Employee.query.filter(Employee.firstname.like('%{}%'.format(search_query))).all()
                serialized_employees = [employee.serialize() for employee in employees]
                return jsonify({'employees': serialized_employees}), returned_code
            
            employees = Employee.query.all()
            employee_list = [employee.serialize() for employee in employees]          

            if not employee_list:
                returned_code = 404 
                error_message = 'No se encontraron empleados'
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
            error_message = 'Error al obtener empleados'
        finally:
            db.session.close()
        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code
        
        return jsonify({'success': True, 'employees': employee_list}), returned_code
    
    @app.route('/departments', methods=['GET'])
    def get_departments():
        returned_code= 200
        error_message = ''
        list_errrors = []
        try:
            search_query = request.args.get('search_query', None)
            if search_query:
                departments = Department.query.filter(Department.name.like('%{}%'.format(search_query))).all()
                serialized_departments = [department.serialize() for department in departments]
                return jsonify({'departments': serialized_departments}), returned_code
            
            departments = Department.query.all()
            department_list = [department.serialize() for department in departments]          

            if not department_list:
                returned_code = 404 
                error_message = 'No se encontraron departamentos'
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
            error_message = 'Error al obtener departamentos'
        finally:
            db.session.close()
        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code
        
        return jsonify({'success': True, 'departments': department_list}), returned_code
    
    #patch:
    @app.route('/employees/<employee_id>', methods=['PATCH'])
    def update_employee(employee_id):
        returned_code= 200
        error_message = ''
        try:
            employee = Employee.query.get(employee_id)  
            if not employee:
                returned_code= 404
                error_message = 'Empleado no encontrado'
            else:
                body = request.form
                if 'firstname' in body:
                    employee.firstname = request.form('firstname')
                if 'lastname' in body:
                    employee.lastname = request.form('lastname')
                if 'age' in body:
                    employee.age = request.form('age')
                print(request.form['is_active'])
                if 'is_active' in body:
                    employee.is_active = True if request.form['is_active'] == 'true' else False
                db.session.commit()
        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error al actualizar empleado'
        finally:
            db.session.close()
        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code
        
        return jsonify({'success': True, 'message': 'Empleado actualizado exitosamente'}), returned_code
    @app.route('/departments/<department_id>', methods=['PATCH'])
    def update_department(department_id):
        returned_code= 200
        error_message = ''  
        try:
            department = Department.query.get(department_id)
            if not department:
                returned_code= 404
                error_message = 'Departamento no encontrado'
            else:
                body = request.form
                if 'name' in body:
                    department.name = request.form('name')
                if 'short_name' in body:
                    department.short_name = request.form('short_name')
                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error al actualizar departamento'
        finally:
            db.session.close()
        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code
        
        return jsonify({'success': True, 'message': 'Departamento actualizado exitosamente'}), returned_code
    
    #delete:
    @app.route('/employees/<employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        returned_code= 200
        error_message = ''
        try:
            employee = Employee.query.get(employee_id)
            if not employee:
                returned_code= 404
                error_message = 'Empleado no encontrado'
            else:
                db.session.delete(employee)
                db.session.commit()
        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error al eliminar empleado'
        finally:
            db.session.close()
        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code
        
        return jsonify({'success': True, 'message': 'Empleado eliminado exitosamente'}), returned_code
    @app.route('/departments/<department_id>', methods=['DELETE'])
    def delete_department(department_id):
        returned_code= 200
        error_message = ''
        try:
            department = Department.query.get(department_id)
            if not department:
                returned_code= 404
                error_message = 'Departamento no encontrado'
            else:
                db.session.delete(department)
                db.session.commit()
        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error al eliminar departamento'
        finally:
            db.session.close()
        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code
        
        return jsonify({'success': True, 'message': 'Departamento eliminado exitosamente'}), returned_code

    # #postCOLLECTION:
    # @app.rooute('/employess/employee_id/departments', methods=['POST'])
    # def assign_employee_department(employee_id):
    #     returned_code= 200
    #     error_message = ''
    #     try:
    #         employee = request.query.get['employee_id']
    #         if not employee:
    #            returned_code= 404
    #             error_message = 'Empleado no encontrado'
    #         else:
    #             body = request.form
    #             if 'name' in 
    return app



            
