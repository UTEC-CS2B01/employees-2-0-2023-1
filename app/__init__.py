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

    @app.route('/employees/<employee_id>', methods=['PATCH'])
    def modify_employee(employee_id):
        returned_code = 200
        try:
            body = request.form

            ids = [employee.id for employee in Employee.query.all()]
            if employee_id in ids:
               employee = Employee.query.filter_by(id=employee_id)
               if 'firstname' in body:
                   employee.firstname = request.form.get('firstname')

               if 'lastname' in body:
                   employee.lastname = request.form.get('lastname')

               if 'age' in body:
                   employee.age = request.form.get('age')

               if 'selectDepartment' in body:
                   employee.department_id = request.form.get('select_department')

                db.session.commit()
            else:
                return_code = 400

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False,
                            'message': 'Error modifying employee',
                            'errors': "Invalid id"}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error modifying employee'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Employee modified successfully!'}), returned_code

    @app.route('/employees/<employee_id', methods=['DELETE'])
    def delete_employee(employee_id):
        returned_code = 200
        try:
            ids = [employee.id for employee in Employee.query.all()]
            if employee_id in ids:
               employee = Employee.query.filter_by(id=employee_id)
               db.session.delete(employee)
               db.session.commit()
            else:
                return_code = 400

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False,
                            'message': 'Error deleting employee',
                            'errors': "Id doesn't exist in the database"}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error deleting employee'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Employee deleted successfully!'}), returned_code

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
    def create_department():
>>>>>>> b9f263d (Arreglando __init__)
        returned_code = 200
        list_errors = []
        try:
            body = request.form
            if 'name' not in body:
                list_errors.append('name is required')
            else:
                name = request.form['name']

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
            return jsonify({'id': department_id, 'success': True, 'message': 'Department created successfully!'}), returned_code

    return app

    @app.route('/employees', methods=['GET'])
    def get_employees():
        try:
            employees = Employee.query
            if request.args.has("search"):
                search_querry = request.args.get("search")
                employees = employees.filter(Employee.firstname.ilike(f'%{search_querry}%'))

            employees = employees.all()
            employees_serialized = [employee.serialize() for employee in employees]
        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error doing search'}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error doing search'}), returned_code
        else:
            return jsonify({'success': True, 'message': "Search successfully", "list": employees_serialized}), returned_code

    @app.route('/departments', methods=['GET'])
    def get_departments():
        departments_serialized
        try:
            departments = Department.query
            if request.args.has("search"):
                search_querry = request.args.get("search")
                departments = departments.filter(Department.name.ilike(f'%{search_querry}%'))

            departments = departments.all()
            departments_serialized = [employee.serialize() for employee in departments]
        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error doing search'}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error doing search'}), returned_code
        else:
            return jsonify({'success': True, 'message': "Search successfully", "list": departments_serialized}), returned_code
