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
        response.headers.add(' Access-Control-Max-Age', '10')
        return response
    
# Post
#########################################################

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
        
                file = request.files['image']

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
        

# GET
#######################################################################################
    
    @app.route('/departments', methods=['GET'])
    def get_departments():
        returned_code = 200
        error_message = ''
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
                error_message = 'No departments found'
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
            error_message = 'Error retrieving departments'

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'data': department_list}), returned_code



    @app.route('/employees', methods=['GET'])
    def get_employees():
        returned_code = 200
        error_message = ''
        employee_list = []

        try:
            search_query = request.args.get('search', None)
            if search_query:
                employees = Employee.query.filter(Employee.firstname.like('%{}%'.format(search_query))).all()

                serialized_employees = [employee.serialize() for employee in employees]

                return jsonify({'employees': serialized_employees}), returned_code


            employees = Employee.query.all()
            employee_list = [employee.serialize() for employee in employees]

            if not employee_list:
                returned_code = 404
                error_message = 'No employees found'
        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
            error_message = 'Error retrieving employees'

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'data': employee_list}), returned_code
    
    
    # PATCH
    ###########################################################################################
    
    
    @app.route('/employees/<employee_id>', methods=['PATCH'])
    def update_employee(employee_id):
        returned_code = 200
        error_message = ''

        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                returned_code = 404
                error_message = 'Employee not found'
            else:
                body = request.form

                if 'firstname' in body:
                    employee.firstname = request.form['firstname']

                if 'lastname' in body:
                    employee.lastname = request.form['lastname']

                if 'age' in body:
                    employee.age = request.form['age']

                print(request.form['is_active'])
                if 'is_active' in body:
                    employee.is_active = True if request.form['is_active'] == 'true' else False

                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error updating employee'

        finally:
            db.session.close()

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'message': 'Employee updated successfully'}), returned_code
    
    
    
    @app.route('/departments/<department_id>', methods=['PATCH'])
    def update_department(department_id):
        returned_code = 200
        error_message = ''

        try:
            department = Department.query.get(department_id)

            if not department:
                returned_code = 404
                error_message = 'Department not found'
            else:
                body = request.form

                if 'name' in body:
                    department.name = request.form['name']

                if 'short_name' in body:
                    department.short_name = request.form['short_name']

                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error updating department'

        finally:
            db.session.close()

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'message': 'Department updated successfully'}), returned_code
    
    
    # DELETE
    ########################################################################################
    
    @app.route('/departments/<department_id>', methods=['DELETE'])
    def delete_department(department_id):
        returned_code = 200
        error_message = ''

        try:
            department = Department.query.get(department_id)

            if not department:
                returned_code = 404
                error_message = 'Department not found'
            else:
                db.session.delete(department)
                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error deleting department'

        finally:
            db.session.close()

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'message': 'Department deleted successfully'}), returned_code



    @app.route('/employees/<employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        returned_code = 200
        error_message = ''

        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                returned_code = 404
                error_message = 'Employee not found'
            else:
                db.session.delete(employee)
                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error deleting employee'

        finally:
            db.session.close()

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'message': 'Employee deleted successfully'}), returned_code


# /employees/<employee_id>/departments
###########################################################################################
    
    # POST Method
    @app.route('/employees/<employee_id>/departments', methods=['POST'])
    def assign_employee_department(employee_id):
        returned_code = 200
        error_message = ''

        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                returned_code = 404
                error_message = 'Employee not found'
            else:
                body = request.form

                if 'name' not in body:
                    returned_code = 400
                    error_message = 'Department name is required'
                elif 'short_name' not in body:
                    returned_code = 400
                    error_message = 'Department short_name is required'
                else:
                    name = request.form['name']
                    short_name = request.form['short_name']

                    department = Department(name, short_name)
                    department.employees.append(employee)

                    db.session.add(department)
                    db.session.commit()

                    department_id = department.id

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error assigning department to employee'

        finally:
            db.session.close()

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'department_id': department_id, 'message': 'Department assigned to employee successfully!'}), returned_code


    # GET Method
    @app.route('/employees/<employee_id>/departments', methods=['GET'])
    def get_employee_departments(employee_id):
        returned_code = 200
        error_message = ''

        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                returned_code = 404
                error_message = 'Employee not found'
            else:
                departments = Department.query.filter(Department.employees.any(id=employee_id)).all()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            returned_code = 500
            error_message = 'Error retrieving employee departments'

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        department_list = [department.serialize() for department in departments]
        return jsonify({'success': True, 'departments': department_list}), returned_code


    # PATCH Method
    @app.route('/employees/<employee_id>/departments', methods=['PATCH'])
    def update_employee_departments(employee_id):
        returned_code = 200
        error_message = ''

        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                returned_code = 404
                error_message = 'Employee not found'
            else:
                body = request.form

                if 'department_id' not in body:
                    returned_code = 400
                    error_message = 'Department ID is required'
                else:
                    department_id = request.form['department_id']
                    department = Department.query.get(department_id)

                    if not department:
                        returned_code = 404
                        error_message = 'Department not found'
                    else:
                        department.employees.append(employee)

                        db.session.add(department)
                        db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error updating employee departments'

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'message': 'Employee departments updated successfully!'}), returned_code


    # DELETE Method
    @app.route('/employees/<employee_id>/departments', methods=['DELETE'])
    def remove_employee_departments(employee_id):
        returned_code = 200
        error_message = ''

        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                returned_code = 404
                error_message = 'Employee not found'
            else:
                departments = Department.query.filter(Department.employees.any(id=employee_id)).all()

                for department in departments:
                    department.employees.remove(employee)

                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            returned_code = 500
            error_message = 'Error removing employee departments'

        if returned_code != 200:
            return jsonify({'success': False, 'message': error_message}), returned_code

        return jsonify({'success': True, 'message': 'Employee departments removed successfully!'}), returned_code

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
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error searching employees'}), returned_code
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
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error searching departments'}), returned_code
        else: 
            return jsonify({'departments':department_list, 'success':True}), returned_code 
    
    return app

