from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

@app.get("/")
def display():
    return {"meassage" : "Patients Record Management API"}

@app.get("/about")
def load_about():
    return {"message" : "A fully crud based backend sytem Integration"}

@app.get("/view")
def view_data():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def Patient_id(patient_id : str = Path(..., description = " id od patient database", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = "patient not found")

@app.get("/sort")
def sorted_patient(sort_by : str = Query(..., description="sort on bias of height, weight or bmi"), order : str = Query("asc", description="sort by asc or desc order")):
    
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code="404", detail="enter the vaild choice from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=404, detail="invalid order")
    
    data = load_data()
    sort_data = True if order == "desc" else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=sort_data)

    return sorted_data