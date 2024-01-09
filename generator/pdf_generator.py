import os
import json
import requests

from flask import Flask, render_template, make_response
from io import BytesIO
from reportlab.graphics.renderSVG import draw
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import black, white, red, HexColor
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer, Frame, PageTemplate, Image, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

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

class PDFGenerator():

    def __init__(self):
        
        self.buffer = BytesIO()
        self.pagesize = letter
        
        self.start_color = HexColor('#4444BD')
        self.end_color = HexColor('#00AEFF')
        
        self.data_json_map = {
            "Basic Valuation Details" : "basic_valuation_detail",
            "Basic Details" : "basic_valuation_detail",
            "Property Details" : "property_details",
            "Location Details" : "location_detail",
            "Schedule Details" : "schedule_detail",
            "Building Details" : "building_detail",
            "Construction Details" : "construction_detail",
            "Plan Details" : "plan_detail",
            "Infrastructure Support" : "infrastructure_detail",
            "Technical Details" : "technical_details",
            "Plot Dimensions" : "plot_dimensons",
            "Land Area" : "land_area",
            "BUA Details" : "bua_detail",
            "SBUA Details" : "sbua_detail",
            "Additional Details" : "additional_details",
            "Valuer Remarks" : "valuer_remarks"
        }
        
        self.subsections = {
                'Basic Valuation Details':[ "Basic Details" ],
                'Property Details': [ "Location Details", "Schedule Details"],
                "Building Details": [ "Construction Details", "Plan Details"],
                "Infrastructure Support" : [ "Infrastructure Support"],
                "Technical Details": [ "Plot Dimensions", "Land Area", "BUA Details", "SBUA Details", "Additional Details"],
                # "Property Value Assessment" : [ ]
                "Valuer Remarks" : [ "Valuer Remarks" ]
            }
        
        # self.data_file = open(os.getcwd() + "/data/reportData.json", 'r')
        # self.data = json.load(self.data_file)
        
        self.data = self.get_data()
        
    def get_data(self):
        
        url = "https://valle-be-api.dev.navanc.com/valuer/view-report"

        payload = json.dumps({
        "token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9kZXYtc2hlN2ZlaGowYTBnYTh6eS51cy5hdXRoMC5jb20vIn0..d9TzoDsyasrHmFjg.FPaV1mh04AorlX135KywZ8Z0KCxzXEKJf0HsgFoA7bXtv4R6sVAzUmUENiQZmojP7I9PEYIPUwdNr9K4d9heshXOEiUpapC6KR8tZccfYy9r59KyrSTQx1L4C3KXCShEWGdVMCVNB6XwPSznqIPkyFtNb6x7znv-Zln811kSAqPoq-fIbMMHAy_wim52dyZwhcygtx_408xMloLWDvgI9IIyj0jz0rdPso33wpNvrKpyKyUkWDDmg5qxn3rfNL5CHwOQ-stnkVriJYD77Sa1anScK4IsVVh8np2pisw4OLGtXaXzN-nwi5Zc-Zr9Lu9dEBflRJSVfSoX-kvbvGcLMOn7PV2Vt7AUnjxUEv8LIoKKxd5CAeM3Qm2jx4FSVd0.W6IaU8yE8JGIfSvWxeKwVw",
        "valle_lead_number": "KA100662"
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        
        response_json = json.loads(response.text)
        return response_json["data"]
        
    def string_formatter(self, string):
        
        if type(string)==type({}):
            string = string.values()
            string = ' '.join([str(s) for s in string])
        
        string = str(string)
        string = string.replace("_", " ")
        string = string.title()
        return string
        
        
    def create_front_page_footer(self):
        
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
    
    def create_front_page(self):
        
        bordered_image = Image(bankImage, width=123, height=43)
        
        front_page_footer_container = self.create_front_page_footer()
        
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
        story.append(front_page_footer_container)
        story.append(PageBreak())

        return story
        
    def create_index_page_header(self, data=None):
        data = [
            [Image(valle_logo_black, width=60, height=18.25),
                "",
                Image(bankImage, width=68, height=24)]
                ]
        table_data = Table(data, colWidths=(70, 420, 80), rowHeights=60)
        
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        return table_data

    def create_index_page_footer(self, data=None):
        
        table_name_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=0,  # 0=left, 1=center, 2=right
            fontSize=12,
            # leading=18
        )
        
        data = [[Paragraph("", table_name_styles),
                Image(report, width=353, height=100),
                Paragraph("", table_name_styles),]]
        
        table_data = Table(data, colWidths=(70, 420, 80), rowHeights=60)
        
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))
        
        return table_data
    
    def create_index_page_content(self, data=None):
        
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

        table_data = Table(data, colWidths=(60, 425, 30), rowHeights=45)
        
        table_data.setStyle(TableStyle([
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

        return table_data
    
    def create_index_page(self, data=None):

        story = []
        
        header = self.create_index_page_header()
        content = self.create_index_page_content()
        footer = self.create_index_page_footer()
        
        story.append(header)
        story.append(Spacer(height=60, width=width))
        story.append(content)
        # story.append(Spacer(height=88, width=width))
        story.append(footer)

        return story

    def create_pdf_page_header(self, data=None):
        data = [[Image(valle_logo_black, width=60, height=18.25),
            Image(report, width=198, height=56),
            Image(bankImage, width=68, height=24)]]
        
        table_data = Table(data, colWidths=(70, 420, 80), rowHeights=60)
        
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        return table_data
    
    def create_pdf_page_footer(self, data=None):
        content = f""" This document contains confidential information. Share this document with authorized and
                approved users of the Financial Institution. NOT for Public Distribution"""
                
        data = [[Image(shield, width=60, height=18.25),
                Paragraph(f"<p>{content}</p>", left_style),
                Paragraph("KA100509", left_style), Paragraph("<p>1</p>", left_style)]]
        
        table_data = Table(data, colWidths=(40, 320, 80, 80), rowHeights=60)
        
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))
        
        return table_data
        
        # Create a table for the footer
        # content = """ This document contains confidential information. Share this document with authorized and
        #                 approved users of the Financial Institution. NOT for Public Distribution"""

        # footer_table_data = [[Image(shield, width=60, height=18.25),
        #                     Paragraph("12",
        #                                 left_style),
        #                     Paragraph("<p>1</p>", left_style),
        #                     Paragraph("<p>1</p>", left_style)]]

        # footer_table = Table(footer_table_data, colWidths=(
        #     40, 320, 80, 80), rowHeights=60)
        # footer_table.setStyle(TableStyle([
        #     ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
        #     ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
        #     ('ALIGN', (1, 0), (-2, -1), 'CENTER'),
        #     ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
        #     ('TEXTCOLOR', (0, 0), (1, -1), black)
        # ]))

        # # Draw the footer table on the canvas
        # footer_table.wrapOn(canvas, 0, 0)
        # footer_table.drawOn(canvas, 36, 36)

        # canvas.restoreState()
    
    def create_section_heading(self, section=None):
        
        table_name_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=0,  # 0=left, 1=center, 2=right
            fontSize=12,
            # leading=18
        )
        
        # table_section_list = self.section_headings.get(section, "")

        # for table_section_name in table_section_list:
        data = [
            [
                Image(basic_valuation_details, width=20, height=20),
                Paragraph(f"{section}", table_name_styles),
                Image(table_title_sider, width=44.56, height=20)
            ]
        ]
        
        table_data = Table(data, colWidths=(40, 450, 80), rowHeights=(40))
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('BACKGROUND', (0, 0), (0, 0), ACCENT_BG),
            # ('BACKGROUND', (0, 1), (-3, -1), red),
            # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            # ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
            # ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
            # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),

            # ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            # ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))
        
        return table_data
    
    def create_subsection_heading(self, subsection):
                
        table_name_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=0,  # 0=left, 1=center, 2=right
            fontSize=12,
            # leading=18
        )
        
        # table_section_list = self.section_headings.get(section, "")

        # for table_section_name in table_section_list:
        data = [
            [
                Image(basic_valuation_details, width=12, height=12),
                Paragraph(f"{subsection}", table_name_styles),
                Paragraph(f"", table_name_styles),
            ]
        ]
        
        table_data = Table(data, colWidths=(40, 450, 80), rowHeights=(40))
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('BACKGROUND', (0, 0), (0, 0), ACCENT_BG),
            # ('BACKGROUND', (0, 1), (-3, -1), red),
            # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            # ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
            # ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
            # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),

            # ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            # ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))
        
        return table_data
    
    def create_subsection(self, section, subsection):
        
        j_section, j_subsection = self.data_json_map.get(section), self.data_json_map.get(subsection)
        
        data_dict = {}
        
        if section in ("Basic Valuation Details", "Infrastructure Support", "Valuer Remarks"):
            data_dict = self.data.get(j_section, {})
        else:
            data_dict = self.data.get(j_section, {}).get(j_subsection, {})
        
        print("Data Dictionary: {}".format(data_dict))
        
        data = []
        
        for key, value in data_dict.items():
            if type(value)==type({}):
                data.append(["", self.string_formatter(key), ""])
                for k,v in value.items():
                    data.append(["", self.string_formatter(k), self.string_formatter(v)])
            else:
                data.append(["", self.string_formatter(key), self.string_formatter(value)])
        
        table_data = Table(data, colWidths=(25, 260, 250), rowHeights=30)
        
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # ('BACKGROUND', (0, 0), (2, 0), ACCENT_BG),
            ('BACKGROUND', (0, 0), (-1, -1), BACKGROUND),
            # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            # ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
            # ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
            # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),
            # ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))
        
        return table_data
    
    def create_section(self, section=""):
        story = []
        story.append(self.create_pdf_page_header())
        story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section))
        story.append(Spacer(width=width, height=15))
        
        sub_sections = self.subsections.get(section, "")
        for subsection in sub_sections:
            story.append(self.create_subsection_heading(subsection))
            story.append(self.create_subsection(section, subsection))
        
        story.append(Spacer(width=width, height=15))
        story.append(self.create_pdf_page_footer())
        

        return story
    
    def create_pdf_page(self, data=None):
        section_basic_valuation = self.create_section("Basic Valuation Details")
        section_property_details = self.create_section("Property Details")
        section_building_details = self.create_section("Building Details")
        section_infrastructure_support = self.create_section("Infrastructure Support")
        section_technical_details = self.create_section("Technical Details")
        section_valuer_remarks = self.create_section("Valuer Remarks")
        # section_images = imagesPage(table_name="Images")
        
        story = []
        # story.append(Spacer(width=width, height=23))
        story.append(KeepTogether(section_basic_valuation))
        story.append(PageBreak())
        story.append(KeepTogether(section_property_details))
        story.append(PageBreak())
        story.append(KeepTogether(section_building_details))
        story.append(PageBreak())
        story.append(KeepTogether(section_infrastructure_support))
        story.append(PageBreak())
        story.append(KeepTogether(section_technical_details))
        story.append(PageBreak())
        story.append(KeepTogether(section_valuer_remarks))
        # story.append(KeepTogether(section_images))

        return story
    
    
    def draw_page_background(self, canvas, width, height):
        # Create a shading pattern for the gradient
        canvas.linearGradient(x0=0, y0=height, x1=width /
                              0.5, y1=0, colors=[self.start_color, self.end_color])
    
    def generate_pdf(self):
        
        self.pdf_report = SimpleDocTemplate(self.buffer, pagesize=self.pagesize)
        
        self.frame_cover = Frame(
                self.pdf_report.leftMargin, self.pdf_report.bottomMargin,
                self.pdf_report.width, self.pdf_report.height,
                topPadding=0,
                id='normal'
            )
        
        self.frame_index = Frame(
                32, 72,
                self.pdf_report.width, self.pdf_report.height,
                topPadding=0,
                bottomPadding =20,
                id='normal'
            )
        
        # Create a PageTemplate with the Frame
        self.page_template_cover = PageTemplate(id='cover_page', frames=[
                                    self.frame_cover])
        self.page_template = PageTemplate(id='cover_page', frames=[
                                    self.frame_index])
        
        self.pdf_report.addPageTemplates([self.page_template_cover, self.page_template])
        
        self.pdf_report.onFirstPage = lambda canvas, doc: self.draw_page_background(canvas, doc.width, doc.height)

        self.pdf_queue = []
        
        ## Cover page
        front_page = self.create_front_page()
        self.pdf_queue.extend(front_page)
        
        ## Index page
        index_page_content = self.create_index_page()
        self.pdf_queue.extend(index_page_content)
        
        ## PDF Pages
        pdf_page = self.create_pdf_page()
        self.pdf_queue.extend(pdf_page)

        ## Build the PDF document
        self.pdf_report.build(self.pdf_queue)

        self.buffer.seek(0)

        # Create a response with the PDF content type
        self.pdf_response = make_response(self.buffer.read())
        self.pdf_response.headers['Content-Disposition'] = 'inline; filename=dynamic_pdf.pdf'
        self.pdf_response.headers['Content-Type'] = 'application/pdf'

        return self.pdf_response












































#     # Create a table for the footer
#     content = """ This document contains confidential information. Share this document with authorized and
#                     approved users of the Financial Institution. NOT for Public Distribution"""

#     footer_table_data = [[Image(shield, width=60, height=18.25),
#                           Paragraph("12",
#                                     left_style),
#                           Paragraph("<p>1</p>", left_style),
#                           Paragraph("<p>1</p>", left_style)]]

#     footer_table = Table(footer_table_data, colWidths=(
#         40, 320, 80, 80), rowHeights=60)
#     footer_table.setStyle(TableStyle([
#         ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
#         ('ALIGN', (1, 0), (-2, -1), 'CENTER'),
#         ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
#         ('TEXTCOLOR', (0, 0), (1, -1), black)
#     ]))

#     # Draw the footer table on the canvas
#     footer_table.wrapOn(canvas, 0, 0)
#     footer_table.drawOn(canvas, 36, 36)

#     canvas.restoreState()












# def ImagesRowContent(table_name):
#     data = [
#         [
#             "",
#            Image(property_image, width=237.5, height=155),
#            Image(property_image, width=237.5, height=155)
#         ],
#         [
#             "",
#            Image(property_image, width=237.5, height=155),
#            Image(property_image, width=237.5, height=155),
#         ],
#         [
#             "",
#            Image(property_image, width=237.5, height=155),
#            Image(property_image, width=237.5, height=155),
#         ],
#         [
#             "",
#            Image(property_image, width=237.5, height=155),
#            Image(property_image, width=237.5, height=155),
#         ]
#     ]
#     t = Table(data, colWidths=(25, 260, 250), rowHeights=200)
#     t.setStyle(TableStyle([
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         # ('BACKGROUND', (0, 0), (2, 0), ACCENT_BG),
#         ('BACKGROUND', (2, 4), (-1, -1), BACKGROUND),
#         # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
#         # ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
#         # ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
#         # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),
#         # ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
#         # ('GRID', (1, 0), (-2, -1), 1, black),
#         # ('GRID', (0, 0), (-1, -1), 0.5, red),
#         ('TEXTCOLOR', (0, 0), (1, -1), black)]))
#     return t


# def imagesPage(table_name):
#     story=[]
#     story.append(pdf_header())
#     story.append(Spacer(width=width, height=10))
#     story.append(tableFormatTitle(table_name))
#     story.append(Spacer(width=width, height=20))
#     story.append(ImagesRowContent(table_name))

#     return story














# def generate_dynamic_pdf_lg_done():
#     # Create a BytesIO buffer to hold the PDF content
#     buffer = BytesIO()
#     pdf = canvas.Canvas(buffer, pagesize=letter)
#     x, y = 0, 2
#     width, height = letter
#     start_color = HexColor('#4444BD')
#     end_color = HexColor('#00AEFF')
#     bankImage = "./assets/images/bank_image.jpeg"
#     valle_Logo_White = "./assets/SVG/Valle_Logo_White.svg"

#     # Create a path with a gradient fill
#     pdf.linearGradient(x0=x, y0=height, x1=width/0.5, y1=y,
#                        colors=[start_color, end_color])

#     # pdf.drawString(200, 700, "Hello, this is RD dynamic PDF!", direction=[x,y] )

#     pdf.drawImage(bankImage, height=60, width=183, x=width *
#                   0.38, y=height-100, preserveAspectRatio=True)
#     # renderSVG.draw(pdf, valle_Logo_White)

#     pdf.drawString(100, 100, "Hello, this is RD dynamic PDF!",
#                    direction=[x, y])

#     pdf.save()

#     buffer.seek(0)

#     # Create a response with the PDF content type
#     response = make_response(buffer.read())
#     response.headers['Content-Disposition'] = 'inline; filename=dynamic_pdf.pdf'
#     response.headers['Content-Type'] = 'application/pdf'

#     return response


# # def generate_pdf_pdfkit():
# #     try :
# #         name = "Rishabh"

# #         html = f"<html><body><h1>{name}</h1></body></html>"
# #         options = {
# #         'page-size': 'Letter',
# #         'margin-top': '0.75in',
# #         'margin-right': '0.75in',
# #         'margin-bottom': '0.75in',
# #         'margin-left': '0.75in',
# #         'encoding': "UTF-8",
# #         'no-outline': None
# #         }
# #         config = pdfkit.configuration()
# #         pdf = pdfkit.from_string(html, 'out.pdf', options=options, configuration=config, verbose=False)
# #         # pdf = pdfkit.from_string(html, verbose=True)
# #         print(pdf)

# #         header = {
# #             "Content-Type" : 'application/pdf',
# #         }

# #         response = Response(pdf, headers=header)
# #         return response
# #     except OSError:
# #         print("error")

