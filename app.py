from flask import Flask, render_template, request
from generator.pdf_generator import PDFGenerator

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    
    valle_lead_number = str(request.form['valle_lead_number'])
    insititute_lead_number = str(request.form['insititute_lead_number'])
    organisation_name = str(request.form['organisation_name'])
    
    if valle_lead_number != "":
        pdf_generator = PDFGenerator()
        pdf_response = pdf_generator.generate_pdf(valle_lead_number, insititute_lead_number, organisation_name)
        return pdf_response
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=4000)