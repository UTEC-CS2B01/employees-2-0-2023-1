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
                list_errors.append('department is required')
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
        returned_code = 200
        list_errors = []
        try:
            employees = Employee.query.all()
            employee_list = []

            if len(employees) == 0:
                list_errors.append('no employees found')
                returned_code = 400
            else: 
                for employee in employees:
                    employee_list.append({
                        'firstname': employee.firstname,
                        'lastname': employee.lastname,
                        'age': employee.age,
                        'department': employee.department.name,
                        'id': employee.id
                    })

        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
        finally:
            db.session.close()
        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error getting employees', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error getting employees'}), returned_code
        else:
            return jsonify({'employees':employee_list}), returned_code

    @app.route('/employees/<employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        returned_code = 200
        list_errors = []

        try:
            employee = Employee.query.get(employee_id)

            if employee is None:
                list_errors.append('employee dont exist')
                returned_code = 404
            else:
                db.session.delete(employee)
                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if len(list_errors) > 0:
            return jsonify({'success': False, 'message': 'Error deleting employee', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error deleting employee'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Employee deleted successfully!'}), returned_code

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
        
    @app.route('/departments', methods=['GET'])
    def get_departments():
        returned_code = 200
        list_errors = []
        try:
            departments = Department.query.all()
            department_list = []

            if len(departments) == 0:
                list_errors.append('no departments found')
                returned_code = 400
            else: 
                for department in departments:
                    department_list.append({
                        'id': department.id,
                        'name': department.name,
                        'short_name': department.short_name
                    })

        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
        finally:
            db.session.close()
        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error getting departments', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error getting deparments'}), returned_code
        else:
            return jsonify({'departments':department_list}), returned_code
    
    @app.route('/departments/<department_id>', methods=['DELETE'])
    def delete_department(department_id):
        returned_code = 200
        list_errors = []

        try:
            department = Department.query.get(department_id)

            if department is None:
                list_errors.append('department dont exist')
                returned_code = 404
            else:
                db.session.delete(department)
                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if len(list_errors) > 0:
            return jsonify({'success': False, 'message': 'Error deleting department', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error deleting department'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Department deleted successfully!'}), returned_code

    @app.route('/departments/<department_id>',methods=['PATCH'])
    def change_department(department_id):
        return_code = 200
        list_errors = []

        try:
            body = request.form
            department = Department.query.get(department_id)

            if department is None:
                list_errors.append('department dont exist')
                return_code = 404
            else:     

                if 'newname' not in body:
                    list_errors.append('newname is required')
                else:
                    department.name = request.form['newname']
                if 'newshortname' not in body:
                    list_errors.append('newshortname is required')
                else:
                    department.short_name = request.form['newshortname']
                    
            db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500
        finally:
            db.session.close() 
        if len(list_errors) > 0:
            return jsonify({'success': False, 'message': 'Error changing department', 'errors': list_errors}), return_code
        elif return_code == 500:
            return jsonify({'success': False, 'message': 'Error changing department'}), return_code
        else:
            return jsonify({'success': True, 'message': 'Deparmeent changed successfully!'}), return_code                            



    return app