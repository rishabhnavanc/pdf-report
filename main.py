from flask import Flask, render_template, make_response
from io import BytesIO
from reportlab.graphics.renderSVG import draw
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import black, white, red, HexColor
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer, Frame, PageTemplate, Image, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

app = Flask(__name__)
x, y = 0, 2
styles = getSampleStyleSheet()
pStyles = ParagraphStyle(name="Heading1", alignment=1,
                         parent=styles['BodyText'], leading=8.2)
width, height = letter

# IMAGES
bankImage = "./assets/images/bank_image.jpeg"
report = "./assets/images/report.png"
valle_logo_white = "./assets/images/valle_logo_white.jpeg"
valle_logo_black = "./assets/images/valle_logo_black.jpeg"
basic_valuation_details = "./assets/images/Basic Valuation Details.jpeg"
property_details = "./assets/images/Property Details.jpg"
building_details = "./assets/images/Building Details .jpeg"
infrastructure_details = "./assets/images/Infrastructure Details.jpeg"
technical_details = "./assets/images/Technical Details.jpeg"
property_value_assesment = "./assets/images/Property Value Assesment.jpeg"
valuer_remarks = "./assets/images/Valuer Remarks.png"
valuer_details = "./assets/images/Valuer Details.png"
images = "./assets/images/Images Icon.jpeg"
shield = "./assets/images/shield.jpeg"
table_title_sider = "./assets/images/table_title_sider.jpeg"
property_image= "./assets/images/property_image.jpeg"

# COLOURS
ACCENT = HexColor("#32B0F1")
ACCENT_BG = HexColor("#EBF8FF")
BACKGROUND = HexColor("#E9E9E8")

# Styles
left_style = ParagraphStyle(
    'CenteredStyle',
    parent=getSampleStyleSheet()['BodyText'],
    alignment=0,  # 0=left, 1=center, 2=right
)
centered_style = ParagraphStyle(
    'CenteredStyle',
    parent=getSampleStyleSheet()['BodyText'],
    alignment=1,  # 0=left, 1=center, 2=right
)
right_style = ParagraphStyle(
    'CenteredStyle',
    parent=getSampleStyleSheet()['BodyText'],
    alignment=2,  # 0=left, 1=center, 2=right
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-pdf')
def generate_pdf():
    response = generate_pdf_class()
    return response


def front_page():

    bordered_image = Image(bankImage, width=123, height=43)

    def footor():

        container_style = ParagraphStyle(
            'ContainerStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=1,  # Center alignment
            # spaceBefore=20,  # Adjust as needed
            # spaceAfter=20,   # Adjust as needed
            backColor='white',
        )

        # Add two paragraphs (divs) to the container with a line break between them
        container_content = [
            Paragraph("First Div Content", left_style),
            # Paragraph("<br/>", centered_style),  # Line break
            Paragraph("Second Div Content", right_style),
        ]

        container = KeepTogether(container_content, container_style)
        return container

    pdfFootorContainer = footor()

    story = []

    story.append(bordered_image)
    story.append(Spacer(height=10, width=width))
    story.append(Image(report, width=400, height=98))
    story.append(Spacer(height=18, width=width))

    content_text = f"""<font size=32 color='white'>Valuation Report</font>"""
    story.append(Paragraph(content_text, pStyles))
    # story.append(Spacer(height=150, width=width))
    story.append(Spacer(height=350, width=width))
    story.append(Image(valle_logo_white, width=150, height=40))
    story.append(pdfFootorContainer)
    story.append(PageBreak())

    return story


def pdf_index_header():
    data = [[Image(valle_logo_black, width=60, height=18.25),
            "",
            Image(bankImage, width=68, height=24)]]
    t = Table(data, colWidths=(70, 420, 80), rowHeights=60)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
        ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
        ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
        # ('GRID', (1, 0), (-2, -1), 1, black),
        # ('GRID', (0, 0), (-1, -1), 0.5, red),
        ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
        ('TEXTCOLOR', (0, 0), (1, -1), black)]))

    return t

def pdf_header():
    data = [[Image(valle_logo_black, width=60, height=18.25),
            Image(report, width=198, height=56),
            Image(bankImage, width=68, height=24)]]
    t = Table(data, colWidths=(70, 420, 80), rowHeights=60)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
        ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
        ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
        # ('GRID', (1, 0), (-2, -1), 1, black),
        # ('GRID', (0, 0), (-1, -1), 0.5, red),
        ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
        ('TEXTCOLOR', (0, 0), (1, -1), black)]))

    return t


def pdf_footer(canvas, doc):

    # content = f""" This document contains confidential information. Share this document with authorized and
    #             approved users of the Financial Institution. NOT for Public Distribution"""
    # data = [[Image(shield, width=60, height=18.25),
    #         Paragraph(f"<p>{content}</p>"),
    #         Paragraph("KA100509"), Paragraph("<p>1</p>")]]
    # t = Table(data, colWidths=(40, 320, 80, 80), rowHeights=60)
    # t.setStyle(TableStyle([
    #     ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
    #     ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
    #     ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
    #     # ('GRID', (1, 0), (-2, -1), 1, black),
    #     # ('GRID', (0, 0), (-1, -1), 0.5, red),
    #     ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
    #     ('TEXTCOLOR', (0, 0), (1, -1), black)]))
    # return t

    # Create a table for the footer
    content = """ This document contains confidential information. Share this document with authorized and
                    approved users of the Financial Institution. NOT for Public Distribution"""

    footer_table_data = [[Image(shield, width=60, height=18.25),
                          Paragraph("12",
                                    left_style),
                          Paragraph("<p>1</p>", left_style),
                          Paragraph("<p>1</p>", left_style)]]

    footer_table = Table(footer_table_data, colWidths=(
        40, 320, 80, 80), rowHeights=60)
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
        ('ALIGN', (1, 0), (-2, -1), 'CENTER'),
        ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
        ('TEXTCOLOR', (0, 0), (1, -1), black)
    ]))

    # Draw the footer table on the canvas
    footer_table.wrapOn(canvas, 0, 0)
    footer_table.drawOn(canvas, 36, 36)

    canvas.restoreState()


def index_page_content():
    contentStyles = ParagraphStyle(
        name="content", parent=styles['BodyText'], alignment=0, leading=8.2, fontSize=16, fontWeight="700")
    pageCountStyles = ParagraphStyle(
        name="page-count", alignment=1, parent=styles['BodyText'], leading=8.2, fontSize=14, textColor=ACCENT)

    size = 26
    # Can be optimised
    data = [
        [Image(basic_valuation_details, width=size, height=size),
            Paragraph("<p>Basic Valuation Details</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
        [Image(property_details, width=size, height=size),
            Paragraph("<p>Property Details</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
        [Image(building_details, width=size, height=size),
            Paragraph("<p>Building Details</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
        [Image(infrastructure_details, width=size, height=size),
            Paragraph("<p>Infrastructure Support</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
        [Image(technical_details, width=size, height=size),
            Paragraph("<p>Technical Details</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
        [Image(property_value_assesment, width=size, height=size),
            Paragraph("<p>Property Value Assesment</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
        [Image(valuer_remarks, width=size, height=size),
            Paragraph("<p>Valuer Remarks</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
        [Image(valuer_details, width=size, height=size),
            Paragraph("<p>Valuer Details</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
        [Image(images, width=size, height=size),
            Paragraph("<p>Images</p>", contentStyles),
            Paragraph("<p>2</p>", pageCountStyles)],
    ]

    t = Table(data, colWidths=(60, 425, 30), rowHeights=45)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
        # ('VALIGN', (1, 0), (-2, -1), 'TOP'),
        # ('ALIGN', (1, 0), (-2, -1), 'LEFT'),
        # ('VALIGN', (1, 2), (-2, -1), 'BOTTOM'),
        ('BOTTOMPADDING', (1, 0), (-2, -1), 15),
        ('BOTTOMPADDING', (2, 0), (-1, -1), 10),
        # ('GRID', (1, 0), (-2, -1), 1, black),
        # ('GRID', (0, 0), (-1, -1), 0.5, red),
        # ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
        ('TEXTCOLOR', (0, 0), (1, -1), black)]))

    return t


def index_page_content_footer():
    data = [[Paragraph(""),
            Image(report, width=353, height=100),
            Paragraph(""),]]
    t = Table(data, colWidths=(70, 420, 80), rowHeights=60)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
        ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
        ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
        # ('GRID', (1, 0), (-2, -1), 1, black),
        # ('GRID', (0, 0), (-1, -1), 0.5, red),
        ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
        ('TEXTCOLOR', (0, 0), (1, -1), black)]))
    return t


def index_page():

    story = []
    header = pdf_index_header()
    content = index_page_content()
    content_footer_image = index_page_content_footer()
    story.append(header)
    story.append(Spacer(height=60, width=width))
    story.append(content)
    # story.append(Spacer(height=88, width=width))
    story.append(content_footer_image)

    return story


def tableFormatTitle(table_name):
    table_name_styles = ParagraphStyle(
        'table_name_styles',
        parent=getSampleStyleSheet()['BodyText'],
        alignment=0,  # 0=left, 1=center, 2=right
        fontSize=12,
        # leading=18
    )

    switch={
       'Basic Valuation Details': "Basic Details",
       'Images': "All Images",
       'i': "It is a vowel",
       'o': "It is a vowel",
       'u': "It is a vowel",
    }
    table_section_name = switch.get(table_name)

    data = [
        [
            Image(basic_valuation_details, width=20, height=20),
            Paragraph(f"{table_name}", table_name_styles),
            Image(table_title_sider, width=44.56, height=20)
        ],
        [
            Image(basic_valuation_details, width=12, height=12),
            Paragraph(f"{table_section_name}", table_name_styles),
            Paragraph(f"", table_name_styles),
        ]
    ]
    t = Table(data, colWidths=(40, 450, 80), rowHeights=(40, 40))
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, 0), 'CENTRE'),
        ('BACKGROUND', (0, 0), (2, 0), ACCENT_BG),
        # ('BACKGROUND', (0, 1), (-3, -1), red),
        # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
        ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
        ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
        # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),

        ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
        # ('GRID', (1, 0), (-2, -1), 1, black),
        # ('GRID', (0, 0), (-1, -1), 0.5, red),
        # ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
        ('TEXTCOLOR', (0, 0), (1, -1), black)]))
    return t


def BasicValuationDetailsRowContent(table_name):
    data = [
        [
            "",
            "Name of Applicant",
            "John Doe",
        ],
        [
            "",
            "Report Date",
            "9 Dec 2023",
        ],
        [
            "",
            "Loan Type",
            "Loan Against Property",
        ],
        [
            "",
            "Person Met at site",
            "9 Dec 2023",
        ],
        [
            "",
            "Documents Provided",
            "A photocopy of Gift settlement \nDeed No. XX11 /XX30 DTD 10-02-2000 ",
        ],
    ]
    t = Table(data, colWidths=(25, 260, 250), rowHeights=30)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # ('BACKGROUND', (0, 0), (2, 0), ACCENT_BG),
        ('BACKGROUND', (2, 4), (-1, -1), BACKGROUND),
        # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
        # ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
        # ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
        # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),
        # ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
        # ('GRID', (1, 0), (-2, -1), 1, black),
        # ('GRID', (0, 0), (-1, -1), 0.5, red),
        ('TEXTCOLOR', (0, 0), (1, -1), black)]))
    return t

def ImagesRowContent(table_name):
    data = [
        [
            "",
           Image(property_image, width=237.5, height=155),
           Image(property_image, width=237.5, height=155)
        ],
        [
            "",
           Image(property_image, width=237.5, height=155),
           Image(property_image, width=237.5, height=155),
        ],
        [
            "",
           Image(property_image, width=237.5, height=155),
           Image(property_image, width=237.5, height=155),
        ],
        [
            "",
           Image(property_image, width=237.5, height=155),
           Image(property_image, width=237.5, height=155),
        ]
    ]
    t = Table(data, colWidths=(25, 260, 250), rowHeights=200)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # ('BACKGROUND', (0, 0), (2, 0), ACCENT_BG),
        ('BACKGROUND', (2, 4), (-1, -1), BACKGROUND),
        # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
        # ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
        # ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
        # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),
        # ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
        # ('GRID', (1, 0), (-2, -1), 1, black),
        # ('GRID', (0, 0), (-1, -1), 0.5, red),
        ('TEXTCOLOR', (0, 0), (1, -1), black)]))
    return t


def table(table_name):
    story = []
    story.append(pdf_header())
    story.append(Spacer(width=width, height=8))
    story.append(tableFormatTitle(table_name))
    story.append(Spacer(width=width, height=15))
    story.append(BasicValuationDetailsRowContent(table_name))

    return story


def imagesPage(table_name):
    story=[]
    story.append(pdf_header())
    story.append(Spacer(width=width, height=10))
    story.append(tableFormatTitle(table_name))
    story.append(Spacer(width=width, height=20))
    story.append(ImagesRowContent(table_name))

    return story


def pdf_content():

    section_basic_valuation = table(table_name="Basic Valuation Details")
    section_images = imagesPage(table_name="Images")
    story = []
    # story.append(Spacer(width=width, height=23))
    story.append(KeepTogether(section_basic_valuation))
    story.append(KeepTogether(section_images))

    return story


def generate_pdf_class():
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    start_color = HexColor('#4444BD')
    end_color = HexColor('#00AEFF')

    frame_cover = Frame(
        pdf.leftMargin, pdf.bottomMargin,
        pdf.width, pdf.height,
        topPadding=0,
        id='normal'
    )
    frame_index = Frame(
        32, 72,
        pdf.width, pdf.height,
        topPadding=0,
        bottomPadding =20,
        id='normal'
    )

    # Create a PageTemplate with the Frame
    page_template_cover = PageTemplate(id='cover_page', frames=[
                                 frame_cover])
    page_template = PageTemplate(id='cover_page', frames=[
                                 frame_index])

    pdf.addPageTemplates([page_template_cover, page_template])

    def draw_page_background(canvas, width, height):
        # Create a shading pattern for the gradient
        canvas.linearGradient(x0=0, y0=height, x1=width /
                              0.5, y1=0, colors=[start_color, end_color])

    pdf.onFirstPage = lambda canvas, doc: draw_page_background(canvas, doc.width, doc.height)

    pdf_queue = []
    cover_page = front_page()
    index_page_content = index_page()
    pdf_data = pdf_content()

    pdf_queue.extend(cover_page)
    pdf_queue.extend(index_page_content)
    pdf_queue.extend(pdf_data)

    # Build the PDF document
    pdf.build(pdf_queue)

    buffer.seek(0)

    # Create a response with the PDF content type
    response = make_response(buffer.read())
    response.headers['Content-Disposition'] = 'inline; filename=dynamic_pdf.pdf'
    response.headers['Content-Type'] = 'application/pdf'

    return response


if __name__ == '__main__':
    app.run(debug=True)
