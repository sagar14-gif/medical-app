from flask import Flask, render_template, request, send_file
from symptoms_data import disease_data
from fpdf import FPDF
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    precautions = []
    if request.method == 'POST':
        user_input = request.form.get('symptoms', '').lower()
        user_symptoms = [s.strip() for s in user_input.split(',')]
        
        for disease, info in disease_data.items():
            if any(s in info['symptoms'] for s in user_symptoms if s):
                result = disease
                precautions = info['precautions']
                break
        
        if not result:
            result = "No matching disease found."
            
    return render_template('index.html', result=result, precautions=precautions)

@app.route('/download_pdf/<disease>')
def download_pdf(disease):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="HealthCheck AI - Report", ln=True, align='C')
    
    # Body
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Detected Condition: {disease}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Recommended Precautions & Info:", ln=True)
    
    pdf.set_font("Arial", size=10)
    if disease in disease_data:
        for p in disease_data[disease]['precautions']:
            pdf.cell(200, 8, txt=f"- {p}", ln=True)
    
    # Disclaimer (Chetawani)
    pdf.ln(15)
    pdf.set_text_color(255, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 10, txt="CAUTION: Do not take any medicine without consulting a doctor.", ln=True, align='C')
    
    file_path = "medical_report.pdf"
    pdf.output(file_path)
    return send_file(file_path, as_attachment=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)