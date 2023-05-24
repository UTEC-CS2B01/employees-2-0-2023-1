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
    
    @app.route('/employees', methods=['GET'])
    def get_employees():
        employees = Employee.query.filter_by(is_active=True).all()
        employees = [employee.serialize() for employee in employees]
        return jsonify({'success': True, 'employees': employees}), 200

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

    @app.route('/employees', methods=['PATCH'])
    def update_employee():
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
                file = request.files['image']

                if file.filename == '':
                    return jsonify({'success': False, 'message': 'No image selected'}), 400

                if not allowed_file(file.filename):
                    return jsonify({'success': False, 'message': 'Image format not allowed'}), 400

            if len(list_errors) > 0:
                returned_code = 400
            else:
                employee = Employee.query.first()  # Obtén el primer empleado de la base de datos o ajusta la lógica según tus necesidades

                if employee is None:
                    return jsonify({'success': False, 'message': 'No employees found'}), 404

                employee.firstname = firstname
                employee.lastname = lastname
                employee.age = age
                employee.department_id = department_id

                cwd = os.getcwd()

                employee_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(employee.id))
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
            return jsonify({'success': False, 'message': 'Error updating employee', 'errors': list_errors}), returned_code
        elif returned_code == 404:
            return jsonify({'success': False, 'message': 'No employees found'}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error updating employee'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Employee updated successfully!'}), returned_code
        
    @app.route('/employees', methods=['DELETE'])
    def delete_all_employees():
        returned_code = 200
        try:
            employees = Employee.query.all()

            if not employees:
                return jsonify({'success': False, 'message': 'No employees found'}), 404

            for employee in employees:
                db.session.delete(employee)

            db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 404:
            return jsonify({'success': False, 'message': 'No employees found'}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error deleting employees'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'All employees deleted successfully!'}), returned_code
    
    @app.route('/employees/<employee_id>', methods=['GET'])
    def get_employee(employee_id):
        try:
            employee = Employee.query.get(employee_id)

            if employee is None:
                return jsonify({'success': False, 'message': 'Employee not found'}), 404

            employee_data = employee.serialize()

            return jsonify({'success': True, 'employee': employee_data}), 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            return jsonify({'success': False, 'message': 'Error retrieving employee'}), 500
        
    @app.route('/employees/<employee_id>', methods=['PATCH'])
    def update_employee(employee_id):
        returned_code = 200
        list_errors = []
        try:
            employee = Employee.query.get(employee_id)

            if employee is None:
                return jsonify({'success': False, 'message': 'Employee not found'}), 404

            body = request.form

            if 'firstname' in body:
                employee.firstname = body['firstname']

            if 'lastname' in body:
                employee.lastname = body['lastname']

            if 'age' in body:
                employee.age = body['age']

            if 'selectDepartment' in body:
                employee.department_id = body['selectDepartment']

            if 'image' in request.files:
                file = request.files['image']

                if file.filename == '':
                    return jsonify({'success': False, 'message': 'No image selected'}), 400

                if not allowed_file(file.filename):
                    return jsonify({'success': False, 'message': 'Image format not allowed'}), 400

                cwd = os.getcwd()

                employee_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(employee.id))
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

        if returned_code == 500:
            return jsonify({'success': False, 'message': 'Error updating employee'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Employee updated successfully!'}), returned_code
        

    @app.route('/employees/<employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        returned_code = 200
        try:
            employee = Employee.query.get(employee_id)

            if employee is None:
                return jsonify({'success': False, 'message': 'Employee not found'}), 404

            db.session.delete(employee)
            db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 500:
            return jsonify({'success': False, 'message': 'Error deleting employee'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Employee deleted successfully!'}), returned_code
        


    @app.route('/departments', methods=['POST'])
    def create_department():
            returned_code = 200
            list_errors = []
            try:
                body = request.get_json()

                if 'name' not in body:
                    list_errors.append('name is required')
                else:
                    name = body['name']

                if 'short_name' not in body:
                    list_errors.append('short name is required')
                else:
                    short_name = body['short_name']

                
                if len(list_errors) > 0:
                    returned_code = 400
                else:
                    department = Department(name,short_name=short_name)
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
    def get_departments():
        departments = Department.query.all()
        departments = [department.serialize() for department in departments]
        return jsonify({'success': True, 'departments': departments}), 200
    
    
    @app.route('/departments/<int:department_id>', methods=['PATCH'])
    def update_department(department_id):
        returned_code = 200
        list_errors = []
        try:
            department = Department.query.get(department_id)

            if department is None:
                return jsonify({'success': False, 'message': 'Department not found'}), 404

            body = request.get_json()

            if 'name' in body:
                department.name = body['name']

            if 'short_name' in body:
                department.short_name = body['short_name']

            db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 500:
            return jsonify({'success': False, 'message': 'Error updating department'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Department updated successfully!'}), returned_code

    @app.route('/departments/<int:department_id>', methods=['DELETE'])
    def delete_department(department_id):
        returned_code = 200
        try:
            department = Department.query.get(department_id)

            if department is None:
                return jsonify({'success': False, 'message': 'Department not found'}), 404

            db.session.delete(department)
            db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 500:
            return jsonify({'success': False, 'message': 'Error deleting department'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Department deleted successfully!'}), returned_code

    return app    

