from flask import (
    Flask,
    request,
    jsonify
)
from .models import db, setup_db, Employee, Department
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
        
    @app.route('/departments', methods=['POST'])
    def create_departament():
        returned_code = 200
        list_errors = []
        try:
            body = request.form

            if 'name' not in body:
                list_errors.append('name is required')
            else:
                name = request.form.get('name')

            if 'short_name' not in body:
                list_errors.append('short_name is required')    
            else:
                short_name = request.form['short_name']

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
            return jsonify({'success': False, 'message': 'Error creating department', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error creating department'}), returned_code
        else:
            return jsonify({'id': department_id, 'success': True, 'message': 'Department Created successfully!'}), returned_code
         
    @app.route('/departments', methods=['GET'])
    def show_departaments():
        returned_code = 200
        try:
            departments = Department.query.all()
            departments_serialized = [department.serialize() for department in departments]
            
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 500:
            return jsonify({'success': False, 'message': 'Error founding department'}), returned_code
        else:
            if len(departments_serialized) == 0:
                returned_code = 400
                return jsonify({'success': True, 'message': 'No departments found'}), returned_code
            return jsonify({'success': True, 'message': departments_serialized}), returned_code

    @app.route('/employees', methods=['GET'])
    def show_employees():
        returned_code = 200
        try:
            employees = Employee.query.all()
            employees_serialized = [employee.serialize() for employee in employees]
            
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 500:
            return jsonify({'success': False, 'message': 'Error founding employees'}), returned_code
        else:
            if len(employees_serialized) == 0:
                returned_code = 400
                return jsonify({'success': True, 'message': 'No employees found'}), returned_code
            return jsonify({'success': True, 'message': employees_serialized}), returned_code

    @app.route('/employees/<id>', methods=['DELETE'])
    def delete_employees(id):
        returned_code = 200
        try:
            employee = Employee.query.get(id)
            if employee is None:
                returned_code = 400
                return jsonify({'success': True, 'message': 'No employees found'}), returned_code
            employee = Employee.query.filter_by(id = id)
            employee.delete()
            db.session.commit()
            
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 500:
            return jsonify({'success': False, 'message': 'Error deleting employee'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Employee delete'}), returned_code

    @app.route('/departments/<id>', methods=['DELETE'])
    def delete_departments(id):
        returned_code = 200
        try:
            department = Department.query.get(id)
            if department is None:
                returned_code = 400
                return jsonify({'success': True, 'message': 'No department found'}), returned_code
            department = Department.query.filter_by(id = id)
            department.delete()
            db.session.commit()
            
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 500:
            return jsonify({'success': False, 'message': 'Error deleting department'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Department delete'}), returned_code

    return app