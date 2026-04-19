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
        # डेटा सुरक्षित तरीके से निकालें
        info = disease_data.get(disease, {"precautions": ["Consult a doctor for advice."]})
        precautions = info.get('precautions', ["Consult a doctor for advice."])

        pdf = FPDF()
        pdf.add_page()
        
        # --- Header ---
        pdf.set_fill_color(0, 51, 102) 
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(255, 255, 255) 
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(190, 20, txt="HEALTHCHECK AI", ln=True, align='C')
        
        pdf.ln(25) 

        # --- Content ---
        pdf.set_text_color(0, 0, 0) 
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, txt="Medical Report Summary", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 10, txt=f"Condition Identified: {disease}", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, txt="Recommended Steps:", ln=True)
        
        pdf.set_font("Arial", size=11)
        for p in precautions:
            # बिना किसी स्पेशल करैक्टर के टेक्स्ट लिखें ताकि एरर न आए
            text = str(p).encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(180, 8, txt=f"- {text}")

        # --- Save ---
        temp_file = os.path.join(tempfile.gettempdir(), "health_report.pdf")
        pdf.output(temp_file)
        
        return send_file(temp_file, as_attachment=True)
    except Exception as e:
        return f"Error generating PDF: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
