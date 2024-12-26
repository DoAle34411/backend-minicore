from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING_MONGO")

client = MongoClient(connection_string)
db = client["gastos_db"]

# Insert empleados
empleados = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "Diana"},
    {"id": 5, "name": "Eve"},
]
db.empleado.insert_many(empleados)

# Insert departamentos
departamentos = [
    {"id": 1, "name": "HR"},
    {"id": 2, "name": "IT"},
    {"id": 3, "name": "Finance"},
    {"id": 4, "name": "Marketing"},
    {"id": 5, "name": "Operations"},
]
db.departamento.insert_many(departamentos)

# Generate random gastos
random.seed(42)
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

gastos = []
for i in range(1, 101):  # 100 expense records
    gasto_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    gastos.append({
        "id": i,
        "date": gasto_date.strftime("%Y-%m-%d"),
        "description": f"Expense {i}",
        "amount": round(random.uniform(20.0, 500.0), 2),
        "employee_id": random.randint(1, len(empleados)),
        "department_id": random.randint(1, len(departamentos)),
    })

db.gastos.insert_many(gastos)

print("Data successfully inserted!")
