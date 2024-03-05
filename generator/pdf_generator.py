import os
import json
import requests
import shutil
import re
import datetime

from flask import make_response, Response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, HexColor
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, PageBreak, Paragraph, Preformatted, Spacer, Frame, PageTemplate, Image, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
# from generator.footer_generator import FooterCanvas
from reportlab.graphics.renderSVG import draw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, HexColor, red
from reportlab.platypus import Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


x, y = 0, 2
styles = getSampleStyleSheet()
pStyles = ParagraphStyle(name="Heading1", alignment=1,
                         parent=styles['BodyText'], leading=8.2)
width, height = letter
support_mobile_no = "8792957057"


# IMAGES
bankImage = "assets/images/bank_image.jpeg"
report = "assets/images/report.png"
valle_logo_white = "assets/images/valle_logo_white.png"
valle_logo_black = "assets/images/valle_logo_black.png"
basic_valuation_details = "assets/images/Basic Valuation Details.png"
property_details = "assets/images/Property Details.png"
building_details = "assets/images/Building Details.png"
infrastructure_details = "assets/images/Infrastructure Details.png"
technical_details = "assets/images/Technical Details.png"
property_value_assesment = "assets/images/Property Value Assesment.png"
valuer_remarks = "assets/images/Valuer Remarks.png"
valuer_details = "assets/images/Valuer Details.png"
images = "assets/images/Images Icon.png"
shield = "assets/images/shield.png"
table_title_sider = "assets/images/table_title_sider.jpeg"
property_image = "assets/images/property_image.jpeg"
mobile_image = "assets/images/Mobile.jpg"
email_image = "assets/images/Email.jpg"
amenities = "assets/images/Amenities.jpeg"
additional_details = "assets/images/additional_details.jpeg"
basic_details = "assets/images/basic_details.jpeg"
bua_details = "assets/images/BUA Details.png"
construction_details = "assets/images/Construction details.jpg"
final_valuation = "assets/images/Final Valuation.jpeg"
ground_floor = "assets/images/ground_floor.jpeg"
infrastructure_support = "assets/images/Infrastructure Support.png"
land_area = "assets/images/Land area.jpg"
loaction_details = "assets/images/Land area.jpg"
plan_details = "assets/images/Plan details.jpg"
plot_details = "assets/images/Plot Details.jpeg"
remarks = "assets/images/Remarks.jpeg"
sbua_details = "assets/images/SBUA Details.png"
schedule_details = "assets/images/Schedule Details.jpg"
seal_signature_details = "assets/images/seal_&_signature.jpeg"

# COLOURS
ACCENT = HexColor("#32B0F1")
ACCENT_BG = HexColor("#EBF8FF")
BACKGROUND = HexColor("#E9E9E8")
TEXT_ME = HexColor("#6B7280")
TEXT_HE = HexColor("#363551")

VALLE_LEAD_NEMBER = ""

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

        # self.data_file = open(os.getcwd() + "/generator/response_data.json", 'r')
        # self.data = json.load(self.data_file)

        # print(self.data)

        self.data_file = open(os.getcwd() + "/data/reportData.json", 'r')
        self.data = json.load(self.data_file)

        # self.data = self.get_data()

    def get_data(self, valle_lead_number, user_id):

        # url = "https://valle-be-api.dev.navanc.com/valuer/view-report"

        # payload = json.dumps({
        # "token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9kZXYtc2hlN2ZlaGowYTBnYTh6eS51cy5hdXRoMC5jb20vIn0..d9TzoDsyasrHmFjg.FPaV1mh04AorlX135KywZ8Z0KCxzXEKJf0HsgFoA7bXtv4R6sVAzUmUENiQZmojP7I9PEYIPUwdNr9K4d9heshXOEiUpapC6KR8tZccfYy9r59KyrSTQx1L4C3KXCShEWGdVMCVNB6XwPSznqIPkyFtNb6x7znv-Zln811kSAqPoq-fIbMMHAy_wim52dyZwhcygtx_408xMloLWDvgI9IIyj0jz0rdPso33wpNvrKpyKyUkWDDmg5qxn3rfNL5CHwOQ-stnkVriJYD77Sa1anScK4IsVVh8np2pisw4OLGtXaXzN-nwi5Zc-Zr9Lu9dEBflRJSVfSoX-kvbvGcLMOn7PV2Vt7AUnjxUEv8LIoKKxd5CAeM3Qm2jx4FSVd0.W6IaU8yE8JGIfSvWxeKwVw",
        # "valle_lead_number": valle_lead_number
        # })
        # headers = {
        # 'Content-Type': 'application/json'
        # }

        # response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)

        # response_json = json.loads(response.text)
        # print(response_json)
        # response = valuer_service.get_report_data(valle_lead_number, user_id)
        # self.data = response["data"]

        self.property_value_assesment_map = self.data.get(
            'property_value_assessment').keys()
        
        self.sorted_property_value_assesment_map = self.sort_PVA_sections(self.property_value_assesment_map)

        self.property_value_assesment = [self.string_formatter(
            val) for val in self.sorted_property_value_assesment_map]

        self.data_json_map = {
            "Basic Valuation Details": "basic_valuation_detail",
            "Basic Details": "basic_valuation_detail",
            "Property Details": "property_details",
            "Location Details": "location_detail",
            "Schedule Details": "schedule_detail",
            "Building Details": "building_detail",
            "Construction Details": "construction_detail",
            "Plan Details": "plan_detail",
            "Infrastructure Support": "infrastructure_detail",
            "Technical Details": "technical_details",
            "Plot Dimensions": "plot_dimensons",
            "Land Area": "land_area",
            "BUA Details": "bua_detail",
            "SBUA Details": "sbua_detail",
            "Additional Details": "additional_details",
            "Valuer Remarks": "valuer_remarks",
            "Property Value Assessment": "property_value_assessment",
            "Images": "images",
            "Valuer Details": "valuer_detail",
            "Valuer Declaration": "valuer_declaration",
            "Declaration": "declaration",
        }

        self.subsections = {
            'Basic Valuation Details': ["Basic Details"],
            'Property Details': ["Location Details", "Schedule Details"],
            "Building Details": ["Construction Details", "Plan Details"],
            "Infrastructure Support": ["Infrastructure Support"],
            "Technical Details": ["Plot Dimensions", "Land Area", "BUA Details", "SBUA Details", "Additional Details"],
            "Property Value Assessment": self.property_value_assesment,
            "Valuer Remarks": ["Valuer Remarks"],
            "Valuer Details": ["Seal and Signature"],
            "Valuer Declaration": ["Declaration"],
            "Images": ["All Images"]
        }

        self.section_images = {
            "basic_valuation_detail": basic_valuation_details,
            "property_details": property_details,
            "building_detail": building_details,
            "infrastructure_detail": infrastructure_details,
            "technical_details": technical_details,
            "property_value_assessment": property_value_assesment,
            "valuer_remarks": valuer_remarks,
            "images": images,
            "valuer_detail": valuer_details,
        }

        self.subsection_images = {
            "amenities":  amenities,
            "additional_details": additional_details,
            "basic_valuation_detail": basic_details,
            "bua_detail": bua_details,
            "construction_detail": construction_details,
            "final_valuation": final_valuation,
            "ground_floor": ground_floor,
            "infrastructure_detail": infrastructure_support,
            "land_area": land_area,
            "location_detail": loaction_details,
            "plot_dimensons": plan_details,
            "plot_details": plot_details,
            "remarks": remarks,
            "sbua_detail": sbua_details,
            "schedule_detail": schedule_details,
            "seal_signature_details": seal_signature_details,
        }

        self.prefix_mapping = {
            "property_value_assessment": {
                "land": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_layout_plan": "Rs "
                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_layout_plan": "Rs "

                    }
                },
                "basement_1": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs ",
                    }
                },
                "basement_2": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    }
                },
                "ground_1": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    }
                },
                "ground_2": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    }
                },
                "ground_3": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs ",
                    }
                },
                "floor_1": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    }
                },
                "floor_2": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs ",
                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    }
                },
                "floor_3": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    }
                },
                "floor_4": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    }
                },
                "non-rcc_1": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    }
                },
                "non-rcc_2": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    }
                },
                "non-rcc_3": {
                    "government_price": "Rs ",
                    "consideration_price": "Rs ",
                    "total_value_government_price": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                    "total_value_fair_market": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    }
                },
                "amenities": {
                    "amenity_1": {
                        "value": "Rs "
                    },
                    "amenity_2": {
                        "value": "Rs "
                    },
                    "amenity_3": {
                        "value": "Rs "
                    },
                    "amenity_4": {
                        "value": "Rs "
                    },
                    "amenity_5": {
                        "value": "Rs "
                    },
                    "amenity_6": {
                        "value": "Rs "
                    }
                },
                "final_valuation": {
                    "fair_market_value_on_date": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "
                    },
                    "fair_market_value_on_completion": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                    "distressed_sale_value": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                    "valuation_as_per_guideline": {
                        "as_per_actual": "Rs ",
                        "as_per_document_provided": "Rs ",
                        "as_per_approved_plan": "Rs "

                    },
                }
            }
        }

        self.suffix_mapping = {
            "property_details": {
                "location_detail": {
                    "distance_from_city_center": " KM"
                }
            },
            "technical_details": {
                "plot_dimensons": {
                    "north": {
                        "as_per_actual": " Ft.",
                        "as_per_document_provided": " Ft.",
                        "as_per_layout_plan": " Ft."
                    },
                    "south": {
                        "as_per_actual": " Ft.",
                        "as_per_document_provided": " Ft.",
                        "as_per_layout_plan": " Ft."
                    },
                    "east": {
                        "as_per_actual": " Ft.",
                        "as_per_document_provided": " Ft.",
                        "as_per_layout_plan": " Ft."
                    },
                    "west": {
                        "as_per_actual": " Ft.",
                        "as_per_document_provided": " Ft.",
                        "as_per_layout_plan": " Ft."
                    }
                },
                "land_area": {
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_layout_plan": " Sq.Ft."
                    }
                },
                "bua_detail": {
                    "basement_1": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "basement_2": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "ground_1": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "ground_2": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "ground_3": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "floor_1": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "floor_2": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "floor_3": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "floor_4": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "summation": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "non-rcc_1": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "non-rcc_2": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    },
                    "non-rcc_3": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "sbua_detail": {
                    "as_per_actual": " Sq.Ft.",
                    "as_per_document_provided": " Sq.Ft.",
                    "as_per_approved_plan": " Sq.Ft."
                },
                "additional_details": {
                    "construction_progress": "%",
                    "recommendation_for_funding": "%",
                    "age_of_property": " Years",
                    "residual_age_of_property": " Years",
                    "development_in_vicinity": "%"
                }
            },
            "property_value_assessment": {
                "land": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_layout_plan": " Sq.Ft."
                    }
                },
                "basement_1": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "basement_2": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "ground_1": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "ground_2": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "ground_3": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "floor_1": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "floor_2": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "floor_3": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "floor_4": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "non-rcc_1": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "non-rcc_2": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                },
                "non-rcc_3": {
                    "government_price": " /Sq.Ft.",
                    "consideration_price": " /Sq.Ft.",
                    "area": {
                        "as_per_actual": " Sq.Ft.",
                        "as_per_document_provided": " Sq.Ft.",
                        "as_per_approved_plan": " Sq.Ft."
                    }
                }
            }
        }

        for k, v in zip(self.property_value_assesment, self.sorted_property_value_assesment_map):
            self.data_json_map[k] = v
   
    def date_formatter(self, value=""):
        if isinstance(value,type(datetime)):
            # parts = value.split()

            # # Take the first part
            # formatted_value = parts[0]
            dt_object = datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S%z")

            return dt_object.strftime(" %d %b %Y")
        else:
            # Split the string by '-'
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', value)

            # Join the extracted date portions with '-'
            formated_value = ' - '.join(dates)

            if formated_value:
                return formated_value
            else :
                # Split the string by whitespace
                parts = value.split()

                # Take the first three parts and join them with whitespace
                formated_value = ' '.join(parts[:4])

                return formated_value
    
    def convert_to_title_case(self,string):
            # Check if the string is already in upper case
            if string.isupper():
                return string  # Return the string unchanged
            else:
                # Convert the string to title case
                return string.title()
            
    def string_formatter(self, string, prefix="", suffix=""):

        if type(string) == type({}):
            string = string.values()
            string = ' '.join([str(s) for s in string])

        string = str(string)
        string = string.replace("_", " ")
        string = self.convert_to_title_case(string)


        if len(string) == 0:
            # print(" empty string")
            return string

        return prefix + string + suffix

    def value_formatter(self, string, prefix="", suffix=""):

        if type(string) == type({}):
            string = string.values()
            string = ' '.join([str(s) for s in string])

        string = str(string)
        string = string.replace("_", " ")

        if len(string) == 0:
            # print(" empty string")
            return string
        
        string = self.convert_to_title_case(string)

        string = prefix + string + suffix

        v_styles = ParagraphStyle(name="Heading1", alignment=0,
                                  parent=styles['BodyText'],
                                  fontSize=8,
                                  leading=12,
                                  textColor=TEXT_HE)
        t = Preformatted(string, v_styles, dedent=0, maxLineLength=45)
        return t

    def long_value_formatter(self, string, prefix="", suffix=""):

        if type(string) == type({}):
            string = string.values()
            string = ' '.join([str(s) for s in string])

        string = str(string)
        string = string.replace("_", " ")


        if len(string) == 0:
            # print(" empty string")
            return string
        
        string = string.title()

        if string:
            string = prefix + string + suffix

        v_styles = ParagraphStyle(name="Heading1", alignment=0,
                                  parent=styles['BodyText'],
                                  fontSize=8,
                                  leading=12,
                                  textColor=TEXT_HE)
        t = Preformatted(string, v_styles, dedent=0, maxLineLength=105)
        return t

    def includes(self, lst, item):
        return item in lst

    def sort_BUA_keys(self, keys):
        order = [
            "basement",
            "ground",
            "floor",
            "non-rcc",
            "amenities",
            "summation",
        ]
        return sorted(
            keys,
            key=lambda key: order.index(key.split("_")[0])
        )
    
    def sort_PVA_sections(self, keys):
        order = [
            "land",
            "basement",
            "ground",
            "floor",
            "non-rcc",
            "amenities",
            "final",
        ]
        return sorted(
            keys,
            key=lambda key: order.index(key.split("_")[0])
        )

    def convert_object_to_configuration(self,input_string = ""):
        # Convert the input string to type counts
        type_counts = {"BS": 0, "GF": 0, "F": 0, "R": 0}
        parts = input_string.split(" + ")
        for part in parts:
            count, type_ = part.split()
            if type_ == "Non-RCC":
                type_ = "R"  # Change "Non-RCC" to "R"
            if type_ in type_counts:  # Ensure type exists in type_counts
                type_counts[type_] += int(count)

        # Filter out keys with count 0
        type_counts = {key: value for key, value in type_counts.items() if value != 0}

        # Define the desired order
        order = ["BS", "GF", "F", "R"]

        # Sort based on the order array
        sorted_types = sorted(type_counts.keys(), key=lambda x: order.index(x))

        # Create the configuration string
        configuration_string = ' + '.join(
            f"{type_counts[type]} {'Non-RCC' if type == 'R' else type}" 
            for type in sorted_types
        )

        return configuration_string

    def create_section_heading(self, section="", j_section=""):

        table_name_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=10,
            # backColor= red,
            leading=14,
            # borderPadding=(0,0,10,0)

        )

        section_image = self.section_images.get(
            j_section, basic_valuation_details)

        data = [
            [
                Image(section_image, width=12, height=12),
                Paragraph(f"{section}", table_name_styles),
                Paragraph("", table_name_styles),

            ]
        ]

        table_data = Table(data, colWidths=(20, 470, 80), rowHeights=(16))
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), ACCENT_BG),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (1, -1), TEXT_HE)]))

        return table_data

    def create_subsection_heading(self, subsection, j_subsection):

        table_name_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=0,  # 0=left, 1=center, 2=right
            fontSize=10,
            leading=14,

        )

        sub_section_image = self.subsection_images.get(j_subsection, land_area)

        data = [
            [
                # Image(sub_section_image, width=12, height=12),
                Paragraph(f"{subsection}", table_name_styles),
                Paragraph(f"", table_name_styles),
            ]
        ]

        table_data = Table(data, colWidths=(450, 120), rowHeights=(14))
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            # ('BACKGROUND', (0, 0), (0, 0), ACCENT_BG),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (1, -1), TEXT_HE)]))

        return table_data

    def create_subsection(self, data):
        table_data = Table(data, colWidths=(120, 165, 120, 165))

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # # ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
            ('TEXTCOLOR', (2, 0), (-1, -1), TEXT_HE),
        ]))

        return table_data

    def create_section(self, section=""):
        story = []
        j_section = self.data_json_map.get(section)
        # story.append(self.create_pdf_page_header())
        # story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section, j_section))
        story.append(Spacer(width=width, height=10))

        sub_sections = self.subsections.get(section, "")
        for subsection in sub_sections:

            j_subsection = self.data_json_map.get(subsection)

            data_dict = {}

            if section in ("Valuer Remarks", "Images"):
                data_dict = self.data.get(j_section, {})
            else:
                data_dict = self.data.get(j_section, {}).get(j_subsection, {})
            
            prefix_data = self.prefix_mapping.get(j_section, {}).get(j_subsection, {})
            suffix_data = self.suffix_mapping.get(j_section, {}).get(j_subsection, {})
            

            data = []

            for key, value in data_dict.items():

                prefix = prefix_data.get(key, "")
                suffix = suffix_data.get(key, "")

                
                # Use regular expression to extract numerical part
                numerical_part = re.search(r'\d+', key)

                if numerical_part:
                    key = numerical_part.group()    

                data.append([self.string_formatter(
                    key), self.long_value_formatter(value, prefix, suffix), "", ""])

            if data:
                story.append(self.create_subsection_heading(subsection, j_subsection))
                story.append(self.create_subsection(data))
            story.append(Spacer(width=width, height=8))

        return story
    
    def create_grid_subsection(self, data):
        table_data = Table(data, colWidths=(130, 135, 150, 155))

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
            ('TEXTCOLOR', (2, 0), (-1, -1), TEXT_HE),
        ]))

        return table_data

    def create_pva_subsection(self, data, ):
        table_data = Table(data, colWidths=(40, 30, 110, 80, 30, 95, 100, 75))

        table_data.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, black),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('SPAN', (0, 0), (1, 2)), #AREA 

            ('SPAN', (0, 3), (3, 3)),  # GAP Between AREA & PRICE

            ('SPAN', (0, 4), (1, 7)),  # PRICE
            ('SPAN', (4, 0), (4, 7)),  # Col Gap)
            ('SPAN', (2, 4), (2, 5)),  # GOVT PRICE
            ('SPAN', (3, 4), (3, 5)),  # GOVT PRICE VALUE
            ('SPAN', (2, 6), (2, 7)),  # Consideration  PRICE
            ('SPAN', (3, 6), (3, 7)),  # Consideration PRICE VALUE
            ('SPAN', (5, 0), (5, 1)),  # As per actual 
            ('SPAN', (5, 2), (7, 2)),  # GAP between as per  actual and Document
            ('SPAN', (5, 3), (5, 4)),  # As per Document
            ('SPAN', (5, 5), (7, 5)),  # GAP between as per  Document and layout or approved
            ('SPAN', (5, 6), (5, 7)),  # As per Layout or Approved

            # ('VALIGN', (-5, -1), (-3, -1), 'BOTTOM'),
            # ('ALIGN', (-5, -1), (-3, -1), 'RIGHT'),
            # ('SPAN', (-5, -1), (-3, -1)),
            # ('GRID', (-5, -1), (-3, -1), 0.5, red),

            ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
            ('TEXTCOLOR', (2, 0), (-1, -1), TEXT_HE),
        ]))

        return table_data
    
    def create_amenitites_subsection(self, data, title_span_point=1):
        table_data = Table(data, colWidths=(80, 70, 110, 60, 80, 60, 100))

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, black),

            ('TEXTCOLOR', (0, 0), (1, title_span_point), TEXT_HE),

            # ('VALIGN', (0, 0), (1, title_span_point), 'MIDDLE'),
            # ('ALIGN', (0, 0), (1, title_span_point), 'CENTER'),
            ('SPAN', (0, 0), (1, title_span_point)),

            # ('VALIGN', (-5, -1), (-3, -1), 'MIDDLE'),
            # ('ALIGN', (-5, -1), (-3, -1), 'CENTER'),
            ('SPAN', (-5, -1), (-3, -1)),
            # ('GRID', (-5, -1), (-3, -1), 0.5, red),

            ('SPAN', (5,0), (5, title_span_point)),

            ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
            ('TEXTCOLOR', (2, 0), (-1, -1), TEXT_HE),
        ]))

        return table_data

    def create_final_valation_subsection(self, data):
        table_data = Table(data, colWidths=(160, 135, 135, 135))

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
            ('TEXTCOLOR', (2, 0), (-1, -1), TEXT_HE),
        ]))

        return table_data

    def create_basic_valuation_details_section(self, section):
        story = []
        # section = "Basic Valuation Details"
        j_section = self.data_json_map.get(section)

        section_heading_name = section

        if j_section == "basic_valuation_detail":
            section_heading_name = "General Details"
        if j_section == "infrastructure_detail":
            section_heading_name = "Infrastructure Details"

        story.append(self.create_section_heading(section_heading_name, j_section))
        story.append(Spacer(width=width, height=10))

        string_formatter_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_ME
        )

        sub_sections = self.subsections.get(section, "")

        for subsection in sub_sections:

            j_subsection = self.data_json_map.get(subsection)

            data_dict = {}

            if section in ("Basic Valuation Details", "Infrastructure Support"):
                data_dict = self.data.get(j_section, {})

            prefix_data = self.prefix_mapping.get(
                j_section, {}).get(j_subsection, {})
            suffix_data = self.suffix_mapping.get(
                j_section, {}).get(j_subsection, {})

            data = []

            # Create an iterator for the dictionary keys
            iter_keys = iter(data_dict.keys())

            # Loop through the iterator in batches of 2
            for key1 in iter_keys:
                value1 = data_dict[key1]
                prefix_x = prefix_data.get(key1, "")
                suffix_x = suffix_data.get(key1, "")

                if key1 == "report_date":
                    value1 = self.date_formatter(value1)

                if key1 == "document_provided":
                    data.append([Paragraph(self.string_formatter(
                        key1), string_formatter_styles), self.long_value_formatter(value1, prefix_x, suffix_x), "", ""])
                    continue  # Skip pairing "line-3" with another key

                # Get the next key from the iterator
                key2 = next(iter_keys, None)


                if key2 is None:
                    # Handle case when there's only one key left
                    data.append([Paragraph(self.string_formatter(
                        key1), string_formatter_styles), self.value_formatter(value1, prefix_x, suffix_y), "", ""])
                    break  # Exit loop as there are no more keys

                value2 = data_dict[key2]
                prefix_y = prefix_data.get(key2, "")
                suffix_y = suffix_data.get(key2, "")


                if key2 == "report_date":
                    value2 = self.date_formatter(value2)

                if key2 == "document_provided":
                    value2 = data_dict[key2]
                    data.append([Paragraph(self.string_formatter(
                        key1), string_formatter_styles), self.value_formatter(value1, prefix_x, suffix_x), "", ""])
                    data.append([Paragraph(self.string_formatter(
                        key2), string_formatter_styles), self.long_value_formatter(value2, prefix_y, suffix_y), "", ""])
                    continue 

                data.append([Paragraph(self.string_formatter(
                            key1), string_formatter_styles), self.value_formatter(value1, prefix_x, suffix_x), Paragraph(self.string_formatter(
                                key2), string_formatter_styles), self.value_formatter(value2, prefix_y, suffix_y)])

            if data:
                story.append(self.create_subsection_heading(
                    subsection, j_subsection))
                story.append(self.create_subsection(data))
            story.append(Spacer(width=width, height=5))

        # story.append(Spacer(width=width, height=15))
        # story.append(self.create_pdf_page_footer())

        return story

    def create_property_details_section(self):
        story = []
        section = "Property Details"
        j_section = self.data_json_map.get(section)
        # story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section, j_section))
        story.append(Spacer(width=width, height=10))

        string_formatter_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_ME
        )
        string_formatter_styles_2 = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_HE
        )

        sub_sections = self.subsections.get(section, "")

        for subsection in sub_sections:

            j_subsection = self.data_json_map.get(subsection)

            data_dict = self.data.get(j_section, {}).get(j_subsection, {})

            prefix_data = self.prefix_mapping.get(
                j_section, {}).get(j_subsection, {})
            suffix_data = self.suffix_mapping.get(
                j_section, {}).get(j_subsection, {})

            data = []

            if j_subsection == "schedule_detail":
                data.append(["", Paragraph(self.string_formatter("as_per_site_visit"), string_formatter_styles), Paragraph(self.string_formatter(
                            "as_per_legal_document"), string_formatter_styles), ""])

            # Create an iterator for the dictionary keys
            iter_keys = iter(data_dict.keys())
            # key2 = next(iter_keys, None)

            for key1 in iter_keys:

                key2 = next(iter_keys, None)

                value1 = data_dict[key1]

                if key2 is None:
                    data.append([Paragraph(self.string_formatter(
                            key1), string_formatter_styles_2), "", "", ""])

                    nested_iter_keys = iter(value1.keys())

                    for k1 in nested_iter_keys:
                        k2 = next(nested_iter_keys, None)
                        v1 = value1[k1]

                        if k2 is None:
                            data.append([Paragraph(self.string_formatter(
                                        k1), string_formatter_styles), self.value_formatter(v1), "", ""])
                            break

                        v2 = value1[k2]

                        data.append([Paragraph(self.string_formatter(
                                    k1), string_formatter_styles), self.value_formatter(v1), Paragraph(self.string_formatter(
                                        k2), string_formatter_styles), self.value_formatter(v2)])
                    break

                if key1 == "boundary_matching":
                    data.append(["","","",""])

                value2 = data_dict[key2]
                prefix_x = prefix_data.get(key1, "")
                suffix_x = suffix_data.get(key1, "")
                prefix_y = prefix_data.get(key2, "")
                suffix_y = suffix_data.get(key2, "")

                if type(value1) == type({}):
                    # print("keys", key1, key2)
                    long_keys = ["postal_address", "address_as_document"]
                    if self.includes(long_keys, key1):
                        if key1 == "postal_address":
                            key1 = "Postal Address of the Applicant"
                        data.append([Paragraph(self.string_formatter(key1), string_formatter_styles),
                                    self.long_value_formatter(value1, prefix_x, suffix_x), "", ""])

                    elif key1 in ("north_of_property", "south_of_property", "west_of_property", "east_of_property"):
                        data.append([Paragraph(self.string_formatter(
                                    key1), string_formatter_styles), self.value_formatter(value1["as_per_site_visit"]), self.value_formatter(value1["as_per_legal_document"]), ""])

                    else:
                        data.append([Paragraph(self.string_formatter(
                            key1), string_formatter_styles_2), "", "", ""])

                        nested_iter_keys = iter(value1.keys())

                        for k1, v1 in nested_iter_keys:
                            k2 = next(nested_iter_keys, None)
                            v1 = value1[k1]

                            if k2 is None:

                                data.append([Paragraph(self.string_formatter(
                                            k1), string_formatter_styles), self.value_formatter(v1),"", ""])
                                break

                            v2 = value1[k2]

                            data.append([Paragraph(self.string_formatter(
                                        k1), string_formatter_styles), self.value_formatter(v1), Paragraph(self.string_formatter(
                                            k2), string_formatter_styles), self.value_formatter(v2)])

                else:
                    if key2 is None:
                        # Handle case when there's only one key left
                        data.append([Paragraph(self.string_formatter(
                            key1), string_formatter_styles), self.value_formatter(value1, prefix_x, suffix_x), "", ""])
                        break  # Exit loop as there are no more keys

                    data.append([Paragraph(self.string_formatter(
                                key1), string_formatter_styles), self.value_formatter(value1, prefix_x, suffix_x), Paragraph(self.string_formatter(
                                    key2), string_formatter_styles), self.value_formatter(value2, prefix_y, suffix_y)])

                if type(value2) == type({}):
                    # print("keys", key1, key2)
                    long_keys = ["postal_address", "address_as_document"]
                    if self.includes(long_keys, key2):
                        data.append([Paragraph(self.string_formatter(key2), string_formatter_styles),
                                    self.long_value_formatter(value2, prefix_x, suffix_x), "", ""])

                    elif key2 in ("north_of_property", "south_of_property", "west_of_property", "east_of_property"):
                        data.append([Paragraph(self.string_formatter(
                                    key2), string_formatter_styles), self.value_formatter(value2["as_per_site_visit"]), self.value_formatter(value2["as_per_legal_document"]), ""])

                    else:
                        data.append([Paragraph(self.string_formatter(
                            key2), string_formatter_styles), "", "", ""])

                        nested_iter_keys = iter(value2.keys())

                        for k1, v1 in nested_iter_keys:
                            k2 = next(nested_iter_keys, None)

                            if k2 is None:
                                v1 = value1[k1]

                                data.append([Paragraph(self.string_formatter(
                                            k1), string_formatter_styles), self.value_formatter(v1),"", ""])
                                break

                            v2 = value1[k2]

                            data.append([Paragraph(self.string_formatter(
                                        k1), string_formatter_styles), self.value_formatter(v1), Paragraph(self.string_formatter(
                                            k2), string_formatter_styles), self.value_formatter(v2)])

            if data:
                story.append(self.create_subsection_heading(
                    subsection, j_subsection))
                story.append(self.create_subsection(data))
            story.append(Spacer(width=width, height=5))

        return story

    def create_building_details_section(self, section):
        story = []
        j_section = self.data_json_map.get(section)
        # story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section, j_section))
        story.append(Spacer(width=width, height=10))

        string_formatter_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_ME
        )

        sub_sections = self.subsections.get(section, "")

        for subsection in sub_sections:

            j_subsection = self.data_json_map.get(subsection)
            data_dict = self.data.get(j_section, {})

            prefix_data = self.prefix_mapping.get(
                j_section, {}).get(j_subsection, {})
            suffix_data = self.suffix_mapping.get(
                j_section, {}).get(j_subsection, {})

            data = []
            # Create an iterator for the dictionary keys
            iter_keys = iter(data_dict.keys())

            # Loop through the iterator in batches of 2
            for key1 in iter_keys:
                value1 = data_dict[key1]
                prefix_x = prefix_data.get(key1, "")
                suffix_x = suffix_data.get(key1, "")


                if type(value1) == type({}):
                    nested_iter_keys = iter(value1.keys())

                    if j_subsection == key1:

                        for k1 in nested_iter_keys:
                            v1 = value1[k1]
                            k2 = next(nested_iter_keys, None)


                            if k1 == "plan_validty":
                                v1 = self.date_formatter(v1)

                            if k2 is None:
                                data.append([Paragraph(self.string_formatter(
                                    k1), string_formatter_styles), self.value_formatter(v1, prefix_x, suffix_x), "", ""])
                                break

                            v2 = value1[k2]


                            if k2 == "plan_validty":
                                v2 = self.date_formatter(v2)


                            data.append([Paragraph(self.string_formatter(
                                        k1), string_formatter_styles), self.value_formatter(v1, prefix_x, suffix_x), Paragraph(self.string_formatter(
                                            k2), string_formatter_styles), self.value_formatter(v2)])

            if data:
                story.append(self.create_subsection_heading(
                    subsection, j_subsection))
                story.append(self.create_subsection(data))
            story.append(Spacer(width=width, height=5))

        return story

    def create_technical_details_section_2(self):
        story = []
        section = "Technical Details"
        j_section = self.data_json_map.get(section)
        # story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section, j_section))
        story.append(Spacer(width=width, height=10))

        string_formatter_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_ME
        )

        string_formatter_styles_2 = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_HE
        )

        sub_sections = self.subsections.get(section, "")

        for subsection in sub_sections:

            j_subsection = self.data_json_map.get(subsection)

            data_dict = self.data.get(j_section, {}).get(j_subsection, {})

            prefix_data = self.prefix_mapping.get(
                j_section, {}).get(j_subsection, {})
            suffix_data = self.suffix_mapping.get(
                j_section, {}).get(j_subsection, {})

            data = []

            if j_subsection == "additional_details": 

                # Create an iterator for the dictionary keys
                iter_keys = iter(data_dict.keys())

                for key1 in iter_keys:

                    value1 = data_dict[key1]
                    prefix_x = prefix_data.get(key1, "")
                    suffix_x = suffix_data.get(key1, "")

                    if key1 in ("municipal_notification","community_sensitivity","progress_in_words","market_feedback"):
                        data.append([Paragraph(self.string_formatter(key1), string_formatter_styles),
                                    self.long_value_formatter(value1, prefix_x, suffix_x), "", ""])
                        continue

                    if type(value1) == type({}):
                        data.append(["", "", "", ""])

                        data.append([Paragraph(self.string_formatter(
                            key1), string_formatter_styles_2), "", "", ""])

                        nested_iter_keys = iter(value1.keys())

                        for k1 in nested_iter_keys:
                            k2 = next(nested_iter_keys, None)

                            v1 = value1[k1]

                            if k1 == "executed_on":
                                v1 = self.date_formatter(v1)

                            if k2 is None:

                                data.append([Paragraph(self.string_formatter(
                                            k1), string_formatter_styles), self.value_formatter(v1), "", ""])
                                break

                            v2 = value1[k2]

                            if k2 == "executed_on":
                                v2 = self.date_formatter(v2)

                            data.append([Paragraph(self.string_formatter(
                                        k1), string_formatter_styles), self.value_formatter(v1), Paragraph(self.string_formatter(
                                            k2), string_formatter_styles), self.value_formatter(v2)])

                        data.append(["", "", "", ""])
                        continue

                    key2 = next(iter_keys, None)

                    print("keys ------------------ -- ---- - -- - --", key1, key2)

                    if key2 is None:
                        data.append([Paragraph(self.string_formatter(
                            key1), string_formatter_styles), self.value_formatter(value1, prefix_x, suffix_x), "", ""])
                        break

                    value2 = data_dict[key2]
                    prefix_y = prefix_data.get(key2, "")
                    suffix_y = suffix_data.get(key2, "")

                    if key2 in ("municipal_notification","community_sensitivity","progress_in_words","market_feedback"):
                        data.append([Paragraph(self.string_formatter(key2), string_formatter_styles),
                                    self.long_value_formatter(value2, prefix_x, suffix_x), "", ""])
                        continue

                    if type(value2) == type({}):

                        data.append(["", "", "", ""])

                        data.append([Paragraph(self.string_formatter(
                            key2), string_formatter_styles_2), "", "", ""])

                        nested_iter_keys = iter(value2.keys())

                        for k1 in nested_iter_keys:
                            k2 = next(nested_iter_keys, None)

                            v1 = value2[k1]

                            if k1 == "executed_on":
                                v1 = self.date_formatter(v1)

                            if k2 is None:

                                data.append([Paragraph(self.string_formatter(
                                            k1), string_formatter_styles), self.value_formatter(v1), "", ""])
                                break

                            v2 = value2[k2]

                            if k2 == "executed_on":
                                v2 = self.date_formatter(v2)

                            data.append([Paragraph(self.string_formatter(
                                        k1), string_formatter_styles), self.value_formatter(v1), Paragraph(self.string_formatter(
                                            k2), string_formatter_styles), self.value_formatter(v2)])

                        data.append(["", "", "", ""])
                        continue

                    else:
                        data.append([Paragraph(self.string_formatter(
                                    key1), string_formatter_styles), self.value_formatter(value1, prefix_x, suffix_x), Paragraph(self.string_formatter(
                                        key2), string_formatter_styles), self.value_formatter(value2, prefix_y, suffix_y)])

            if data:
                story.append(self.create_subsection_heading(
                    subsection, j_subsection))
                story.append(self.create_grid_subsection(data))
                story.append(Spacer(width=width, height=5))


        return story
    
    def create_technical_details_section(self):
        story = []
        section = "Technical Details"
        j_section = self.data_json_map.get(section)
        # story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section, j_section))
        story.append(Spacer(width=width, height=10))

        string_formatter_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_ME
        )

        string_formatter_styles_2 = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_HE
        )

        sub_sections = self.subsections.get(section, "")

        for subsection in sub_sections:

            j_subsection = self.data_json_map.get(subsection)

            data_dict = self.data.get(j_section, {}).get(j_subsection, {})

            prefix_data = self.prefix_mapping.get(
                j_section, {}).get(j_subsection, {})
            suffix_data = self.suffix_mapping.get(
                j_section, {}).get(j_subsection, {})

            data = []

            if j_subsection in ("plot_dimensons", "land_area"):
                if j_subsection =="land_area":
                    data.append([Paragraph(self.string_formatter("holding_type"), string_formatter_styles), Paragraph(
                        self.string_formatter(str(data_dict["holding_type"]), "", ""), string_formatter_styles_2), "", ""])
                    
                data.append(["", Paragraph(self.string_formatter("as_per_actual"), string_formatter_styles), Paragraph(self.string_formatter(
                            "as_per_document_provided"), string_formatter_styles), Paragraph(self.string_formatter(
                                "as_per_layout_plan"), string_formatter_styles)])

                # Create an iterator for the dictionary keys
                iter_keys = iter(data_dict.keys())

                for key1 in iter_keys:
                    value1 = data_dict[key1]

                    if key1 == "holding_type":
                        continue

                    # print("value1", value1)

                    prefix_x = prefix_data.get(key1, "")
                    suffix_x = suffix_data.get(key1, "")
                    # print("suffix_x", suffix_x)

                    if type(value1) == type({}):
                        match_value = ""

                        if value1["is_match"] == True:
                            match_value = "Match"
                        else:
                            match_value = "No Match"

                        first_col_value = f"{key1} (" + match_value + ")"

                        data.append([Paragraph(self.string_formatter(
                                    first_col_value), string_formatter_styles), self.value_formatter(value1["as_per_actual"], prefix_x, suffix_x["as_per_actual"]), self.value_formatter(value1["as_per_document_provided"], prefix_x, suffix_x["as_per_document_provided"]), self.value_formatter(value1["as_per_layout_plan"], prefix_x, suffix_x["as_per_layout_plan"])])
                    else:
                        data.append([Paragraph(self.string_formatter(
                            key1), string_formatter_styles), self.value_formatter(value1, prefix_x, suffix_x), "", ""])

            elif j_subsection == "bua_detail":

                config_value = self.convert_object_to_configuration(data_dict["configuration"])


                data.append([Paragraph(self.string_formatter("configuration"), string_formatter_styles), Paragraph(
                    self.string_formatter(config_value, "", ""), string_formatter_styles_2), "", ""])

                data.append(["", Paragraph(self.string_formatter("as_per_actual"), string_formatter_styles), Paragraph(self.string_formatter(
                            "as_per_document_provided"), string_formatter_styles), Paragraph(self.string_formatter(
                                "as_per_approved_plan"), string_formatter_styles)])

                del data_dict["configuration"]

                old_keys = data_dict.keys()
                sorted_keys = self.sort_BUA_keys(old_keys)

                iter_keys = iter(sorted_keys)

                for key1 in iter_keys:

                    if key1 == "configuration":
                        continue

                    value1 = data_dict[key1]

                    prefix_x = prefix_data.get(key1, "")
                    suffix_x = suffix_data.get(key1, "")

                    match_value = ""

                    if value1["is_match"] == True:
                        match_value = "Match"
                    else:
                        match_value = "No Match"

                    first_col_value = f"{key1} ({match_value})"

                    data.append([Paragraph(self.string_formatter(
                                first_col_value), string_formatter_styles), self.value_formatter(value1["as_per_actual"], prefix_x, suffix_x["as_per_actual"]), self.value_formatter(value1["as_per_document_provided"], prefix_x, suffix_x["as_per_document_provided"]), self.value_formatter(value1["as_per_approved_plan"], prefix_x, suffix_x["as_per_approved_plan"])])

            elif j_subsection == "sbua_detail":
                data.append(["", Paragraph(self.string_formatter("as_per_actual"), string_formatter_styles), Paragraph(self.string_formatter(
                            "as_per_document_provided"), string_formatter_styles), Paragraph(self.string_formatter(
                                "as_per_approved_plan"), string_formatter_styles)])

                match_value = ""

                if data_dict["is_match"] == True:
                    match_value = "Match"
                else:
                    match_value = "No Match"

                first_col_value = f"Super Buildup Area (" + match_value + ")"

                data.append([Paragraph(self.string_formatter(
                            first_col_value), string_formatter_styles), self.value_formatter(data_dict["as_per_actual"], prefix_x, suffix_x["as_per_actual"]), self.value_formatter(data_dict["as_per_document_provided"], prefix_x, suffix_x["as_per_document_provided"]), self.value_formatter(data_dict["as_per_approved_plan"], prefix_x, "Sq. Ft.")])

            if data:
                story.append(self.create_subsection_heading(
                    subsection, j_subsection))
                story.append(self.create_grid_subsection(data))
            story.append(Spacer(width=width, height=10))

        return story

    def create_pva_section(self, section):
        story = []
        j_section = self.data_json_map.get(section)
        story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section, j_section))
        story.append(Spacer(width=width, height=10))

        string_formatter_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_ME
        )

        string_formatter_styles_2 = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=8,
            leading=12,
            textColor=TEXT_HE
        )
        
        string_formatter_styles_3 = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=10,
            leading=12,
            textColor=TEXT_HE
        )
        
        string_formatter_styles_4 = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=1,
            fontSize=10,
            leading=12,
            textColor=TEXT_HE
        )

        sub_sections = self.subsections.get(section, "")

        for subsection in sub_sections:

            j_subsection = self.data_json_map.get(subsection)

            data_dict = self.data.get(j_section, {}).get(j_subsection, {})

            prefix_data = self.prefix_mapping.get(
                j_section, {}).get(j_subsection, {})
            suffix_data = self.suffix_mapping.get(
                j_section, {}).get(j_subsection, {})
            

            per_sq_ft_suffix = " / Sq. Ft."
            sq_ft_suffix = " Sq. Ft."
            ft_suffix = " Ft."
            
            rupees_prefix = "Rs "

            title_govt_price = "Govt Price"
            title_fair_market_price ="Fair Market Price"

            data = []

            if j_subsection == "amenities":
                title_span_point = 1
                total = 0
                data.append([Paragraph(self.string_formatter("Amenities"), string_formatter_styles_4), "", Paragraph(self.string_formatter("Item Name"), string_formatter_styles), Paragraph(self.string_formatter(
                            "qauntity"), string_formatter_styles), Paragraph(self.string_formatter("per unit value"), string_formatter_styles), "", Paragraph(self.string_formatter("Total"), string_formatter_styles_4)])
                
                # Create an iterator for the dictionary keys
                iter_keys = iter(data_dict.keys())

                for key1 in iter_keys:

                    value1 = data_dict[key1]
                    prefix_x = prefix_data.get(key1, "")
                    suffix_x = suffix_data.get(key1, "")

                    quantity = 1
                    total_value = int(value1["value"]) * quantity
                    title_span_point += 1
                    total = total + int(value1["value"])

                    data.append(["", "", Paragraph(self.string_formatter(value1["item_name"]), string_formatter_styles), Paragraph(self.string_formatter(quantity), string_formatter_styles), Paragraph(self.string_formatter(value1["value"], rupees_prefix), string_formatter_styles), "", Paragraph(self.string_formatter(
                        total_value, rupees_prefix), string_formatter_styles_2)])

                data.append(["", "", Paragraph(self.string_formatter("Total"), string_formatter_styles_4), "", "", "", Paragraph(self.string_formatter(
                    total, rupees_prefix), string_formatter_styles_2)])

            elif j_subsection == "final_valuation":

                data.append(["", Paragraph(self.string_formatter("as_per_actual"), string_formatter_styles), Paragraph(self.string_formatter(
                            "as_per_document_provided"), string_formatter_styles), Paragraph(self.string_formatter(
                                "as_per_plan"), string_formatter_styles)])
                #   Create an iterator for the dictionary keys
                iter_keys = iter(data_dict.keys())

                for key1 in iter_keys:

                    value1 = data_dict[key1]

                    prefix_x = prefix_data.get(key1, "")

                    data.append([Paragraph(self.string_formatter(f"Total {key1}"), string_formatter_styles),
                                self.value_formatter(
                                    value1["as_per_actual"], prefix_x["as_per_actual"]),
                                self.value_formatter(
                                    value1["as_per_document_provided"], prefix_x["as_per_document_provided"]),
                                 self.value_formatter(value1["as_per_approved_plan"], prefix_x["as_per_approved_plan"])])

            else:
                title_span_point = 8
                if j_subsection == "land":

                    area_as_per_actual = data_dict["area"]["as_per_actual"]
                    area_as_per_document_provided = data_dict["area"]["as_per_document_provided"]
                    area_as_per_layout_plan = data_dict["area"]["as_per_layout_plan"]

                    total_value_government_price_as_per_actual = data_dict["total_value_government_price"]["as_per_actual"]
                    total_value_government_price_as_per_document_provided = data_dict["total_value_government_price"]["as_per_document_provided"]
                    total_value_government_price_as_per_layout_plan = data_dict["total_value_government_price"]["as_per_layout_plan"]

                    total_value_fair_market_as_per_actual = data_dict["total_value_fair_market"]["as_per_actual"]
                    total_value_fair_market_as_per_document_provided = data_dict["total_value_fair_market"]["as_per_document_provided"]
                    total_value_fair_market_as_per_layout_plan = data_dict["total_value_fair_market"]["as_per_layout_plan"]

                    govt_price = data_dict["government_price"]
                    consideration_price = data_dict["consideration_price"]

                    data.append(
                                    [ 
                                        Paragraph(self.string_formatter("Area"), string_formatter_styles_4), 
                                        "",
                                        Paragraph(self.string_formatter("as_per_actual"), string_formatter_styles), 
                                        Paragraph(self.string_formatter(str(area_as_per_actual),"", sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        Paragraph(self.string_formatter("as_per_actual"), string_formatter_styles_3), 
                                        Paragraph(self.string_formatter(title_govt_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(str(total_value_government_price_as_per_actual),rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    
                    data.append(
                                    [ 
                                        "", 
                                        "",
                                        Paragraph(self.string_formatter("as_per_document_provided"), string_formatter_styles), 
                                        Paragraph(self.string_formatter(area_as_per_document_provided, "", sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        "",
                                        Paragraph(self.string_formatter(title_fair_market_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_fair_market_as_per_actual, rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    
                    data.append(
                                    [ 
                                        "", 
                                        "",
                                        Paragraph(self.string_formatter("as_per_layout_plan"), string_formatter_styles), 
                                        Paragraph(self.string_formatter(area_as_per_layout_plan,  "", sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        "",
                                        "",
                                        "",
                                     ]
                                )
                    data.append(
                                    [ 
                                        "", 
                                        "",
                                        "",
                                        "",
                                        "",
                                        Paragraph(self.string_formatter("as_per_document"), string_formatter_styles_3), 
                                        Paragraph(self.string_formatter(title_govt_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_government_price_as_per_document_provided, rupees_prefix), string_formatter_styles_2)
                                   ]
                                )
                    data.append(
                                    [ 
                                        Paragraph(self.string_formatter("price"), string_formatter_styles_4), 
                                        "", 
                                        Paragraph(self.string_formatter("Govt Price / Sq. Ft."), string_formatter_styles), 
                                        Paragraph(self.string_formatter(govt_price,  rupees_prefix, per_sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        "",
                                        Paragraph(self.string_formatter(title_fair_market_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_fair_market_as_per_document_provided, rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    data.append(
                                    [ 
                                        "", 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "",
                                        "",
                                        ""
                                     ]
                                )
                    data.append(
                                    [ 
                                        "", 
                                        "", 
                                        Paragraph(self.string_formatter("Consideration Price / Sq. Ft."), string_formatter_styles), 
                                        Paragraph(self.string_formatter(consideration_price, rupees_prefix, per_sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        Paragraph(self.string_formatter("As Per Layout"), string_formatter_styles_3), 
                                        Paragraph(self.string_formatter(title_govt_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_government_price_as_per_layout_plan,  rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    data.append(
                                    [ 

                                        "", 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "",
                                        Paragraph(self.string_formatter(title_fair_market_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_fair_market_as_per_layout_plan,  rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    
                else:

                    area_as_per_actual = data_dict["area"]["as_per_actual"]
                    area_as_per_document_provided = data_dict["area"]["as_per_document_provided"]
                    area_as_per_approved_plan = data_dict["area"]["as_per_approved_plan"]

                    total_value_government_price_as_per_actual = data_dict["total_value_government_price"]["as_per_actual"]
                    total_value_government_price_as_per_document_provided = data_dict["total_value_government_price"]["as_per_document_provided"]
                    total_value_government_price_as_per_approved_plan = data_dict["total_value_government_price"]["as_per_approved_plan"]

                    total_value_fair_market_as_per_actual = data_dict["total_value_fair_market"]["as_per_actual"]
                    total_value_fair_market_as_per_document_provided = data_dict["total_value_fair_market"]["as_per_document_provided"]
                    total_value_fair_market_as_per_approved_plan = data_dict["total_value_fair_market"]["as_per_approved_plan"]


                    govt_price = data_dict["government_price"]
                    consideration_price = data_dict["consideration_price"]

                    data.append(
                                    [ 
                                        Paragraph(self.string_formatter("Area"), string_formatter_styles_4), 
                                        "",
                                        Paragraph(self.string_formatter("as_per_actual"), string_formatter_styles), 
                                        Paragraph(self.string_formatter(str(area_as_per_actual), "", sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        Paragraph(self.string_formatter("as_per_actual"), string_formatter_styles_3), 
                                        Paragraph(self.string_formatter(title_govt_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(str(total_value_government_price_as_per_actual), rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    
                    data.append(
                                    [ 
                                        "", 
                                        "",
                                        Paragraph(self.string_formatter("as_per_document_provided"), string_formatter_styles), 
                                        Paragraph(self.string_formatter(area_as_per_document_provided, "", sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        "",
                                        Paragraph(self.string_formatter(title_fair_market_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_fair_market_as_per_actual, rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    
                    data.append(
                                    [ 
                                        "", 
                                        "",
                                        Paragraph(self.string_formatter("as_per_approved_plan"), string_formatter_styles), 
                                        Paragraph(self.string_formatter(area_as_per_approved_plan, "", sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        "",
                                        "",
                                        "",
                                     ]
                                )
                    data.append(
                                    [ 
                                        "", 
                                        "",
                                        "",
                                        "",
                                        "",
                                        Paragraph(self.string_formatter("as_per_document"), string_formatter_styles_3), 
                                        Paragraph(self.string_formatter(title_govt_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_government_price_as_per_document_provided, rupees_prefix), string_formatter_styles_2)
                                   ]
                                )
                    data.append(
                                    [ 
                                        Paragraph(self.string_formatter("price"), string_formatter_styles_4), 
                                        "", 
                                        Paragraph(self.string_formatter("Govt Price / Sq. Ft."), string_formatter_styles), 
                                        Paragraph(self.string_formatter(govt_price,  rupees_prefix, per_sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        "",
                                        Paragraph(self.string_formatter(title_fair_market_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_fair_market_as_per_document_provided, rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    data.append(
                                    [ 
                                        "", 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "",
                                        "",
                                        ""
                                     ]
                                )
                    data.append(
                                    [ 
                                        "", 
                                        "", 
                                        Paragraph(self.string_formatter("Consideration Price / Sq Ft."), string_formatter_styles), 
                                        Paragraph(self.string_formatter(consideration_price,  rupees_prefix, per_sq_ft_suffix), string_formatter_styles_2), 
                                        "",
                                        Paragraph(self.string_formatter("As Per Approved"), string_formatter_styles_3), 
                                        Paragraph(self.string_formatter(title_govt_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_government_price_as_per_approved_plan, rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    data.append(
                                    [ 

                                        "", 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "",
                                        Paragraph(self.string_formatter(title_fair_market_price), string_formatter_styles), 
                                        Paragraph(self.string_formatter(total_value_fair_market_as_per_approved_plan,rupees_prefix), string_formatter_styles_2)
                                    ]
                                )
                    

            data_2 = []
            if data:
                data_2.append(self.create_subsection_heading(
                    subsection, j_subsection))
                data_2.append(Spacer(width=width, height=(5)))
                if j_subsection == "amenities":
                    data_2.append(self.create_amenitites_subsection(
                        data, title_span_point))
                elif j_subsection == "final_valuation":
                    data_2.append(self.create_final_valation_subsection(data))
                else:
                    data_2.append(self.create_pva_subsection(data))

            data_2.append(Spacer(width=width, height=10))
            story.append(KeepTogether(data_2))

        return story

    def create_images_section(self, section, images_data):
        story = []

        story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section))
        story.append(Spacer(width=width, height=15))
        story.append(self.create_subsection_heading("All Images", ""))

        data = []
        all_images = []

        for img_number, img_data in enumerate(images_data):

            if img_data["filename"].split(".")[-1] not in ("jpg", "png", "jpeg"):
                continue

            image_name = "report_image_" + str(img_number)

            image_url = img_data["url"]

            image_data = requests.get(image_url)

            with open(f'{os.getcwd()}/assets/pdf_dynamic_images/{self.valle_lead_number}/{image_name}.jpg', 'wb') as f:
                f.write(image_data.content)

            all_images.append(
                f'{os.getcwd()}/assets/pdf_dynamic_images/{self.valle_lead_number}/{image_name}.jpg')

        data = self.destribute_images(all_images)

        table_data = Table(data, colWidths=(25, 260, 250), rowHeights=200)
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # ('BACKGROUND', (0, 0), (2, 0), ACCENT_BG),
            # ('BACKGROUND', (0, 0), (-1, -1), BACKGROUND),
            # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            # ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
            # ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
            # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),
            # ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        story.append(table_data)

        story.append(Spacer(width=width, height=15))

        return story

    def destribute_seal_sign_images(self, images):

        data = []

        width = 137.5
        height = 105
        

        if len(images) % 2 == 0:
            for img in range(0, len(images), 2):
                data.append(["", Image(images[img], width=width, height=height),"",  Image(
                    images[img+1], width=width, height=height)])
        else:
            for img in range(0, len(images)-1, 2):
                data.append(["", Image(images[img], width=width, height=height), "", Image(
                    images[img+1], width=width, height=height)])
            data.append(["", Image(images[-1], width=width, height=height), "", ""])

        return data
    
    def destribute_images(self, images):

        data = []

        width = 237.5
        height = 155
        
        if len(images) % 2 == 0:
            for img in range(0, len(images), 2):
                data.append(["", Image(images[img], width=width, height=height), Image(
                    images[img+1], width=width, height=height)])
        else:
            for img in range(0, len(images)-1, 2):
                data.append(["", Image(images[img], width=width, height=height),  Image(
                    images[img+1], width=width, height=height)])
            data.append(["", Image(images[-1], width=width, height=height), ""])

        return data

    def create_valuer_details_section(self, section):
        story = []
        story.append(self.create_section_heading(section))
        story.append(Spacer(width=width, height=10))

        valuer_detail = self.data.get("valuer_detail")

        data_d = [["", "Valuer Name", valuer_detail.get(
            "first_name", "") + " " + valuer_detail.get("last_name", "")]]

        table_data_d = Table(data_d, colWidths=(25, 160, 250))

        table_data_d.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
            ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_HE),
        ]))

        story.append(table_data_d)
        story.append(Spacer(width=width, height=10))


        story.append(self.create_subsection_heading("Seal and Signature", ""))

        data = []
        all_images = []

        try:
            os.mkdir(
                f"assets/pdf_dynamic_images/{self.valle_lead_number}")
        except:
            print("Directory Already Exists")

        valuer_seal_url = valuer_detail.get("seal_doc").get("url")
        valuer_sign_url = valuer_detail.get("sign_doc").get("url")

        if valuer_seal_url:
            image_data = requests.get(valuer_seal_url)
            with open(f'{os.getcwd()}/assets/pdf_dynamic_images/{self.valle_lead_number}/valuer_seal.jpg', 'wb') as f:
                f.write(image_data.content)
            all_images.append(
                f'{os.getcwd()}/assets/pdf_dynamic_images/{self.valle_lead_number}/valuer_seal.jpg')

        if valuer_sign_url:
            image_data = requests.get(valuer_sign_url)
            with open(f'{os.getcwd()}/assets/pdf_dynamic_images/{self.valle_lead_number}/valuer_sign.jpg', 'wb') as f:
                f.write(image_data.content)
            all_images.append(
                f'{os.getcwd()}/assets/pdf_dynamic_images/{self.valle_lead_number}/valuer_sign.jpg')

        data = self.destribute_seal_sign_images(all_images)

        table_data = Table(data, colWidths=(25, 150, 100, 150), rowHeights=150)
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # ('BACKGROUND', (0, 0), (2, 0), ACCENT_BG),
            # ('BACKGROUND', (0, 0), (-1, -1), BACKGROUND),
            # ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            # ('ALIGN', (2, 0), (-1, -2), 'CENTRE'),
            # ('ALIGN', (0, 1), (-3, -1), 'RIGHT'),
            # ('VALIGN', (0, 1), (-3, -1), 'CENTRE'),
            # ('ALIGN', (0, 0), (-2, -2), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        story.append(table_data)

        story.append(Spacer(width=width, height=15))
        # story.append(self.create_pdf_page_footer())

        return story

    def create_pdf_page(self, data=None):
        section_basic_valuation = self.create_basic_valuation_details_section(
            "Basic Valuation Details")
        section_property_details = self.create_property_details_section()
        section_building_details = self.create_building_details_section(
            "Building Details")
        section_infrastructure_support = self.create_basic_valuation_details_section(
            "Infrastructure Support")
        section_technical_details = self.create_technical_details_section()
        section_technical_details_2 = self.create_technical_details_section_2()
        section_property_value_assessement = self.create_pva_section(
            "Property Value Assessment")
        section_valuer_remarks = self.create_section(
            "Valuer Remarks")
        section_valuer_declaration = self.create_section(
            "Valuer Declaration")
        # section_valuer_details = self.create_valuer_details_section(
        #     "Valuer Details")
        # images_data = self.data.get("images")
        # if images_data:
        #     section_images = self.create_images_section("Images", images_data)

        story = []
        story.append(KeepTogether(section_basic_valuation))
        story.append(KeepTogether(section_property_details))
        story.append(KeepTogether(section_building_details))
        story.append(KeepTogether(section_infrastructure_support))
        story.append(KeepTogether(section_technical_details))
        story.append(KeepTogether(section_technical_details_2))
        story.append(KeepTogether(section_property_value_assessement))
        # story.append(KeepTogether(section_valuer_remarks,
        #              section_valuer_declaration))


        story.append(KeepTogether(section_valuer_remarks))

        story.append(KeepTogether(section_valuer_declaration))

        # story.append(KeepTogether(section_valuer_details))
        # if images_data:
        #     # story.append(PageBreak())
        #     story.append(KeepTogether(section_images))

        return story

    def draw_page_background(self, canvas, doc):
        height = doc.height
        width = doc.width
        canvas.linearGradient(x0=0, y0=height, x1=width /
                              0.5, y1=0, colors=[self.start_color, self.end_color])

    def add_watermark(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 84)
        canvas.setFillGray(0.8, 0.35)
        canvas.rotate(45)
        canvas.drawCentredString(500, 65, 'TENTATIVE')
        canvas.restoreState()

    def generate_pdf(self, valle_lead_number="KA100725", user_id="RISHABH", insititute_lead_number="RANDOM_!", organisation_name="RANDOM2", tentative_report=False):

        self.valle_lead_number = valle_lead_number
        self.insititute_lead_number = insititute_lead_number
        self.organisation_name = organisation_name
        self.tentative_report = tentative_report

        self.get_data(self.valle_lead_number, user_id)

        try:
            self.data["basic_valuation_detail"]["loan_application_number"] = self.insititute_lead_number
        except Exception as e:
            print("Error while inserting data into basic_valuation_detail" + str(e))

        self.data["valuer_declaration"] = {"declaration": {
            "1. ": "Valle and the Service Provider Partner have no direct or indirect interest in the property.",
            "2.": "The valuation provided here is based on our best knowledge, ability and experience and is under prevailing market rates at the time of evaluation.",
            "3.": "This report is computer-generated and has been reviewed by above Valuer, rendering a wet signature unnecessary."
        }
        }

        self.pdf_report = BaseDocTemplate(
            self.buffer, pagesize=self.pagesize, title=f"{self.valle_lead_number}")

        self.frame_cover = Frame(
            self.pdf_report.leftMargin, self.pdf_report.bottomMargin,
            self.pdf_report.width, self.pdf_report.height + 35,
            id='normal'
        )

        # Create a PageTemplate with the Frame

        if self.tentative_report:
            self.page_template_cover = PageTemplate(
                id='cover_page', frames=[self.frame_cover], onPage=self.add_watermark)
        else:
            self.page_template_cover = PageTemplate(
                id='cover_page', frames=[self.frame_cover])

        # self.page_template = PageTemplate(id='index_page', frames=[
        #     self.frame_cover])

        self.pdf_report.addPageTemplates([self.page_template_cover])

        # self.pdf_report.onFirstPage = lambda canvas, doc: self.draw_page_background(
        #     canvas, doc)

        self.pdf_queue = []

        # PDF Pages
        pdf_page = self.create_pdf_page()
        self.pdf_queue.extend(pdf_page)

        # Build the PDF document
        global VALLE_LEAD_NEMBER
        VALLE_LEAD_NEMBER = self.valle_lead_number

        self.pdf_report.build(self.pdf_queue,  canvasmaker=FooterCanvas)

        self.buffer.seek(0)

        # Create a response with the PDF content type
        self.pdf_response = make_response(self.buffer.read())
        self.pdf_response.headers['Content-Disposition'] = 'inline; filename=dynamic_pdf.pdf'
        self.pdf_response.headers['Content-Type'] = 'application/pdf'

        # Delete The Temporary Directory
        try:
            shutil.rmtree(
                f"assets/pdf_dynamic_images/{self.valle_lead_number}")
        except:
            print("Unable to Delete Temporary Directory")

        return self.pdf_response


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.valle_lead_number = VALLE_LEAD_NEMBER

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            # if (self._pageNumber == 1):
            #     # self.draw_front_page_footer()
            # # elif (self._pageNumber == 2):
            # #     self.draw_index_header(page_count)
            # #     self.draw_index_footer(page_count)
            # else:
            self.draw_header()
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
                           colWidths=(50, 160, 50, 160), rowHeights=50)  # , cornerRadii=(8, 8, 8, 8))

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTRE'),
            # ("BACKGROUND", (0, 0), (-1, -1), colors.white),
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

    def draw_header(self):

        data = [[Image(valle_logo_black, width=50, height=20),
                 Image(report, width=99, height=29),
                 Image(bankImage, width=50, height=24)]]

        table_data = Table(data, colWidths=(70, 420, 80), rowHeights=30)

        table_data.setStyle(TableStyle([
            # ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (-2, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (1, 0), (-2, -1), 'BOTTOM'),
            ('BOTTOMPADDING', (1, 0), (-2, -1), -5),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEBELOW', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        # Draw the table_data on the canvas
        table_data.wrapOn(self, height-50, 10)
        # Here 20 is left margin , and (height-40 ) is height of table
        table_data.drawOn(self, 20, height-35)

    def draw_footer(self, page_count):
        page = self._pageNumber
        content = f""" This document contains sensitive information. Share this document with essential personal only. """

        # global VALLE_LEAD_NEMBER
        # self.valle_lead_number = VALLE_LEAD_NEMBER

        lead_number_styles = ParagraphStyle(
            'CenteredStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=1,
            fontSize=10,
            backColor=ACCENT_BG,
            textColor=ACCENT,
            leading=16,
            # borderRadius=(3, 3),
            borderColor=ACCENT_BG,
            borderWidth=1,
            padding=(5, 2)
        )

        content_style = ParagraphStyle(
            'CenteredStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=0,  # 0=left, 1=center, 2=right
            fontSize=8
        )

        page_number_styles = ParagraphStyle(
            'CenteredStyle',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=1,
            fontSize=11,
            backColor=ACCENT,
            textColor="white",
            leading=14,
            borderRadius=(2, 2),
            borderColor=ACCENT,
            borderWidth=1,
            borderPadding=(2, 0, 2, 0)
        )

        data = [[Image(shield, width=9, height=10.75),
                Paragraph(content, content_style),
                Paragraph(f"{self.valle_lead_number}", lead_number_styles),
                Paragraph(f"{page}", page_number_styles)]]

        table = Table(data, colWidths=(15, 400, 100, 35), rowHeights=35)

        # Apply styles to the table if needed
        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
            # ('GRID', (1, 0), (-2, -1), 1, black),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('LINEABOVE', (0, 0), (-1, -1), 1, ACCENT),
            ('TEXTCOLOR', (0, 0), (1, -1), black)])

        table.setStyle(style)

        # Draw the table on the canvas
        table.wrapOn(self, 0, 0)
        table.drawOn(self, 30, 0)
