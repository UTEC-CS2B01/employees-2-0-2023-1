from flask import (
    Flask,
    request,
    jsonify,
    abort
)
from .models import db, setup_db, Employee, Department, File
from flask_cors import CORS
from .utilities import allowed_file

import os
import sys
app = Flask(__name__)

def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        app.config['UPLOAD_FOLDER'] = 'static/employees'
        setup_db(app, test_config['database_path'] if test_config else None)
        CORS(app, origins='*')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add(' Access-Control-Max-Age', '10')
        return response
    
    # Post
    #########################################################

    @app.route('/employees', methods=['POST'])
    def create_employee():
        returned_code = 201
        list_errors = []
        try:
            body = request.json

            if 'firstname' not in body:
                list_errors.append('firstname is required')
            else:
                firstname = body.get('firstname')

            if 'lastname' not in body:
                list_errors.append('lastname is required')    
            else:
                lastname = body['lastname']

            if 'age' not in body:
                list_errors.append('age is required')    
            else:
                age = body['age']

            if 'selectDepartment' not in body:
                list_errors.append('department is required')
            else:
                department_id = body['selectDepartment']

            if len(list_errors) > 0:
                returned_code = 400
            else:
                employee = Employee(firstname, lastname, age, department_id)
                db.session.add(employee)
                db.session.commit()

                employee_id = employee.id

        except Exception as e:
        
            # print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error creating employee', 'errors': list_errors}), returned_code
        elif returned_code != 201:
            abort(returned_code)
        else:
            return jsonify({'id': employee_id, 'success': True, 'message': 'Employee Created successfully!'}), returned_code
    

    @app.route('/files', methods=['POST'])
    def upload_image():
        returned_code = 201
        list_errors = []
        try:
            if 'employee_id' not in request.form:
                list_errors.append('employee_id is required')
            else:
                employee_id = request.form['employee_id']

            if 'image' not in request.files:
                list_errors.append('image is required')
            else:
                file = request.files['image']

                if not allowed_file(file.filename):
                    return jsonify({'success': False, 'message': 'Image format not allowed'}), 400

            if len(list_errors) > 0:
                returned_code = 400
            else:

                cwd = os.getcwd()

                employee_dir = os.path.join(app.config['UPLOAD_FOLDER'], employee_id)
                os.makedirs(employee_dir, exist_ok=True)

                upload_folder = os.path.join(cwd, employee_dir)

                file.save(os.path.join(upload_folder, file.filename))
                
                file = File(file.filename, employee_id)

                db.session.add(file)
                db.session.commit()

        except Exception as e:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error uploading file', 'errors': list_errors}), returned_code
        elif returned_code != 201:
            abort(returned_code)
        else:
            return jsonify({'success': True, 'message': 'File uploaded successfully!'}), returned_code


    @app.route('/departments', methods=['POST'])
    def create_department():
        returned_code = 201
        list_errors = []
        try:
            body = request.json

            if 'name' not in body:
                list_errors.append('name is required')
            else:
                name = request.json['name']

            if 'short_name' not in body:
                list_errors.append('short_name is required')
            else:
                short_name = request.json['short_name']

            if len(list_errors) > 0:
                returned_code = 400
            else:
                department = Department(name, short_name)
                db.session.add(department)
                db.session.commit()

                department_id = department.id

        except Exception as e:
            # print('error: ', e)
            # print('exc_info: ',sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error creating department', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            abort(returned_code)
        else:
            return jsonify({'id': department_id, 'success': True, 'message': 'Department created successfully!'}), returned_code
        
    # GET
    #######################################################################################
    
    @app.route('/employees', methods=['GET'])
    def get_employees():
        returned_code = 200
        error_message = ''
        employee_list = []

        try:
            search_query = request.args.get('search', None)
            if search_query:
                employees = Employee.query.filter(Employee.firstname.like('%{}%'.format(search_query))).all()

                employees_list = [employee.serialize() for employee in employees]

            else:
                employees = Employee.query.all()
                employee_list = [employee.serialize() for employee in employees]

            if not employee_list:
                returned_code = 404
                error_message = 'No employees found'

        except Exception as e:
        
            # print(sys.exc_info())
            returned_code = 500
            error_message = 'Error retrieving employees'

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'data': employee_list}), returned_code
    
    # PATCH
    ###########################################################################################
    
    @app.route('/departments/<department_id>', methods=['PATCH'])
    def update_department(department_id):
        returned_code = 200
        
        try:
            department = Department.query.filter_by(id=department_id).first()

            if not department:
                returned_code = 404
            else:
                body = request.json

                if 'name' in body:
                    department.name = body['name']

                if 'short_name' in body:
                    department.short_name = body['short_name']

                db.session.commit()

        except Exception as e:
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code != 200:
            abort(returned_code)

        return jsonify({'success': True, 'message': 'Department updated successfully'}), returned_code
    
    # DELETE
    ########################################################################################
    
    @app.route('/departments/<department_id>', methods=['DELETE'])
    def delete_department(department_id):
        returned_code = 200
        error_message = ''

        try:
            department = Department.query.filter_by(id=department_id).first()

            if not department:
                returned_code = 404
            else:
                db.session.delete(department)
                db.session.commit()

        except Exception as e:
        
            # print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code != 200:
            abort(returned_code)

        return jsonify({'success': True, 'message': 'Department deleted successfully'}), returned_code


    @app.route('/employees/<employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        returned_code = 200
        error_message = ''

        try:
            employee = Employee.query.filter_by(id=employee_id).first()

            if not employee:
                returned_code = 404
            else:
                db.session.delete(employee)
                db.session.commit()

        except Exception as e:
        
            # print(sys.exc_info())
            db.session.rollback()
            returned_code = 500

        finally:
            db.session.close()

        if returned_code != 200:
            abort(returned_code)

        return jsonify({'success': True, 'message': 'Employee deleted successfully'}), returned_code

    

    @app.route('/employees/<employee_id>', methods=['PATCH'])
    def update_employee(employee_id):
        returned_code = 200
        list_errors = []
        try:
            employee = Employee.query.filter_by(id=employee_id).first()

            if employee is None:
                list_errors.append('employee does not exist')
                returned_code = 404
            else:
                body = request.form

                if 'age' not in body:
                    list_errors.append('age is required')
                else:
                    employee.age = request.form['age']    

                if 'selectDepartment' not in body:
                    list_errors.append('selectDepartment is required')
                else:
                    employee.department_id = request.form['selectDepartment']

                if 'image' not in request.files:
                    list_errors.append('image is required')
                else:
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
        except Exception as e:
        
            # print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()
        if len(list_errors) > 0:
            returned_code = 400
            return jsonify({'success': False, 'message': 'Error updating employee', 'errors': list_errors}), returned_code
        elif returned_code != 200:
            abort(returned_code)
        else:
            return jsonify({'success': True, 'message': 'Employee updated successfully!'}), returned_code        

    @app.route('/departments', methods=['GET'])
    def get_departments():
        returned_code = 200
        department_list = []

        try:
            search_query = request.args.get('search', None)  
            if search_query:
                departments = Department.query.filter(
                    db.or_(
                        Department.name.ilike(f'%{search_query}%'),
                        Department.short_name.ilike(f'%{search_query}%')
                    )
                ).all()
                serialized_departments = [department.serialize() for department in departments]

                return jsonify({'success': True, 'departments': serialized_departments, \
                                'total': len(serialized_departments)}), returned_code



            departments = Department.query.all()
            department_list = [department.serialize() for department in departments]

            if not department_list:
                returned_code = 404
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500

        if returned_code != 200:
            abort(returned_code)

        return jsonify({'success': True, 'data': department_list}), returned_code                 

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
                # como un empleado solo tiene un departamento
                department = Department.query.get(employee.department_id)
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
        finally:
            db.session.close()
        if len(list_errors) > 0:
            return jsonify({'success': False, 'message': 'Error getting employee department', 'errors': list_errors}), returned_code 
        elif returned_code != 200:
            abort(returned_code)
        
        
        return jsonify({'employee':employee.firstname,'department': department.name, 'success': True}), returned_code                  

    @app.route('/departments/<department_id>/employees', methods=['GET'])
    def get_department_employees(department_id):
        returned_code = 200
        list_errors = []
        try:
            department = Department.query.get(department_id)
            
            if department is None:
                list_errors.append('department does not exist')
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
        elif returned_code != 200:
            abort(returned_code)
        else:
            return jsonify({'employees': employee_list, 'success': True}), returned_code

    @app.route('/employees/search', methods=['GET'])
    def search_employees():
        returned_code = 200
        list_errors = []
        try:
            # Obtener los parámetros de la solicitud GET
            search_query_firstname = request.args.get('firstname')
            search_query_lastname = request.args.get('lastname')
            search_query_age = request.args.get('age')

            # Crear una lista de filtros vacía
            filters = []

            # Agregar filtros a la lista si se proporcionan los parámetros correspondientes
            if search_query_firstname:
                filters.append(Employee.firstname.ilike(f'%{search_query_firstname}%'))

            if search_query_lastname:
                filters.append(Employee.lastname.ilike(f'%{search_query_lastname}%'))

            if search_query_age:
                filters.append(Employee.age == search_query_age)

            # Verificar si se proporcionó al menos un parámetro de búsqueda
            if not filters:
                list_errors.append('at least one search query is required')
                returned_code = 400

            # Realizar la consulta a la base de datos utilizando los filtros
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
        elif returned_code != 200:
            abort(returned_code)
        else: 
            return jsonify({'employees':employee_list, 'success':True}), returned_code 

    @app.route('/departments/search', methods=['GET'])
    def search_departments():
        returned_code = 200
        list_errors = []
        try:
            # Obtener los parámetros de la solicitud GET
            # se busca por los URL query parameters
            search_query_name = request.args.get('name')
            search_query_short_name = request.args.get('short_name')

            # Crear una lista de filtros vacía
            filters = []

            # Agregar filtros a la lista si se proporcionan los parámetros correspondientes
            if search_query_name:
                filters.append(Department.name.ilike(f'%{search_query_name}%'))

            if search_query_short_name:
                filters.append(Department.short_name.ilike(f'%{search_query_short_name}%'))

            # Verificar si se proporcionó al menos un parámetro de búsqueda
            if not filters:
                list_errors.append('at least one search query is required')
                returned_code = 400

            # Realizar la consulta a la base de datos utilizando los filtros
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
        elif returned_code != 200:
            abort(returned_code)
        else: 
            return jsonify({'departments':department_list, 'success':True}), returned_code 
        

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Method not allowed'
        }), 405   

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }) 
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal Server error'
        }), 500
    

    return app

