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
    try:
        # डेटा निकालें
        info = disease_data.get(disease, {"precautions": ["Consult a doctor."]})
        precautions = info.get('precautions', ["Consult a doctor."])

        pdf = FPDF()
        pdf.add_page()
        
        # --- Blue Header ---
        pdf.set_fill_color(0, 51, 102) 
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(255, 255, 255) 
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(190, 20, txt="HEALTHCHECK AI", ln=True, align='C')
        
        pdf.ln(25) 

        # --- Diagnosis ---
        pdf.set_text_color(0, 0, 0) 
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, txt="MEDICAL REPORT SUMMARY", ln=True, border='B')
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        # सुरक्षित टेक्स्ट क्लीनिंग
        clean_disease = str(disease).encode('ascii', 'ignore').decode('ascii')
        pdf.cell(190, 10, txt=f"Identified Condition: {clean_disease}", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, txt="Recommended Precautions:", ln=True)
        
        # --- Precautions List ---
        pdf.set_font("Arial", size=11)
        for p in precautions:
            
            clean_text = str(p).encode('ascii', 'ignore').decode('ascii')
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(10, 8, txt="-", ln=0) 
            
            pdf.set_font("Arial", size=11)
             
            pdf.multi_cell(0, 8, txt=clean_text, align='L')
            
            pdf.ln(2)

        # --- PDF Output ---
        temp_file = os.path.join(tempfile.gettempdir(), "health_report.pdf")
        pdf.output(temp_file)
        
        return send_file(temp_file, as_attachment=True)

    except Exception as e:
        # अगर फिर भी एरर आए तो स्क्रीन पर दिखेगा
        return f"PDF Error Details: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
