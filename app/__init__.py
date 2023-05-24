from flask import (
    Flask,
    request,
    jsonify
)
from .models import db, setup_db, Employee
from .models import db, setup_db, Department

from flask_cors import CORS
from flask_sqlalchemy import or_
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

    @app.route('/employees', methods=['GET'])
    def get_employees():
        employees = Employee.query.all()
        employees_list = []
        for employee in employees:
            employee_data = {
                'id': employee.id,
                'firstname': employee.firstname,
                'lastname': employee.lastname,
                'age': employee.age,
                'is_active': employee.is_active,
                'department_id': employee.department_id,
                'image': employee.image
            }
            employees_list.append(employee_data)

        return jsonify(employees_list), 200
    
    @app.route('/employees/<int:employee_id>', methods=['PATCH'])
    def update_employee(employee_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        
        employee_data = request.get_json()

        for key, value in employee_data.items():
            setattr(employee, key, value)
        db.session.commit()
        db.session.close()
        return jsonify({'success': True, 'message': 'Employee updated successfully!'}), 200
    
    @app.route('/employees/<int:employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        
        db.session.delete(employee)
        db.session.commit()
        db.session.close()
        return jsonify({'success': True, 'message': 'Employee deleted successfully!'}), 200


    
    @app.route('/departments', methods=['POST'])
    def create_departments():
        returned_code = 200
        list_errors = []
        try:
            body = request.form
            if 'name' not in body:
                list_errors.append('name is required')
            else:
                name = request.form.get('name')
            
            if 'short_name' not in body:
                list_errors.append('shortname is required')    
            else:
                short_name = request.form.get['shortname']

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
    def get_departments():
        departments = Department.query.all()
        departments_list = []
        for department in departments:
            department_data = {
                'id': department.id,
                'name': department.name,
                'short_name': department.short_name
            }
            departments_list.append(department_data)

        return jsonify(departments_list), 200
    
    @app.route('/departments/<int:department_id>', methods=['PATCH'])
    def update_department(department_id):
        department = Department.query.get(department_id)
        if department is None:
            return jsonify({'success': False, 'message': 'Department not found'}), 404
        
        department_data = request.get_json()

        for key, value in department_data.items():
            setattr(department, key, value)
        db.session.commit()
        db.session.close()
        return jsonify({'success': True, 'message': 'Department updated successfully!'}), 200
    
    @app.route('/departments/<int:department_id>', methods=['DELETE'])
    def delete_department(department_id):
        department = Department.query.get(department_id)
        if department is None:
            return jsonify({'success': False, 'message': 'Department not found'}), 404
        
        db.session.delete(department)
        db.session.commit()
        db.session.close()
        return jsonify({'success': True, 'message': 'Department deleted successfully!'}), 200
    



    @app.route('/employees/<id>/departments', methods=['POST'])
    def create_employee_department(id):
        employee = Employee.query.get(id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        data = request.get_json()
        department = Department(name=data['name'], short_name=data['short_name'])
        department.employees.append(employee)
        db.session.add(department)
        db.session.commit()

        return jsonify(department.serialize()), 201
    
    @app.route('/employees/<id>/departments', methods=['GET'])
    def get_employee_departments(id):
        employee = Employee.query.get(id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404

        departments = employee.departments
        departments_list = []
        for department in departments:
            department_data = {
                'id': department.id,
                'name': department.name,
                'short_name': department.short_name
            }
            departments_list.append(department_data)

        return jsonify(departments_list), 200
    
    @app.route('/employees/<id>/departments', methods = ['PATCH'])
    def update_employee_department(employee_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        department_data = request.get_json()
        department_id = department_data.get('department_id')

        if not department_id:
            return jsonify({'success': False, 'message': 'Department ID is required'}), 400 
        
    @app.route('/employees/<id>/departments', methods = ['DELETE'])
    def delete_employee_department(employee_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        if employee.department is None:
            return jsonify({'success': False, 'message': 'Employee does not belong to any department'}), 400
        employee.department = None
        db.session.commit()

        return jsonify({'success': True, 'message': 'Employee removed from department successfully!'}), 200
    
    

    @app.route('employees/<id>/departments/<id>', methods=['POST'])
    def add_employee_department(employee_id, department_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        department = Department.query.get(department_id)
        if department is None:
            return jsonify({'success': False, 'message': 'Department not found'}), 404

        employee.departments.append(department)
        db.session.commit() 
        return jsonify({'success': True, 'message': 'Employee added to department successfully!'}), 200
    

    @app.route('employees/<id>/departments/<id>', methods=['GET'])
    def get_employee_department(employee_id, department_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        department = Department.query.get(department_id)
        if department is None:
            return jsonify({'success': False, 'message': 'Department not found'}), 404
        
        if employee.department != department:
            return jsonify({'success': False, 'message': 'Employee does not belong to this department'}), 400
        
        return jsonify(employee.department.serialize()), 200
    
    @app.route('employees/<id>/departments/<id>', methods=['PATCH'])
    def update_employee_department(employee_id, department_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        department = Department.query.get(department_id)
        if department is None:
            return jsonify({'success': False, 'message': 'Department not found'}), 404
        if employee.department != department:
            return jsonify({'success': False, 'message': 'Employee does not belong to this department'}), 404
        
        department_data = request.get_json()
        for key, value in department_data.items():
            setattr(department, key, value)
        db.session.commit()

        return jsonify(employee.department.serialize()), 200
            
    
    @app.route('/employees/<employee_id>/departments/<department_id>', methods=['DELETE'])
    def delete_employee_department(employee_id, department_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404
        
        department = Department.query.get(department_id)
        if department is None:
            return jsonify({'success': False, 'message': 'Department not found'}), 404
        
        if employee.department != department:
            return jsonify({'success': False, 'message': 'Employee does not belong to this department'}), 400
        
        employee.department = None
        db.session.commit()

        return jsonify({'success': True, 'message': 'Employee department deleted successfully'}), 200


    @app.route('/employees', methods=['GET'])
    def search_employees():
        search_query = request.args.get('search', '')
        
        employees = Employee.query.filter(
            or_(
                Employee.firstname.ilike(f'%{search_query}%'),
                Employee.lastname.ilike(f'%{search_query}%')
            )
        ).all()
        
        serialized_employees = [employee.serialize() for employee in employees]
        
        return jsonify(serialized_employees), 200

    @app.route('/departments', methods=['GET'])
    def search_departments():
        search_query = request.args.get('search', '')
        
        departments = Department.query.filter(
            or_(
                Department.name.ilike(f'%{search_query}%'),
                Department.short_name.ilike(f'%{search_query}%')
            )
        ).all()
        
        serialized_departments = [department.serialize() for department in departments]
        
        return jsonify(serialized_departments), 200

    

    return app




