Patient Record Management API

A fully functional CRUD-based REST API built using FastAPI for managing patient records.
This system stores patient data in a JSON file and performs automatic BMI calculation with health classification.

🚀 Features:

✅ Create Patient
📄 View All Patients
🔍 View Single Patient by ID
✏️ Update Patient Details
❌ Delete Patient
📊 Sort Patients (by height, weight, BMI)
🧮 Automatic BMI Calculation
🏷 Health Category Verdict.

🛠 Tech Stack :

Technology	Purpose
FastAPI	Backend Framework
Pydantic	Data Validation
JSON	Data Storage
Uvicorn	ASGI Server.

📂 Project Structure :

PatientManagement/
│
├── main.py
├── patients.json
├── README.md
└── requirements.txt   

📦 Installation:

1️⃣ Clone Repository
git clone https://github.com/nithin-dharavathu/PatientManagement.git
cd PatientManagement
2️⃣ Create Virtual Environment
python -m venv venv
Activate: Windows - venv\Scripts\activate
Mac/Linux - source venv/bin/activate
3️⃣ Install Dependencies
pip install fastapi uvicorn
▶️ Running the Server
uvicorn main:app --reload

Server runs at: http://127.0.0.1:8000
Swagger Documentation: http://127.0.0.1:8000/docs
ReDoc Documentation: http://127.0.0.1:8000/redoc


📌 API Endpoints:

🏠 Base Route
GET / - Returns welcome message.

ℹ️ About
GET /about - Returns API description.

📄 View All Patients
GET /view - Returns all patient records.

🔍 Get Patient by ID
GET /patient/{patient_id} - Example: /patient/P001

➕ Create Patient :

POST /create
Sample JSON Body:
{
  "id": "P001",
  "name": "Nithin",
  "city": "Hyderabad",
  "age": 22,
  "gender": "male",
  "height": 170,
  "weight": 65
}

✏️ Update Patient:
PUT /edit/{patient_id} - Only send fields that need updating.

Example:
{
  "weight": 70
}

❌ Delete Patient:
DELETE /delete/{patient_id}

Example: /delete/P001

📊 Sort Patients
GET /sort?sort_by=height&order=asc
Query Parameters:
Parameter	Values
sort_by	height / weight / bmi
order	asc / desc
Example: /sort?sort_by=bmi&order=desc

🧮 BMI Calculation Logic:
BMI Formula - BMI = weight / (height_in_meters)^2

Health Verdict:
BMI Range	Category
< 18.5	Underweight
18.5 - 24.9	Normal
25 - 29.9	Overweight
≥ 30	Obese

⚠️ Validations :

Age must be between 1 and 120
Height and Weight must be > 0

Gender must be:

male, female, others

Duplicate Patient ID not allowed

📌 Notes :

Data is stored in patients.json
This is a file-based backend (not production ready)
For production, replace JSON storage with: PostgreSQL / MySQL / MongoDB

📈 Future Improvements :

🔐 Authentication & Authorization
🗄 Database Integration
🧪 Unit Testing
🐳 Docker Deployment
☁️ Cloud Deployment (AWS/Azure)

👨‍💻 Author
Nithin
Final Year B.Tech Student
Aspiring Backend Developer 🚀
