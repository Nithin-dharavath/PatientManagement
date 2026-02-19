from fastapi import FastAPI
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
