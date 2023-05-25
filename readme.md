# Structure Project

- Mantenimiento
  - app/ + **init**.py
  - models.py
  - controller.py
  - service.py
    - confi/
      - local.py
      - qa.py
      - ingtegration.py
      - production.py
  - tests/
    - test_controller.py
    - test_service.py

## Operations

### Create Employee

```
curl -F "firstname=Juan" -F "lastname=perez" -F "age=20" -F "selectDepartment=0cd34425-f007-4b37-9160-bff3fae9cba7" -F "image=@cristiano.jpeg;type=image/jpeg" -X POST "http://127.0.0.1.1:5000/employees"

{
  "id": "27b79c53-edeb-4caf-9bcb-3725669eaa9d",
  "message": "Employee Created successfully!",
  "success": true
}
```

### Errors

```
curl -X POST http://127.0.0.1:5000/employees
{
  "errors": [
    "firstname is required",
    "lastname is required",
    "age is required",
    "selectDepartment is required",
    "image is required"
  ],
  "message": "Error creating employee",
  "success": false
}

```

### Create Department

```
curl -F "name=Departmento de Ventas" -F "short_name=DV" -X POST http://127.0.0.1:5000/departments

{
  "id": "15f1b7a4-3f63-4e2e-b5b2-f4ea02a5b331",
  "message": "Department created successfully!",
  "success": true
}

curl   -X POST http://127.0.0.1:5000/departments
{
  "errors": [
    "name is required",
    "short_name is required"
  ],
  "message": "Error creating department",
  "success": false
}
```

### Patch Employee

```
curl -F "firstname=juan2" -F "lastname=perez2" -F "age=40" -F "is_active=false" -X PATCH http://127.0.0.1:5000/employees/d2064332-6a02-43c8-b8d5-d070979bda4b
{
  "message": "Employee updated successfully",
  "success": true
}
```

### Patch Department

```
curl -F "name=Departmento de Finanzas" -F "short_name=DF" -X PATCH http://127.0.0.1:5000/departments/15f1b7a4-3f63-4e2e-b5b2-f4ea02a5b331
{
  "message": "Department updated successfully",
  "success": true
}
```

### Delete Deparmtent

El departamento no debe tener empleados afiliados.
```
curl -X DELETE http://127.0.0.1:5000/departments/15f1b7a4-3f63-4e2e-b5b2-f4ea02a5b331
{
  "message": "Department deleted successfully",
  "success": true
}
```

### Search employees by name

```
curl http://127.0.0.1:5000/employees?search=gus
{
  "employees": [
    {
      "age": 20,
      "created_at": "Wed, 24 May 2023 04:41:09 GMT",
      "firstname": "gustavo",
      "id": "d43f5421-200d-4713-b6af-68a03e075749",
      "image": "courtois.jpeg",
      "is_active": true,
      "lastname": "gutierrez",
      "modified_at": "Tue, 23 May 2023 23:41:09 GMT"
    },
    {
      "age": 20,
      "created_at": "Wed, 24 May 2023 05:06:09 GMT",
      "firstname": "gustavo",
      "id": "cfd5150f-4b86-4a9b-85fb-dfe526c3346c",
      "image": "carvajal.jpeg",
      "is_active": true,
      "lastname": "gutierrez",
      "modified_at": "Wed, 24 May 2023 00:06:09 GMT"
    }
  ]
}
```

### Search departments by name

```
curl http://127.0.0.1:5000/departments?search=s
{
  "departments": [
    {
      "created_at": "Tue, 23 May 2023 23:22:55 GMT",
      "id": "eef11f69-ffe9-4078-ad09-16e31fe7f77c",
      "modified_at": "Tue, 23 May 2023 23:22:55 GMT",
      "name": "Recursos Humanos",
      "short_name": "RRHH"
    }
  ]
}

$ curl http://127.0.0.1:5000/departments?search=z
{
  "departments": []
}
```

# Tarea 1

1.- /employees - GET/POST/PATCH/DELETE
2.- /departments - GET/POST/PATCH/DELETE
3.- /employees/<id> - GET/PATCH/DELETE
4.- /departments/<id> - GET/PATCH/DELETE
5.- Search - /employees?search=<q>
6.- Search - /departments?search=<q>

