from flask import Flask, render_template, make_response
from generator.pdf_generator import PDFGenerator

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-pdf')
def generate_pdf():
    pdf_generator = PDFGenerator()
    pdf_response = pdf_generator.generate_pdf()
    return pdf_response

if __name__ == '__main__':
    app.run(debug=True, port=7000)