from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json


app = FastAPI()


class Patient(BaseModel):
    
    id : Annotated[Optional[str], Field(..., description="id of the patient", examples=["P001"])]
    name : Annotated[Optional[str], Field(..., description="name of the patient")]
    city : Annotated[Optional[str], Field(..., description="city name of the patient", examples=["Hyderbad"])]
    age : Annotated[Optional[int], Field(..., gt=0, lt=120, description="age of the patient")]
    gender : Annotated[Optional[Literal["male", "female", "others"]],Field(..., description="gender of the patient")]
    height : Annotated[Optional[float], Field(..., gt=0, description="height of the patient in mtrs")]
    weight: Annotated[Optional[float], Field(..., gt=0, description="weight of the patient in kgs")]

    @computed_field(return_type=float)
    @property
    def bmi(self) -> str:
        height_m = self.height / 100
        bmi = round(self.weight / (height_m ** 2), 2)
        return bmi
    
    @computed_field(return_type=str)
    @property
    def verdit(self) -> str:
        if self.bmi <18.5:
            return "underweight"
        elif self.bmi <25:
            return "normal"
        elif self.bmi <30:
            return "normal"
        else:
            return "obese"
        
class PatientUpdate(BaseModel):
    name : Annotated[str, Field(default=None)]
    city : Annotated[str, Field(default=None)]
    age : Annotated[int, Field(default=None, gt=0)]
    gender : Annotated[Literal["male", "female", "others"],Field(default=None)]
    height : Annotated[float, Field(default=None, gt=0)]
    weight: Annotated[float, Field(default=None, gt=0)]




def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


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


@app.post("/create")
def create_patient(patient : Patient):

    #firstly load the data
    data = load_data()

    #serach the patient in data 
    if patient.id in data:
        raise HTTPException(status_code="400", detail="user patient already exists")
    
    #if not in data add to database
    data[patient.id] = patient.model_dump(exclude=["id"])

    #save it back into json 
    save_data(data)

    #return a jsonrespsonse for knowing the create is working or not
    return JSONResponse(status_code=201, content={"message" : "new patient id is created in db"})


@app.put("/edit/{patient_id}")
def patient_update(patient_id : str, patient_update : PatientUpdate):

    #load the data
    data = load_data()

    #check the id present or not first
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient id not found")
    
    #create a exiting(old data of patients)
    existing_info = data[patient_id]

    #make the pydantic model
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    #update the old data with using new keys and values in updated data
    for key, value in updated_patient_info.items():
        existing_info[key] = value
    
    existing_info["id"] = patient_id 

    #pydantic object(for - ruuning the model again in bg, bmi and vedect run in buit)
    patient_pydantic_object = Patient(**existing_info)

    #pydantic object to data
    existing_info = patient_pydantic_object.model_dump(exclude="id")

    #add this new to data
    data[patient_id ] = existing_info

    #save data
    save_data(data)

    return JSONResponse(status_code=200, content={"message" : "patient updated sucessfully"})



@app.delete("/delete/{patient_id}")
def patient_deletd(patient_id : str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=202, content={"message" : "patient deleted sucessfully"})
    