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
        info = disease_data.get(disease, {"precautions": ["Consult a doctor."]})
        precautions = info.get('precautions', ["Consult a doctor."])

        pdf = FPDF()
        pdf.add_page()
        
        # --- Header Section ---
        pdf.set_fill_color(0, 51, 102) 
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(255, 255, 255) 
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(190, 20, txt="HEALTHCHECK AI", ln=True, align='C')
        pdf.ln(25) 

        # --- Report Body ---
        pdf.set_text_color(0, 0, 0) 
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, txt="Medical Report Summary", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 10, txt=f"Condition Identified: {disease}", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, txt="Recommended Steps:", ln=True)
        pdf.ln(2)

        # --- Precautions (Fixing the alignment) ---
        pdf.set_font("Arial", size=11)
        for p in precautions:
            # सुरक्षित टेक्स्ट क्लीनिंग
            clean_text = str(p).encode('ascii', 'ignore').decode('ascii')
            
            # सुधार: हर पॉइंट शुरू करने से पहले कर्सर को वापस बाईं (X=10) पर सेट करना
            pdf.set_x(10)
            
            # बुलेट (-) के लिए एक छोटी सेल
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(10, 8, txt="-", ln=0) 
            
            # मुख्य टेक्स्ट के लिए multi_cell (ln=1 यहाँ सबसे जरूरी है)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, txt=clean_text, align='L') 
            
            # एक छोटा गैप ताकि अगला पॉइंट एकदम सटकर न आए
            pdf.ln(2)

        # --- Footer ---
        pdf.set_y(-30)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, txt="AI-Generated Report. Consult a doctor for professional advice.", align='C')

        # सुरक्षित तरीके से फाइल सेव करना
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "final_report.pdf")
        pdf.output(file_path)
        
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"

    except Exception as e:
        # अगर फिर भी एरर आए तो स्क्रीन पर दिखेगा
        return f"PDF Error Details: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
