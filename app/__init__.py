from flask import (
    Flask,
    request,
    jsonify
)
from .models import db, setup_db, Employee
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
    

    @app.route('/employees', methods=['POST'])
    def create_employee():
        returned_code = 200
        list_errors = []
        try:
            body = request.form

            if 'firstname' not in body:
                list_errors.append('firstname is required')
            else:
                firstname = request.form.get('firstname')

            if 'lastname' not in body:
                list_errors.append('lastname is required')    
            else:
                lastname = request.form['lastname']

            if 'age' not in body:
                list_errors.append('age is required')    
            else:
                age = request.form['age']

            if 'selectDepartment' not in body:
                list_errors.append('selectDepartment is required')
            else:
                department_id = request.form['selectDepartment']

            if 'image' not in request.files:
                list_errors.append('image is required')
            else:
                if 'image' not in request.files:
                    return jsonify({'success': False, 'message': 'No image provided by the employee'}), 400
        
                file = request.files['image']

                if file.filename == '':
                    return jsonify({'success': False, 'message': 'No image selected'}), 400
        
                if not allowed_file(file.filename):
                    return jsonify({'success': False, 'message': 'Image format not allowed'}), 400
        

            if len(list_errors) > 0:
                returned_code = 400
            else:
                employee = Employee(firstname, lastname, age, department_id)
                db.session.add(employee)
                db.session.commit()

                employee_id = employee.id

                cwd = os.getcwd()

                employee_dir = os.path.join(app.config['UPLOAD_FOLDER'], employee.id)
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
            return jsonify({'success': False, 'message': 'Error creating employee', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error creating employee'}), returned_code
        else:
            return jsonify({'id': employee_id, 'success': True, 'message': 'Employee Created successfully!'}), returned_code

    return app

    @app.route('/employees/<id>', methods=['GET', 'DELETE', 'PATCH'])
    def get_employee(id):
        if request.method == 'GET':
            try:
                employee = Employee.query.get(id)
                if employee is None:
                    return jsonify({'success': False, 'message': 'Employee not found'}), 404
                else:
                    return jsonify({'success': True, 'employee': employee.format()}), 200
            except Exception as e:
                print(e)
                print(sys.exc_info())
                return jsonify({'success': False, 'message': 'Error getting employee'}), 500
            finally:
                db.session.close()
        elif request.method == 'DELETE':
            try:
                employee = Employee.query.get(id)
                if employee is None:
                    return jsonify({'success': False, 'message': 'Employee not found'}), 404
                else:
                    db.session.delete(employee)
                    db.session.commit()
                    return jsonify({'success': True, 'message': 'Employee deleted successfully!'}), 200
            except Exception as e:
                print(e)
                print(sys.exc_info())
                return jsonify({'success': False, 'message': 'Error deleting employee'}), 500
            finally:
                db.session.close()

        elif request.method == 'PATCH':
            returned_code = 200
            list_errors = []
            try:
                body = request.form
                if 'firstname' not in body:
                    list_errors.append('firstname is required')
                if 'lastname' not in body:
                    list_errors.append('lastname is required')
                if 'age' not in body:
                    list_errors.append('age is required')
                if 'selectDepartment' not in body:
                    list_errors.append('selectDepartment is required')
                if len(list_errors) > 0:
                    returned_code = 400
                else:
                    employee = Employee.query.get(id)
                    if employee is None:
                        return jsonify({'success': False, 'message': 'Employee not found'}), 404
                    else:
                        employee.firstname = request.form['firstname']
                        employee.lastname = request.form['lastname']
                        employee.age = request.form['age']
                        employee.department_id = request.form['selectDepartment']
                        db.session.commit()
            except Exception as e:
                print(e)
                print(sys.exc_info())
                db.session.rollback()
                returned_code = 500
            finally:
                db.session.close()
            
            if returned_code == 400:
                return jsonify({'success': False, 'message': 'Error updating employee', 'errors': list_errors}), returned_code
            elif returned_code == 500:
                return jsonify({'success': False, 'message': 'Error updating employee'}), returned_code
            else:
                return jsonify({'success': True, 'message': 'Employee updated successfully!'}), returned_code
            

    @app.route('/departments', methods=['GET'])
    def create_departments():
        returned_code = 200
        list_errors = []
        try:
            body = request.form
            if 'name' not in body:
                list_errors.append('name is required')
            if 'short_name' not in body:
                list_errors.append('short_name is required')
            if len(list_errors) > 0:
                returned_code = 400
            else:
                name = request.form['name']
                short_name = request.form['short_name']
                department = Department(name, short_name)
                db.session.add(department)
                db.session.commit()
        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()
        
        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error creating department', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error creating department'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Department Created successfully!'}), returned_code
        

    @app.route('/departments/<id>', methods=['GET', 'DELETE', 'PATCH'])
    def get_department(id):
        if request.method == 'GET':
            try: 
                department = Department.query.get(id)
                if department is None:
                    return jsonify({'success': False, 'message': 'Department not found'}), 404
                else:
                    return jsonify({'success': True, 'department': department.format()}), 200
            except Exception as e:
                print(e)
                print(sys.exc_info())
                return jsonify({'success': False, 'message': 'Error getting department'}), 500
            finally:
                db.session.close()
        elif request.method == 'DELETE':
            try:
                department = Department.query.get(id)
                if department is None:
                    return jsonify({'success': False, 'message': 'Department not found'}), 404
                else:
                    db.session.delete(department)
                    db.session.commit()
                    return jsonify({'success': True, 'message': 'Department deleted successfully!'}), 200
            except Exception as e:
                print(e)
                print(sys.exc_info())
                return jsonify({'success': False, 'message': 'Error deleting department'}), 500
            finally:
                db.session.close()
        elif request.method == 'PATCH':
            returned_code = 200
            list_errors = []
            try:
                body = request.form
                if 'name' not in body:
                    list_errors.append('name is required')
                if 'short_name' not in body:
                    list_errors.append('short_name is required')
                if len(list_errors) > 0:
                    returned_code = 400
                else:
                    department = Department.query.get(id)
                    if department is None:
                        return jsonify({'success': False, 'message': 'Department not found'}), 404
                    else:
                        department.name = request.form['name']
                        department.short_name = request.form['short_name']
                        db.session.commit()
            except Exception as e:
                print(e)
                print(sys.exc_info())
                db.session.rollback()
                returned_code = 500
            finally:
                db.session.close()
            
            if returned_code == 400:
                return jsonify({'success': False, 'message': 'Error updating department', 'errors': list_errors}), returned_code
            elif returned_code == 500:
                return jsonify({'success': False, 'message': 'Error updating department'}), returned_code
            else:
                return jsonify({'success': True, 'message': 'Department updated successfully!'}), returned_code
        
