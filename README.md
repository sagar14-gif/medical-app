
# 🩺 HealthCheck AI - Smart Symptom Analyzer
HealthCheck AI is a professional Python-based web application built using the Flask framework. It is designed to identify potential health conditions based on user-provided symptoms and generate a structured, downloadable medical summary in PDF format.Project Title




🚀 The Process (How it Works)
The application follows a systematic workflow to provide health insights:

User Input: The user enters symptoms (e.g., fever, cough, headache) into the search bar on the homepage.

Data Processing: The backend processes the input and matches it against an extensive disease database stored in symptoms_data.py.

Diagnosis Identification: Once a match is found, the system displays the identified condition along with a list of recommended precautions on the screen.

PDF Generation: Upon clicking the "Download PDF" button, the backend triggers the fpdf library to generate a professional medical report.



✨ Key Features
Intelligent Symptom Matching: Advanced logic to connect multiple symptoms to potential conditions.

Professional PDF Reports: Generates clean, hospital-style reports with headers, bullet points, and essential medical disclaimers.

High Accuracy Logic: Includes a confidence-based scoring system to show how closely symptoms match a condition.

Responsive Design: Optimized for both mobile devices and desktop computers.

Cloud Deployment: Configured for seamless hosting on platforms like Render.



🛠️ Tech Stack
Backend: Python 3.x, Flask

Frontend: HTML5, CSS3 (Modern UI)

PDF Generation: FPDF Library

Version Control: Git & GitHub

Deployment: Render



📂 Project Structure
To ensure the app runs correctly, the files are organized as follows:

Plaintext
├── app.py                 # Main application logic & PDF routes
├── symptoms_data.py       # Database of 100+ diseases, symptoms, and precautions
├── requirements.txt       # List of required Python libraries (Flask, FPDF)
├── Procfile               # Deployment instructions for Render
└── templates/             # Folder for HTML templates
    └── index.html         # The main user interface



    ⚙️ Installation & Setup
To run this project locally on your machine:

1.Clone the repository:


Bash
git clone https://github.com/your-username/medical-app.git


2.Navigate to the project folder:

Bash
cd medical-app


3.Install dependencies:

Bash
pip install -r requirements.txt


4.Run the application:

Bash
python app.py


5. Open http://127.0.0.1:5000 in your browser.

 
