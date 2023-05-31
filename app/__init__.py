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
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', '10')
        return response

    # Employees

    # POST
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

                employee_dir = os.path.join(
                    app.config['UPLOAD_FOLDER'], employee.id)
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

    # GET
    @app.route('/employees', methods=['GET'])
    def getEmployees():
        return_code = 200
        error_List = []
        employees_list = []

        try:
            search = request.args.get("search")
            body = request.headers.get('Content-Type')
            employees = [b.serialize() for b in db.view()]
            if search is not None:
                employees_filter = Employee.query.filter_by(db.or_(
                    Employee.name.ilike(f"{search}"),
                    Employee.lastname.ilike(f"{search}")
                ))

                employees_list = [e for e in employees_filter]


            else:
                if (body == 'application/json'):
                    json = request.json
                    for e in employees:
                        if (e['id'] == json['id']):
                            return_code = 200
                        else:
                            return_code = 400
                            error_List.append(
                                f"Could not find employee with id: {json['id']}")

                else:
                    return_code = 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500

        finally:
            db.session.close()

            if return_code == 500:
                return jsonify({'success': False, 'message': 'Error retrieving employees', 'errors': error_List}), return_code
            elif return_code == 400:
                return jsonify({'success': False, 'message': 'Error retrieving employees', 'errors': error_List}), return_code
            else:
                return jsonify({'success': True, 'message': 'Employees retrieved succesfully', 'data': employees_list.serialize()}), return_code

    # PATCH
    @app.route('/employees/<_id>', methods=['PATCH'])
    def patch_employee(_id):
        return_code = 200
        errorList = []
        body = request.get_json()
        try:
            employee = Employee.query.filter_by(id=_id).first()

            if employee is None:
                return_code = 400
                errorList.append(f'Could not find employee with id: {_id}')
            else:
                if 'name' in body:
                    employee.name = body.get('name')

                if 'lastname' in body:
                    employee.lastname = body.get('lastname')

                if 'age' in body:
                    employee.age = body.get('age')

                if 'image' in body and not (allowed_file(image)):
                    return_code = 400
                    errorList.append("Image file type not allowed")
                else:
                    image = body.get('image')
                    db.session.commit()
                    cwd = os.getcwd()
                    employee_dir = os.path.join(
                        app.config['UPLOAD_FOLDER'], employee.id)
                    os.makedirs(employee_dir, exist_ok=True)
                    upload_folder = os.path.join(cwd, employee_dir)
                    image.save(os.path.join(upload_folder, image.filename))
                    employee.image = image.filename

                if 'selectDepartment' in body:
                    employee.department_id = body.get('selectDepartment')

                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500
        finally:
            db.session.close()
            if return_code == 400:
                return jsonify({'success': False, 'message': 'Error updating employee', 'errors': errorList}), return_code
            elif return_code == 500:
                return jsonify({'success': False, 'message': 'Error updating employee'}), return_code
            else:
                return jsonify({'id': employee.id, 'success': True, 'message': 'Employee updated successfully!'}), return_code

    # DELETE
    @app.route('/employee/<_id>', methods=['DELETE'])
    def delete_employee(_id):
        return_code = 200
        errorList = []
        try:
            employee = Employee.query.filter_by(id=_id).first()
            if employee is None:
                return_code = 400
                errorList.append(f'Unable to find employee with id {_id}')
            else:
                n_id = employee.id
                db.session.delete(employee)

            db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500

        finally:
            db.session.close()
            if return_code == 400:
                return jsonify({'success': False, 'message': 'Unable to delete employee', 'errors': errorList}), return_code
            elif return_code == 500:
                return jsonify({'success': False, 'message': 'Unable to delete employee', 'errors': errorList}), return_code
            else:
                return jsonify({'id': n_id, 'success': True, 'message': 'Employee deleted successfully!'}), return_code

    # Departments

    # GET
    @app.route('/departments', methods=['GET'])
    def getDepartments():
        return_code = 200
        error_List = []
        body = request.headers.get('Content-Type')
        departments = [d.serialize() for d in db.view()]
        try:
            if (body == 'application/json'):
                json = request.json
                for d in departments:
                    if (e['id'] == json['id']):
                        return_code = 200
                    else:
                        return_code = 400
                        error_List.append(
                            f"Could not department with name: {json['name']}")

            else:
                return_code = 200

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500

        finally:
            db.session.close()

            if return_code == 500:
                return jsonify({'success': False, 'message': 'Error retrieving departments', 'errors': error_List}), return_code
            elif return_code == 400:
                return jsonify({'success': False, 'message': 'Error retrieving departments', 'errors': error_List}), return_code
            else:
                return jsonify({'success': True, 'message': 'Departments retrieved succesfully'}), return_code

    # PATCH
    @app.route('/departments/<_id>', methods=['PATCH'])
    def patch_department(_id):
        return_code = 200
        errorList = []
        body = request.get_json()
        try:
            department = Department.query.filter_by(id=_id).first()

            if department is None:
                return_code = 400
                errorList.append(f'Could not find department with id: {_id}')
            else:
                if 'name' in body:
                    department.name = body.get('name')

                if 'short_name' in body:
                    department.short_name = body.get('lastname')

                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500
        finally:
            db.session.close()
            if return_code == 400:
                return jsonify({'success': False, 'message': 'Error updating department', 'errors': errorList}), return_code
            elif return_code == 500:
                return jsonify({'success': False, 'message': 'Error updating department'}), return_code
            else:
                return jsonify({'id': department.id, 'success': True, 'message': 'Department updated successfully!'}), return_code

    # DELETE

    @app.route('/department/<_id>', methods=['DELETE'])
    def delete_department(_id):
        return_code = 200
        errorList = []
        try:
            department = Department.query.filter_by(id=_id).first()
            if department is None:
                return_code = 400
                errorList.append(f'Unable to find department with id {_id}')
            else:
                n_id = department.id
                db.session.delete(department)

            db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500

        finally:
            db.session.close()
            if return_code == 400:
                return jsonify({'success': False, 'message': 'Unable to delete department', 'errors': errorList}), return_code
            elif return_code == 500:
                return jsonify({'success': False, 'message': 'Unable to delete department', 'errors': errorList}), return_code
            else:
                return jsonify({'id': n_id, 'success': True, 'message': 'Department deleted successfully!'}), return_code

    # POST
    @app.route('/departments', methods=['POST'])
    def departments():
        return_code = 200
        errorList = []
        body = request.form

        try:
            if 'name' not in body:
                errorList.append("name is required")
            else:
                name = request.form['name']

            if 'short name' not in body:
                errorList.append("short name is required")
            else:
                short_name = request.form["short_name"]

            if len(errorList) != 0:
                return_code = 400
            else:
                department = Department(name, short_name)
                db.session.add(department)
                db.session.commit()

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500

        finally:
            db.session.close()
            if return_code == 400:
                return jsonify({'success': False, 'message': 'Error creating department', 'errors': errorList}), return_code
            elif return_code == 500:
                return jsonify({'success': False, 'message': 'Error creating department', 'errors': errorList}), return_code
            else:
                return jsonify({'name': name, 'success': True, 'message': 'Department created successfully!'}), return_code

    # -------- Search

    # Employees

    @app.route('/search/employees', methods=['GET'])
    def searchEmployee():
        errorList = []
        return_code = 200
        try:
            _name = request.args.get('name')
            employee = Employee.query.filter_by(name=_name)
            if employee == None:
                return_code = 400
                errorList.append(f'No employee with name {_name}')

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500
        finally:
            db.session.close()
            if return_code == 400:
                return jsonify({'success': False, 'message': 'Error finding employee', 'errors': errorList}), return_code
            elif return_code == 500:
                return jsonify({'success': False, 'message': 'Error finding employee', 'errors': errorList}), return_code
            else:
                return jsonify({'name': _name, 'success': True, 'message': 'Employee found successfully!', 'data': employee.serialize()}), return_code

    # Departments

    @app.route('/search/departments', methods=['GET'])
    def searcDepartment():
        errorList = []
        return_code = 200
        try:
            _name = request.args.get('name')
            department = Department.query.filter_by(name=_name)
            if department == None:
                return_code = 400
                errorList.append(f'No department with name {_name}')

        except Exception as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return_code = 500
        finally:
            db.session.close()
            if return_code == 400:
                return jsonify({'success': False, 'message': 'Error finding department', 'errors': errorList}), return_code
            elif return_code == 500:
                return jsonify({'success': False, 'message': 'Error finding department', 'errors': errorList}), return_code
            else:
                return jsonify({'success': True, 'message': 'Department found', 'data': department.serialize()}), return_code

    return app
