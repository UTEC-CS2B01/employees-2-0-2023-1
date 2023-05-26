from flask import (
    Flask,
    request,
    jsonify,
    abort,
)
from .models import db, setup_db, Employee, Department
from .utils.utilities import allowed_file
from flask_cors import CORS
import os
import sys

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'static/employees'
    with app.app_context():
        setup_db(app)
        CORS(app, origins='*')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Max-Age', '15')
        return response
    
    @app.route('/employees', methods=['POST'])
    def create_employee():
        error_code = 200
        list_errors = []
        try:
            body = request.form

            if 'first_name' not in body:
                list_errors.append('first_name is required')
            else:
                first_name = request.form.get('first_name')

            if 'last_name' not in body:
                list_errors.append('last_name is required')
            else:
                last_name = request.form.get('last_name')

            if 'job_title' not in body:
                list_errors.append('job_title is required')
            else:
                job_title = request.form.get('job_title')

            if 'selectDepartment' not in body:
                list_errors.append('selectDepartment is required')
            else:
                department_id = request.form.get('selectDepartment')

            if 'image' not in request.files:
                print('image is required')
                list_errors.append('image is required')
            else:
                file = request.files['image']

                if file.filename == '':
                    list_errors.append('filename should not be empty')
                
                if not allowed_file(file.filename):
                    list_errors.append('File extension not allowed')
            

            if len(list_errors) > 0:
                error_code = 400
            else:
                employee = Employee(first_name, last_name, job_title, department_id)
                db.session.add(employee)
                db.session.commit()
                employeeid_created = employee.id
                
                cwd = os.getcwd()

                employee_dir = os.path.join(app.config['UPLOAD_FOLDER'], employee.id)
                os.makedirs(employee_dir, exist_ok=True)

                upload_folder = os.path.join(cwd, employee_dir)

                absolute_path = os.path.join(upload_folder, file.filename)
                file.save(absolute_path)
                file.close()

                relative_path = os.path.join(employee_dir, file.filename)

                employee.image_path = relative_path
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("e: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            error_code = 500

        if error_code == 400:
            return jsonify({'success': False, 'message': 'Error creating employee', 'errors': list_errors}), error_code
        elif error_code == 500:
            return jsonify({'success': False, 'message': 'Internal Server Error'}), error_code
        else:
            return jsonify({'success': True, 'id': employeeid_created, 'message': 'Employee created successfully'}), 201

    @app.route('/employees', methods=['GET'])
    def get_employees():
        
        try:
            search_query = request.args.get('query', None)
            if search_query:
                employees = Employee.query.filter_by(is_active=True).filter(Employee.first_name.ilike('%{}%'.format(search_query)))\
                    .order_by(Employee.first_name).all()
                
                return jsonify({'success': True, 'employees': [e.serialize() for e in employees], 'total': len(employees)}), 200

            employees = Employee.query.filter_by(is_active=True).order_by(Employee.first_name).all()
            return jsonify({'success': True, 'employees': [e.serialize() for e in employees]}), 200
        except Exception as e:
            print("e: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Internal Server Error'}), 500

    @app.route('/employees/<id>', methods=['PATCH'])
    def update_employee(id):
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({'success':False,'message': 'Empleado no encontrado'}), 404

        data = request.form

        if 'first_name' in data:
            employee.first_name = data['first_name']
        if 'last_name' in data:
            employee.last_name = data['last_name']
        if 'job_title' in data:
            employee.job_title = data['job_title']
        if 'selectDepartment' in data:
            employee.department_id = data['selectDepartment']
        db.session.commit()
        db.session.close()

        return jsonify({'success':True,'message': 'Empleado actualizado correctamente'}), 200

    @app.route('/employees/<id>', methods=['DELETE'])
    def delete_employee(id):
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({'success':False,'message': 'Empleado no encontrado'}), 404

        employee.is_active = False
        db.session.commit()
        db.session.close()

        return jsonify({'success':True,'message': 'Empleado eliminado correctamente'}), 200
    
    @app.route('/employees/search', methods=['GET'])
    def search_employees():
        if request.method == 'GET':
            search_query = request.args.get('q')

            # Realiza la búsqueda de empleados en función del query de búsqueda
            employees = Employee.query.filter(Employee.firstname.ilike(f'%{search_query}%') |
                                            Employee.lastname.ilike(f'%{search_query}%')).all()

            serialized_employees = [employee.serialize() for employee in employees]

            return jsonify(serialized_employees), 200

    @app.route('/departments', methods=['GET'])
    def get_departments():
        try:
            search_query = request.args.get('query', None)
            if search_query:
                departments = Department.query.filter(
                    db.or_(Department.name.ilike('%{}%'.format(search_query)),
                            Department.short_name.ilike('%{}%'.format(search_query)))    
                ).all()

                return jsonify({'success': True, 'departments': [d.serialize() for d in departments], 'total': len(departments)}), 200

            departments = Department.query.order_by(Department.short_name).all()
            return jsonify({'success': True, 'departments': [d.serialize() for d in departments]}), 200


        except Exception as e:
            print("e: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Internal Server Error'}), 500
             
        
    @app.route('/departments', methods=['POST'])
    def create_department():
        error_code = 200
        list_errors = []
        try:
            body = request.form

            if 'name' not in body:
                list_errors.append('name is required')
            else:
                name = body.get('name')

            if 'short_name' not in body:
                list_errors.append('short_name is required')
            else:
                short_name = body.get('short_name')

            if len(list_errors) > 0:
                error_code = 400
            else:
                department = Department(name, short_name)
                db.session.add(department)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("e: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            error_code = 500

        
        if error_code == 400:
            return jsonify({'success': False, 'message': 'Error creating department', 'errors': list_errors}), error_code
        elif error_code == 500:
            return jsonify({'success': False, 'message': 'Internal Server Error'}), error_code
        else:
            return jsonify({'success': True, 'id': department.id, 'name':department.name, 'short_name':department.short_name ,'message': 'Department created successfully'}), 201

    @app.route('/departments/<id>', methods=['PATCH'])
    def update_department(id):
        department = Department.query.get(id)

        if not department:
            return jsonify({'message': 'Departamento no encontrado'}), 404

        data = request.form

        if 'name' in data:
            department.name = data['name']
        if 'short_name' in data:
            department.short_name = data['short_name']
        db.session.commit()
        db.session.close()

        return jsonify({'success': True, 'message': 'Departamento actualizado exitosamente'})
    
    @app.route('/departments/<id>', methods=['DELETE'])
    def delete_department(id):
        department = Department.query.get(id)

        if not department:
            return jsonify({'message': 'Departamento no encontrado'}), 404

        db.session.delete(department)
        db.session.commit()
        db.session.close()

        return jsonify({'success': True,'message': 'Departamento eliminado exitosamente'})
    
    @app.route('/departments/search', methods=['GET'])
    def search_departments():
        if request.method == 'GET':
            search_query = request.args.get('q')

            # Realiza la búsqueda de departamentos en función del query de búsqueda
            departments = Department.query.filter(Department.name.ilike(f'%{search_query}%') |
                                                Department.short_name.ilike(f'%{search_query}%')).all()

            serialized_departments = [department.serialize() for department in departments]

            return jsonify(serialized_departments), 200

    return app
