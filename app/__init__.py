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
    #
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        #response.headers.add('Acces')
        return response
    
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
                        'id_employee': employee.id
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
            return jsonify({'employees':employee_list, 'success': True}), returned_code

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

    @app.route('/employees/<employee_id>', methods=['PATCH'])
    def update_employee(employee_id):
        returned_code = 200
        list_errors = []
        try:
            employee = Employee.query.get(employee_id)

            if employee is None:
                list_errors.append('employee dont exist')
                returned_code = 404
            else:
                body = request.form

                if 'newage' not in body:
                    list_errors.append('newage is required')
                else:
                    employee.age = request.form['newage']    
                if 'newselectDepartment' not in body:
                    list_errors.append('newdepartment is required')
                else:
                    employee.department_id = request.form['newselectDepartment']
                if 'newimage' not in request.files:
                    list_errors.append('newimage is required')
                else:
                    file = request.files['newimage']

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
        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()
        if len(list_errors)>0:
            return jsonify({'success': False, 'message': 'Error updating employee', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error updating employee'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Employee updated successfully!'}), returned_code        

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
            return jsonify({'departments':department_list, 'success': True}), returned_code
    
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
    def update_department(department_id):
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

    @app.route('/employees/<employee_id>/department', methods=['GET'])
    def get_employee_departments(employee_id):
        returned_code = 200
        list_errors = []
        try:
            employee = Employee.query.get(employee_id)
            
            if employee is None:
                list_errors.append('employee dont exist')
                returned_code = 404
            else:
                department = Department.query.get(employee.department_id)
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
        finally:
            db.session.close()
        if len(list_errors) > 0:
            return jsonify({'success': False, 'message': 'Error getting employee department', 'errors': list_errors}), returned_code 
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error getting employee department'}), returned_code
        else:
            return jsonify({'employee':employee.firstname,'department': department.name, 'success': True}), returned_code                  

    @app.route('/departments/<department_id>/employees', methods=['GET'])
    def get_department_employees(department_id):
        returned_code = 200
        list_errors = []
        try:
            department = Department.query.get(department_id)
            
            if department is None:
                list_errors.append('department dont exist')
                returned_code = 404
            else:
                employees = Employee.query.filter_by(department_id=department_id).all()
                if len(employees) == 0:
                    list_errors.append('no employees found')
                    returned_code = 404
                else: 
                    employee_list = []
                    for employee in employees:
                        employee_list.append({
                            'id': employee.id,
                            'firstname': employee.firstname,
                            'lastname': employee.lastname,
                        })
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
        finally:
            db.session.close()
        if len(list_errors) > 0:
            return jsonify({'success': False, 'message': 'Error getting department employees', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error getting department employees'}), returned_code
        else:
            return jsonify({'employees':employee_list, 'success': True}), returned_code

    @app.route('/employees/search', methods=['GET'])
    def search_employees():
        returned_code = 200
        list_errors = []
        try:
            search_query_firstname = request.args.get('firstname')
            search_query_lastname = request.args.get('lastname')
            search_query_age = request.args.get('age')

            filters = []

            if search_query_firstname:
                filters.append(Employee.firstname.ilike(f'%{search_query_firstname}%'))

            if search_query_lastname:
                filters.append(Employee.lastname.ilike(f'%{search_query_lastname}%'))

            if search_query_age:
                filters.append(Employee.age == search_query_age)

            if not filters:
                list_errors.append('at least one search query is required')
                returned_code = 400
            
            employees = Employee.query.filter(*filters).all()

            if len(employees) == 0:
                list_errors.append('no employee found')
                returned_code = 404
            else:
                employee_list = []
                for employee in employees:
                    employee_list.append({
                        'id': employee.id,
                        'firstname': employee.firstname,
                        'lastname': employee.lastname,
                    })

        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
        finally:
            db.session.close()

        if len(list_errors) > 0:
            return jsonify({'success': False, 'message': 'Error searching employees', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error searching employees'}), returned_code
        else: 
            return jsonify({'employees':employee_list, 'success':True}), returned_code 
    
    @app.route('/departments/search', methods=['GET'])
    def search_departments():
        returned_code = 200
        list_errors = []
        try:
            search_query_name = request.args.get('name')
            search_query_short_name = request.args.get('short_name')

            filters = []

            if search_query_name:
                filters.append(Department.name.ilike(f'%{search_query_name}%'))

            if search_query_short_name:
                filters.append(Department.short_name.ilike(f'%{search_query_short_name}%'))

            if not filters:
                list_errors.append('at least one search query is required')
                returned_code = 400


            departments = Department.query.filter(*filters).all()

            if len(departments) == 0:
                list_errors.append('no department found')
                returned_code = 404
            else:
                department_list = []
                for department in departments:
                    department_list.append({
                        'id': department.id,
                        'name': department.name,
                        'short_name': department.short_name,
                    })

        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
        finally:
            db.session.close()

        if len(list_errors) > 0:
            return jsonify({'success': False, 'message': 'Error searching departments', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error searching departments'}), returned_code
        else: 
            return jsonify({'departments':department_list, 'success':True}), returned_code
    
    return app