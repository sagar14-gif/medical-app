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
    # बीमारी का डेटा निकालें
    info = disease_data.get(disease, {})
    precautions = info.get('precautions', ["Consult a doctor for detailed advice."])

    pdf = FPDF()
    pdf.add_page()
    
    # --- Blue Header Bar ---
    pdf.set_fill_color(0, 51, 102) 
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_text_color(255, 255, 255) 
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(190, 20, txt="HEALTHCHECK AI", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(190, 10, txt="Smart Symptom Analysis Report", ln=True, align='C')
    
    pdf.ln(20) 

    # --- Report Section ---
    pdf.set_text_color(0, 0, 0) 
    pdf.set_font("Arial", 'B', 16)
    pdf.set_draw_color(0, 51, 102)
    pdf.cell(190, 10, txt="Diagnosis Summary", ln=True, border='B')
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 10, txt=f"Detected Condition: {disease}", ln=True)
    
    pdf.ln(10)

    # --- Precautions Section ---
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, txt="Recommended Precautions", ln=True, border='B')
    
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    
    # सावधानियों को बुलेट पॉइंट्स में जोड़ें
    for p in precautions:
        pdf.cell(10, 8, txt="*", ln=0)
        pdf.multi_cell(180, 8, txt=p)
        pdf.ln(2)

    # --- Footer ---
    pdf.set_y(-40)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(128, 128, 128)
    disclaimer = ("Disclaimer: This report is AI-generated and for informational purposes only. "
                  "It is not a substitute for professional medical advice. Always consult a doctor.")
    pdf.multi_cell(190, 5, txt=disclaimer, align='C')

    # PDF को सुरक्षित जगह पर सेव करें
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "Medical_Report.pdf")
    pdf.output(file_path)
    
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
