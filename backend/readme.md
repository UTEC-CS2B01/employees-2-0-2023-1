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
curl -F "firstname=Juan" -F "lastname=perez" -F "age=20" -F "selectDepartment=eef11f69-ffe9-4078-ad09-16e31fe7f77c" -F "image=@cristiano.jpeg;type=image/jpeg" -X POST http://localhost:5002/employees

{
  "id": "27b79c53-edeb-4caf-9bcb-3725669eaa9d",
  "message": "Employee Created successfully!",
  "success": true
}

curl -X POST http://localhost:5002/employees
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
curl -F "name=Departmento de Ventas" -F "short_name=DV" -X POST http://localhost:5002/departments

{
  "id": "15f1b7a4-3f63-4e2e-b5b2-f4ea02a5b331",
  "message": "Department created successfully!",
  "success": true
}

curl   -X POST http://localhost:5002/departments
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
curl -F "firstname=juan2" -F "lastname=perez2" -F "age=40" -F "is_active=false" -X PATCH http://localhost:5002/employees/d2064332-6a02-43c8-b8d5-d070979bda4b
{
  "message": "Employee updated successfully",
  "success": true
}
```

### Patch Department

```
curl -F "name=Departmento de Finanzas" -F "short_name=DF" -X PATCH http://localhost:5002/departments/15f1b7a4-3f63-4e2e-b5b2-f4ea02a5b331
{
  "message": "Department updated successfully",
  "success": true
}
```

### Delete Deparmtent

```
curl -X DELETE http://localhost:5002/departments/15f1b7a4-3f63-4e2e-b5b2-f4ea02a5b331
{
  "message": "Department deleted successfully",
  "success": true
}
```

### Delete Deparmtent

```
curl -X DELETE http://localhost:5002/employees/d2064332-6a02-43c8-b8d5-d070979bda4b
{
  "message": "Employee deleted successfully",
  "success": true
}
```

### Search employees by name

```
curl http://localhost:5002/employees?search=gus
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
curl http://localhost:5002/departments?search=s
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

$ curl http://localhost:5002/departments?search=z
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

### Create Branch

git checkout -b feature/tarea-1-23-05-2021-<username de gitbhub>

git checkout -b feature/tarea-1-23-05-2021-mabisrror

### Testing: Crear PR with rules

- Not merge until 3 approvals

### Tarea 4

- Crear Rama: fix/UTEC-O004-username-tests-endpoints-unnittest
- Donde username es el usuario de github
- Crear los tests para todos los endpoints (16)
- # success, failed_400, failed_500
- DO NOT merge until 3 approvals
