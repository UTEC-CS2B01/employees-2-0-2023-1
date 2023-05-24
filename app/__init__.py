from flask import (
    Flask,
    request,
    jsonify
)
from models import db, setup_db, Employee, Department
from flask_cors import CORS
from utilities import allowed_file

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
    

    @app.route('/employees', methods=['POST', 'GET', 'PATCH', 'DELETE'])
    def create_employee():
    returned_code = 200
    list_errors = []
    try:
        if request.method == 'POST':
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

        elif request.method == 'GET':
            # Aquí va la lógica para obtener todos los empleados
            employees = Employee.query.all()
            employee_data = []
            for employee in employees:
                employee_data.append({
                    'id': employee.id,
                    'firstname': employee.firstname,
                    'lastname': employee.lastname,
                    'age': employee.age,
                    'department_id': employee.department_id,
                    'image': employee.image
                })
            return jsonify({'employees': employee_data})

        elif request.method == 'PATCH':
            employee_id = request.args.get('id')
            if employee_id is None:
                return jsonify({'success': False, 'message': 'Employee ID is required'}), 400
            
            employee = Employee.query.get(employee_id)
            if employee is None:
                return jsonify({'success': False, 'message': 'Employee not found'}), 404

            # Aquí va la lógica para actualizar los datos del empleado
            body = request.form
            if 'firstname' in body:
                employee.firstname = body['firstname']
            
            if 'lastname' in body:
                employee.lastname = body['lastname']

            if 'age' in body:
                employee.age = body['age']

            if 'selectDepartment' in body:
                employee.department_id = body['selectDepartment']

            db.session.commit()
            return jsonify({'success': True, 'message': 'Employee updated successfully'})

        elif request.method == 'DELETE':
            employee_id = request.args.get('id')
            if employee_id is None:
                return jsonify({'success': False, 'message': 'Employee ID is required'}), 400

            employee = Employee.query.get(employee_id)
            if employee is None:
                return jsonify({'success': False, 'message': 'Employee not found'})

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
        
        
        





























    @app.route('/departments', methods=['POST', 'GET', 'PATCH','DELETE'])
    def create_departaments():
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
                departament = Department(name, short_name )
                db.session.add(departament)
                db.session.commit()

                departament_id = departament.id

                cwd = os.getcwd()

                departament_dir = os.path.join(app.config['UPLOAD_FOLDER'], departament.id)
                os.makedirs(departament_dir, exist_ok=True)

                upload_folder = os.path.join(cwd, departament_dir)

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error creating departament', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error creating departament'}), returned_code
        else:
            return jsonify({'id': departament_id, 'success': True, 'message': 'Departament Created successfully!'}), returned_code


    return app