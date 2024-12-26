from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("CONNECTION_STRING_MONGO")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

client = MongoClient(connection_string)
db = client["gastos_db"]

@app.post("/expenses")
async def get_expenses(request: Request):
    try:
        body = await request.json()
        startDate = body.get("startDate")
        endDate = body.get("endDate")

        start_date = datetime.strptime(startDate, '%Y-%m-%d') if startDate else None
        end_date = datetime.strptime(endDate, '%Y-%m-%d') if endDate else None

        query = {}
        if start_date:
            query["date"] = {"$gte": start_date.strftime('%Y-%m-%d')}
        if end_date:
            if "date" in query:
                query["date"]["$lte"] = end_date.strftime('%Y-%m-%d')
            else:
                query["date"] = {"$lte": end_date.strftime('%Y-%m-%d')}

        gastos = list(db.gastos.find(query))
        department_totals = {}
        employee_totals = {}

        for gasto in gastos:
            department = db.departamento.find_one({"id": gasto["department_id"]})
            employee = db.empleado.find_one({"id": gasto["employee_id"]})

            if department and "name" in department:
                dept_name = department["name"]
                if dept_name not in department_totals:
                    department_totals[dept_name] = 0
                department_totals[dept_name] += gasto["amount"]

            if employee and "name" in employee:
                emp_name = employee["name"]
                if emp_name not in employee_totals:
                    employee_totals[emp_name] = 0
                employee_totals[emp_name] += gasto["amount"]

        return {
            "departments": [{"name": k, "total": v} for k, v in department_totals.items()],
            "employees": [{"name": k, "total": v} for k, v in employee_totals.items()],
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))