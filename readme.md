# Structure Project

-Mantenimiento + app/ + **init**.py + models.py + controller.py + service.py + confi/ + local.py + qa.py + ingtegration.py + production.py + tests/ + test_controller.py + test_service.py

## Operations

### Create Employee

```
curl -F "first_name=Juan" -F "last_name=perez" -F "job_title=Reclutador" -F "selectDepartment=3cf975cb-ad8f-4e79-ac83-a9f4a0f466c9" -F "image=@cristiano.jpeg;type=image/jpeg" -X POST http://localhost:5004/employees
```

### Create Department

```
curl -F "name=ingenieros" -F "shortname=ing" -X POST "http://127.0.0.1:5000/departments"
```

### Errors

```
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

# Tarea 1

1.- /employees - GET/POST/PATCH/DELETE
2.- /departments - GET/POST/PATCH/DELETE
3.- /employees/<id> - GET/PATCH/DELETE
4.- /departments/<id> - GET/PATCH/DELETE
5.- Search - /employees?search=<q>
6.- Search - /departments?search=<q>
