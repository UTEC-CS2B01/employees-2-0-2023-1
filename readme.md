# Structure Project

-Mantenimiento + app/ + **init**.py + models.py + controller.py + service.py + confi/ + local.py + qa.py + ingtegration.py + production.py + tests/ + test_controller.py + test_service.py

## Operations

### Create Employee

```
curl -F "first_name=Juan" -F "last_name=perez" -F "job_title=Reclutador" -F "selectDepartment=3cf975cb-ad8f-4e79-ac83-a9f4a0f466c9" -F "image=@cristiano.jpeg;type=image/jpeg" -X POST http://localhost:5004/employees
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


### Create Departaments
```	

```
