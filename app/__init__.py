from flask import (
    Flask,
    request,
    jsonify
)
from models import db, setup_db, Employee, Department
from flask_cors import CORS
from utilities import allowed_file
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
    

    @app.route('/employees', methods=['GET','POST', 'PATCH', 'DELETE'])
    def create_employee():
        if request.method == 'GET':
            employees = Employee.query.filter_by(is_active=True).all()
            employees = [employee.serialize() for employee in employees]
            return jsonify({'success': True, 'employees': employees}), 200
        
        if request.method == 'POST':
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
    
    @app.route('/departaments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    def create_departament():
        if request.method == 'GET':
            try:
                departaments = Department.query.all()
                departaments = [departament.format() for departament in departaments]
                return jsonify({'success': True, 'departaments': departaments}), 200
            except Exception as e:
                print(e)
                print(sys.exc_info())
                db.session.rollback()
                return jsonify({'success': False, 'message': 'Error obtener departaments'}), 500
            finally:
                db.session.close()

        if request.method == 'POST':
            returned_code = 200
            list_errors = []

            try:
                body = request.form

                if 'name' not in body:
                    list_errors.append('name is required')
                else:
                    name = request.form.get('name')

                if 'short_name' not in body:
                    list_errors.append('short name is required')
                else:
                    short_name = request.form.get('short_name')

                if len(list_errors) > 0:
                    returned_code = 400
                else:
                    departament = Department(name, short_name)
                    db.session.add(departament)
                    db.session.commit()

                    departament_id = departament.id

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

        if request.method == 'PATCH':
            new_name = request.json.get('name')
            new_short_name = request.json.get('short_name')

            try:
                departments = Department.query.all()
                for department in departments:
                    if new_name is not None:
                        department.name = new_name
                        department.modified_at = datetime.utcnow()
                    if new_short_name is not None:
                        department.short_name = new_short_name
                        department.modified_at = datetime.utcnow()

                db.session.commit()

                return jsonify({'message': 'Departments updated successfully'})

            except Exception as e:
                print(e)
                print(sys.exc_info())
                db.session.rollback()
                return jsonify({'success': False, 'message': 'Error updating departaments'}), 500

            finally:
                db.session.close()

        if request.method == 'DELETE':
            try:
                departments = Department.query.all()
                for department in departments:
                    db.session.delete(department)

                db.session.commit()

                return jsonify({'message': 'Departments deleted successfully'})

            except Exception as e:
                print(e)
                print(sys.exc_info())
                db.session.rollback()
                return jsonify({'success': False, 'message': 'Error deleting departaments'}), 500

            finally:
                db.session.close()
        
            

        
    return app