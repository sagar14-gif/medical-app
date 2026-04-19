import os
import tempfile
from flask import Flask, render_template, request, send_file
from symptoms_data import disease_data
from fpdf import FPDF

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
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Health Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Condition: {disease}", ln=True)
    
    # PDF सेव करने का तरीका (Windows और Render दोनों के लिए)
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "report.pdf")
    pdf.output(file_path)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
