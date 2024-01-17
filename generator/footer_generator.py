from reportlab.graphics.renderSVG import draw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, HexColor
from reportlab.platypus import Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


x, y = 0, 2
styles = getSampleStyleSheet()
pStyles = ParagraphStyle(name="Heading1", alignment=1,
                         parent=styles['BodyText'], leading=8.2)
width, height = letter
support_mobile_no = "8792957057"


# IMAGES
bankImage = "./assets/images/bank_image.jpeg"
report = "./assets/images/report.png"
valle_logo_white = "./assets/images/valle_logo_white.png"
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
property_image = "./assets/images/property_image.jpeg"
mobile_image = "./assets/images/Mobile.jpg"
email_image = "./assets/images/Email.jpg"
amenities = "./assets/images/Amenitites.jpeg"
additional_details = "./assets/images/additional_details.jpeg"
basic_details = "./assets/images/basic_details.jpeg"
bua_details = "./assets/images/BUA Details.jpeg"
construction_details = "./assets/images/Construction Details.jpeg"
final_valuation = "./assets/images/Final Valuation.jpeg"
ground_floor = "./assets/images/ground_floor.jpeg"
infrastructure_support = "./assets/images/Infrastructure Support.jpg"
land_area = "./assets/images/Land area.jpg"
loaction_details = "./assets/images/Loaction Details.jpeg"
plan_details = "./assets/images/Plan Details.jpeg"
plot_details = "./assets/images/Plot Details.jpeg"
remarks = "./assets/images/Remarks.jpeg"
sbua_details = "./assets/images/SBUA Details.png"
schedule_details = "./assets/images/Schedule Details.jpeg"
seal_signature_details = "./assets/images/seal_&_signature.jpeg"

# COLOURS
ACCENT = HexColor("#32B0F1")
ACCENT_BG = HexColor("#EBF8FF")
BACKGROUND = HexColor("#E9E9E8")
TEXT_ME = HexColor("#6B7280")
TEXT_HE = HexColor("#363551")

# VALLE_LEAD_NEMBER = ""

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


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.valle_lead_number = kwargs.pop('valle_lead_number', "")

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if (self._pageNumber == 1):
                self.draw_front_page_footer()
            # elif (self._pageNumber == 2):
            #     self.draw_index_header(page_count)
            #     self.draw_index_footer(page_count)
            else:
                self.draw_header(page_count)
                self.draw_footer(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_front_page_footer(self):

        left_container_style = ParagraphStyle(
            'ContainerStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=0,  # Center alignment
            fontSize=12,
            leading=16,
            backColor='white',
        )

        # Add two paragraphs (divs) to the container with a line break between them
        container_top_content = [[
            "",
            Image(valle_logo_white, width=150, height=60),
            ""
        ]
        ]

        table = Table(container_top_content,
                      colWidths=(200, 200, 200), rowHeights=50)

        table.wrapOn(self, 0, 0)

        table.drawOn(self, 30, 125)

        container_content = [[
            Image(mobile_image, width=32, height=32),
            Paragraph(
                f"<span><b>Talk to us</b></span> <br /> <p> +91 {support_mobile_no}</p>", left_container_style),
            Image(email_image, width=32, height=32),
            Paragraph(
                f"<span><b>Write to us</b></span> <br /> <p>support@navanc.com</p>", left_container_style),
        ]
        ]

        table_data = Table(container_content,
                           colWidths=(50, 160, 50, 160), rowHeights=50)#, cornerRadii=(8, 8, 8, 8))

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        # Draw the table on the canvas
        table_data.wrapOn(self, 0, 0)

        table_data.drawOn(self, 100, 50)

    def draw_index_header(self, page_count):

        data = [
            [Image(valle_logo_black, width=60, height=25),
                "",
                Image(bankImage, width=68, height=40)]
        ]
        table_data = Table(data, colWidths=(70, 400, 80), rowHeights=50)

        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)])

        table_data.setStyle(style)

        # Draw the table_data on the canvas
        table_data.wrapOn(self, height-60, 0)
        table_data.drawOn(self, 30, height-60)

    def draw_index_footer(self, page_count):
        page = self._pageNumber - 1
        content = f""" This document contains sensitive information. Share this document with essential personal only. """

        # global VALLE_LEAD_NEMBER
        # self.valle_lead_number = VALLE_LEAD_NEMBER

        lead_number_styles = ParagraphStyle(
            'CenteredStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=1,
            fontSize=14,
            backColor=ACCENT_BG,
            textColor=ACCENT,
            leading=18,
            borderRadius=3,
            borderColor=ACCENT_BG,
            borderWidth=1,
            padding=(5, 2)
        )

        page_number_styles = ParagraphStyle(
            'CenteredStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=1,
            fontSize=22,
            backColor=ACCENT,
            textColor="white",
            leading=24,
            borderRadius=(8, 8),
            borderColor=ACCENT,
            borderWidth=1,
            borderPadding=(2, 2, 20, 2)
        )

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

        table_data = Table(data, colWidths=(70, 420, 80), rowHeights=30)

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            # ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        # Draw the table on the canvas
        table_data.wrapOn(self, 0, 0)
        table_data.drawOn(self, 30, 60)

        bottom_first_data = [
            [Image(shield, width=18, height=18.25),
                Paragraph(content, left_style),
                Paragraph(f"{self.valle_lead_number}", lead_number_styles),
                Paragraph(f"{page}", page_number_styles)
             ]
        ]

        table = Table(bottom_first_data, colWidths=(
            30, 360, 100, 60), rowHeights=60)

        # Apply styles to the table if needed
        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDD'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEABOVE', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)])

        table.setStyle(style)

        # Draw the table on the canvas
        table.wrapOn(self, 0, 0)
        table.drawOn(self, 30, 0)

    def draw_header(self, page_count):

        data = [[Image(valle_logo_black, width=60, height=25),
                 Image(report, width=198, height=56),
                 Image(bankImage, width=68, height=40)]]

        table_data = Table(data, colWidths=(70, 420, 80), rowHeights=60)

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        # Draw the table_data on the canvas
        table_data.wrapOn(self, height-60, 0)
        table_data.drawOn(self, 20, height-70)

    def draw_footer(self, page_count):
        page = self._pageNumber - 1
        content = f""" This document contains sensitive information. Share this document with essential personal only. """

        # global VALLE_LEAD_NEMBER
        # self.valle_lead_number = VALLE_LEAD_NEMBER

        lead_number_styles = ParagraphStyle(
            'CenteredStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=1,
            fontSize=14,
            backColor=ACCENT_BG,
            textColor=ACCENT,
            leading=18,
            # borderRadius=(3, 3),
            borderColor=ACCENT_BG,
            borderWidth=1,
            padding=(5, 2)
        )

        page_number_styles = ParagraphStyle(
            'CenteredStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=1,
            fontSize=22,
            backColor=ACCENT,
            textColor="white",
            leading=24,
            # borderRadius=(8, 8),  
            borderColor=ACCENT,
            borderWidth=1,
            borderPadding=(2, 2, 20, 2)
        )

        data = [[Image(shield, width=18, height=18.25),
                Paragraph(content, left_style),
                Paragraph(f"{self.valle_lead_number}", lead_number_styles), Paragraph(f"{page}", page_number_styles)]]

        table = Table(data, colWidths=(30, 360, 100, 60), rowHeights=60)

        # Apply styles to the table if needed
        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEABOVE', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)])

        table.setStyle(style)

        # Draw the table on the canvas
        table.wrapOn(self, 0, 0)
        table.drawOn(self, 30, 0)