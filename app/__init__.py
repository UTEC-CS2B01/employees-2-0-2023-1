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
    

    @app.route('/employees', methods=['GET','POST', 'PATCH', 'DELETE'])
    def create_employee():
        if request.method == 'GET':
            search_query = request.args.get('search','')

            if search_query:
                employee = Employee.query.filter(
                    db.or_(
                        Employee.firstname.ilike(f'%{search_query}%'),
                        Employee.lastname.ilike(f'%{search_query}%')
                    )
                ).all()
                if employee:
                    serialized_employees = [emp.serialize() for emp in employee]
                    return jsonify(serialized_employees), 200
                else:
                    return jsonify({'success':False, 'message': 'employee not found'}),400

            employees = Employee.query.all()
            return jsonify([employe.serialize() for employe in employees]), 200
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
        
        if request.method == 'PATCH':
            returned_code = 200
            body = request.form

            if 'id' not in body:
                returned_code = 400
                return jsonify({'success': False, 'message': 'You need an id to update employee data'}), returned_code

            employee = Employee.query.filter_by(id=request.form['id']).first()

            if employee:
                try:
                    if 'firstname' in body:
                        employee.firstname = request.form['firstname']

                    if 'lastname' in body:
                        employee.lastname = request.form['lastname']  

                    if 'age' in body:
                        employee.age = request.form['age'] 

                    if 'selectDepartment'in body:
                        employee.department_id = request.form['selectDepartment']

                    if 'image' in request.files:
                
                        file = request.files['image']

                        if file.filename == '':
                            return jsonify({'success': False, 'message': 'No image selected'}), 400
                
                        if not allowed_file(file.filename):
                            return jsonify({'success': False, 'message': 'Image format not allowed'}), 400

                        cwd = os.getcwd()

                        employee_dir = os.path.join(app.config['UPLOAD_FOLDER'], employee.id)
                        os.makedirs(employee_dir, exist_ok=True)

                        upload_folder = os.path.join(cwd, employee_dir)

                        file.save(os.path.join(upload_folder, file.filename))

                        employee.image = file.filename
                        db.session.commit()
                    
                    db.session.commit()
                    employee_id = employee.id

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
                    return jsonify({'id': employee_id, 'success': True, 'message': 'Employee updated successfully!'}), returned_code

            else:
                returned_code = 400
                return jsonify({'success':False, 'message':'Id not found'}), returned_code

        if request.method == 'DELETE':
            returned_code = 200
            body = request.form

            if 'id' not in body:
                returned_code = 400
                return jsonify({'success': False, 'message': 'You need an id to delete an employee'}), returned_code

            employee = Employee.query.filter_by(id=request.form['id']).first()
            if employee:
                try:
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
            else:
                returned_code = 400
                return jsonify({'success':False, 'message':'Id not found'}), returned_code            

    @app.route('/department', methods=['GET','POST', 'PATCH', 'DELETE'])
    def create_department():
        returned_code = 200

        if request.method == 'GET':
            
            search_query = request.args.get('search','')

            if search_query:
                department = Department.query.filter(
                    db.or_(
                        Department.name.ilike(f'%{search_query}%'),
                        Department.short_name.ilike(f'%{search_query}%')
                    )
                ).all()
                if department:
                    serialized_departments = [dep.serialize() for dep in department]
                    return jsonify(serialized_departments), 200
                else:
                    return jsonify({'success':False, 'message': 'Department not found'}),400

            try:
                departments = Department.query.all()
                departments_serialized = [department.serialize() for department in departments]
                return jsonify({'success': True, 'departments': departments_serialized}), returned_code
            except Exception as e:
                return jsonify({'success': False, 'message':'No departments found'}),400
            
        if request.method == 'POST':
            list_errors = []
            dp_id = ''
            try:
                body = request.form
                
                if 'name' not in body:
                    list_errors.append('name is required')
                else:
                    name = request.form.get('name')

                if 'short_name' not in body:
                    list_errors.append('shortname is required')
                else:
                    short_name = request.form['short_name']

                if len(list_errors) > 0:
                    returned_code = 400
                else:
                    department = Department(name, short_name)
                    db.session.add(department)
                    dp_id = department.id
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
                return jsonify({'id': dp_id, 'success': True, 'message': 'Employee Created successfully!'}), returned_code

        if request.method == 'PATCH':
            body = request.form

            if 'id' not in body:
                returned_code = 400
                return jsonify({'success': False, 'message': 'You need an id to update department data'}), returned_code

            department = Department.query.filter_by(id=request.form['id']).first()

            if department:
                try:
                    if 'name' in body:
                        department.name = request.form['name']

                    if 'short_name' in body:
                        department.short_name = request.form['short_name']  
                    
                    db.session.commit()

                    department_id = department.id

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
                    return jsonify({'id': department_id, 'success': True, 'message': 'Department updated successfully!'}), returned_code

            else:
                returned_code = 400
                return jsonify({'success':False, 'message':'Department id not found'}), returned_code

        if request.method == 'DELETE':
            body = request.form

            if 'id' not in body:
                returned_code = 400
                return jsonify({'success': False, 'message': 'You need an id to delete a department'}), returned_code

            department = Department.query.filter_by(id=request.form['id']).first()
            if department:
                try:
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
            else:
                returned_code = 400
                return jsonify({'success':False, 'message':'Department id not found'}), returned_code  



    @app.route('/employees/<id>', methods=['GET','PATCH', 'DELETE'])
    def employee_id():
        if request.method == 'GET':
            return 0
        if request.method == 'PATCH':
            return 0
        if request.method == 'DELETE':
            return 0
    return app
    