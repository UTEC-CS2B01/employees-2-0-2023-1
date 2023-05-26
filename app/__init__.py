from flask import (
    Flask,
    request,
    jsonify
)
from .models import db, setup_db, Employee, Department
from datetime import datetime
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

    @app.route('/departments', methods=['GET'])
    def get_departments():
        departments = Department.query.all()
        serialized_departments = [department.serialize() for department in departments]
        return jsonify({'departments': serialized_departments})

    # Endpoint para crear un nuevo departamento
    @app.route('/departments', methods=['POST'])
    def create_department():
        try:
            data = request.get_json()
            name = data.get('name')
            short_name = data.get('short_name')

            if not name or not short_name:
                return jsonify({'success': False, 'message': 'Name and short_name are required fields'}), 400

            department = Department(name, short_name)
            db.session.add(department)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Department created successfully!', 'department': department.serialize()}), 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error creating department'}), 500

    # Endpoint para actualizar un departamento existente
    @app.route('/departments/<department_id>', methods=['PATCH'])
    def update_department(department_id):
        try:
            data = request.get_json()
            department = Department.query.get(department_id)

            if not department:
                return jsonify({'success': False, 'message': 'Department not found'}), 404

            name = data.get('name')
            short_name = data.get('short_name')

            if name:
                department.name = name
            if short_name:
                department.short_name = short_name

            department.modified_at = datetime.utcnow()

            db.session.commit()

            return jsonify({'success': True, 'message': 'Department updated successfully!', 'department': department.serialize()}), 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error updating department'}), 500

    # Endpoint para eliminar un departamento existente
    @app.route('/departments/<department_id>', methods=['DELETE'])
    def delete_department(department_id):
        try:
            department = Department.query.get(department_id)

            if not department:
                return jsonify({'success': False, 'message': 'Department not found'}), 404

            db.session.delete(department)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Department deleted successfully!'}), 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error deleting department'}), 500

    # Endpoint para actualizar un empleado existente
    @app.route('/employees/<employee_id>', methods=['PATCH'])
    def update_employee(employee_id):
        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                return jsonify({'success': False, 'message': 'Employee not found'}), 404

            data = request.get_json()
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            age = data.get('age')
            department_id = data.get('department_id')

            if firstname:
                employee.firstname = firstname
            if lastname:
                employee.lastname = lastname
            if age:
                employee.age = age
            if department_id:
                employee.department_id = department_id

            employee.modified_at = datetime.utcnow()

            db.session.commit()

            return jsonify({'success': True, 'message': 'Employee updated successfully!', 'employee': employee.serialize()}), 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error updating employee'}), 500

    # Endpoint para eliminar un empleado existente
    @app.route('/employees/<employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                return jsonify({'success': False, 'message': 'Employee not found'}), 404

            db.session.delete(employee)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Employee deleted successfully!'}), 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error deleting employee'}), 500
    
    @app.route('/employees/search', methods=['GET'])
    def search_employees():
        try:
            search_query = request.args.get('query')

            if not search_query:
                return jsonify({'success': False, 'message': 'Query parameter is required'}), 400

            employees = Employee.query.filter(Employee.firstname.ilike(f'%{search_query}%') | Employee.lastname.ilike(f'%{search_query}%')).all()
            serialized_employees = [employee.serialize() for employee in employees]

            return jsonify({'success': True, 'employees': serialized_employees}), 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            return jsonify({'success': False, 'message': 'Error searching employees'}), 500

    @app.route('/departments/search', methods=['GET'])
    def search_departments():
        try:
            search_query = request.args.get('query')

            if not search_query:
                return jsonify({'success': False, 'message': 'Query parameter is required'}), 400

            departments = Department.query.filter(Department.name.ilike(f'%{search_query}%') | Department.short_name.ilike(f'%{search_query}%')).all()
            serialized_departments = [department.serialize() for department in departments]

            return jsonify({'success': True, 'departments': serialized_departments}), 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            return jsonify({'success': False, 'message': 'Error searching departments'}), 500
    

    return app