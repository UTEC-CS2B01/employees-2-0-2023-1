from flask import (
    Flask,
    request,
    jsonify
)
from .models import db, setup_db, Employee, Department
from flask_cors import CORS
from .utilities import allowed_file
from datetime import datetime

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
        
        
    @app.route('/employees', methods=['GET'])
    def get_employees():
        try:
            employees = Employee.query.all()
            return jsonify([employee.serialize() for employee in employees]), 200
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'message': 'Error retrieving employees'}), 500


    @app.route('/employees/<string:employee_id>', methods=['PATCH'])
    def patch_employee(employee_id):
        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                return jsonify({'success': False, 'message': 'Employee not found'}), 404

            body = request.get_json()
            if 'firstname' in body:
                employee.firstname = body['firstname']
            if 'lastname' in body:
                employee.lastname = body['lastname']
            if 'age' in body:
                employee.age = body['age']
            if 'department_id' in body:
                employee.department_id = body['department_id']

            employee.modified_at = datetime.utcnow()

            db.session.commit()
            return jsonify({'success': True, 'message': 'Employee updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error updating employee'}), 500

        finally:
            db.session.close()


    @app.route('/employees/<string:employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                return jsonify({'success': False, 'message': 'Employee not found'}), 404

            db.session.delete(employee)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Employee deleted successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error deleting employee'}), 500

        finally:
            db.session.close()
        
           
    
    @app.route('/departments', methods=['POST'])
    def create_department():
        returned_code = 200
        list_errors = []
        try:
            body = request.form
            if 'name' not in body:
                list_errors.append('name is required')
            else:
                name = request.form['name']
            if 'shortname' not in body:
                list_errors.append('shortname is required')
            else:
                shortname = request.form['shortname']
            if len(list_errors) > 0:
                returned_code = 400
                
        except Exception as e:
            print(e)
            returned_code = 500
        
    @app.route('/departments', methods=['GET'])
    def get_departments():
        try:
            departments = Department.query.all()
            return jsonify([department.serialize() for department in departments]), 200
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'message': 'Error retrieving departments'}), 500
        
    @app.route('/departments/<string:department_id>', methods=['PATCH'])
    def patch_department(department_id):
        try:
            department = Department.query.get(department_id)

            if not department:
                return jsonify({'success': False, 'message': 'Department not found'}), 404

            body = request.get_json()
            if 'name' in body:
                department.name = body['name']
            if 'short_name' in body:
                department.short_name = body['short_name']

            department.modified_at = datetime.utcnow()

            db.session.commit()
            return jsonify({'success': True, 'message': 'Department updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error updating department'}), 500

        finally:
            db.session.close()

    @app.route('/departments/<string:department_id>', methods=['DELETE'])
    def delete_department(department_id):
        try:
            department = Department.query.get(department_id)

            if not department:
                return jsonify({'success': False, 'message': 'Department not found'}), 404

            db.session.delete(department)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Department deleted successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error deleting department'}), 500

        finally:
            db.session.close()


        
    return app
