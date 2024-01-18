import os
import json
import requests
import shutil

from flask import make_response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, HexColor
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Preformatted, Spacer, Frame, PageTemplate, Image, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
# from generator.footer_generator import FooterCanvas


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
amenities = "./assets/images/Amenities.jpeg"
additional_details = "./assets/images/additional_details.jpeg"
basic_details = "./assets/images/basic_details.jpeg"
bua_details = "./assets/images/BUA Details.png"
construction_details = "./assets/images/Construction details.jpg"
final_valuation = "./assets/images/Final Valuation.jpeg"
ground_floor = "./assets/images/ground_floor.jpeg"
infrastructure_support = "./assets/images/Infrastructure Support.jpg"
land_area = "./assets/images/Land area.jpg"
loaction_details = "./assets/images/Land area.jpg"
plan_details = "./assets/images/Plan details.jpg"
plot_details = "./assets/images/Plot Details.jpeg"
remarks = "./assets/images/Remarks.jpeg"
sbua_details = "./assets/images/SBUA Details.png"
schedule_details = "./assets/images/Schedule Details.jpg"
seal_signature_details = "./assets/images/seal_&_signature.jpeg"

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

    def get_data(self, valle_lead_number):

        url = "https://console.navanc.com/report/nis-view-report"
        # url = "https://valle-be-api.dev.navanc.com/report/nis-view-report"

        payload = json.dumps({
            # "token":"eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9kZXYtc2hlN2ZlaGowYTBnYTh6eS51cy5hdXRoMC5jb20vIn0..7fGLOTHktVWJowPg.yGUOzJFPlqhCyhA1NqQK_WsR8a12KdPq6r8FtPqfA0sajC_YTBnQ5VCEq1I5VJGZXH4EyGelCliEhxUQhNzywP1fdVdDX-qn2oI7c3gErcs9Zu975TKVkirSmuPZ3Ayc9-EuW0iQUDW6KxKdnDeJFGI8DLI7VGlEaL4YcyDatcZzfm_MDKUak7evASWWPPTDEIcJ2W0FsnHy-MI70iUsxBueEzaA3ywfU8QU5wrPWxBOTcpfN0EA6OSX8DVnq02ednMUACJwnbAIQBMno-TQZcx7uy3YCuXSAbvpWfNT1JuSOp-wb8RhnhAp7hxAockYCh9GzU6KeaiWN1S-43S5FmVAZ9PqIZ-ijgna5WnX0sY62jPwqT625wAjiIuPWx8.Cio4a8i6BnscYbydGxbWzg",
            "token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9uYXZhbmMtcHJvZC51cy5hdXRoMC5jb20vIn0..GnvKKCXI0hVnho1f.xW7rGqqDBbFq99Gy00ImOJdZ1bQxzlGyGn3AWFKxwOE_LZKAVOz1Q2y65dvhSPdLzHnk4zNFyESTjl1ZCvLKKPXH4T7MWiE32vK4Q67CoVfgxfo3OyIBiY7PWsOPf1hRysAfIjKMaEu3BUDjE7p6HFvTBwLCpapT32bX455MG68qXqkXgRglDFFhrej_WBNUyREXHPWjNqneCtKGjvRmyw3DL939c9KC677gCQhHFu9VNdWR3n8adbIRv_h6JHGeGE0h_MWG_OUZSvJrhlPFTpIWTyU1GQPLnRMZVMkAJvHwUrYLX2zeCrefJRGnJxXi9Ymm9SpQuE0910Lhe_z5ZGenrelwOVjlnL9SKgw.qnQGzZC2VD-Acyhlm5ssgw",
            "valle_lead_number": self.valle_lead_number
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

        response_json = json.loads(response.text)
        print(response_json)

        self.data = response_json["data"]
        
        # self.data_file = open(os.getcwd() + "/data/KA1000149.json", 'r')
        # self.data_json = json.load(self.data_file)
        
        # self.data = self.data_json["data"]
        

        self.property_value_assesment_map = self.data.get(
            'property_value_assessment').keys()
        self.property_value_assesment = [self.string_formatter(
            val) for val in self.property_value_assesment_map]

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
            "property_value_assessment" : {
                "land" : {"Rs "
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "basement_1" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "basement_2" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "ground_1" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "ground_2" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "ground_3" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "floor_1" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "floor_2" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "floor_3" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "floor_4" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "non-rcc_1" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "non-rcc_2" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "non-rcc_3" : {
                    "government_price" : "Rs ",
                    "consideration_price" : "Rs ",
                    "total_value_government_price" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "total_value_fair_market" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    }
                },
                "amenities" : {
                    "amenity_1" : {
                        "value" : "Rs "
                    },
                    "amenity_2" : {
                        "value" : "Rs "
                    },
                    "amenity_3" : {
                        "value" : "Rs "
                    },
                    "amenity_4" : {
                        "value" : "Rs "
                    },
                    "amenity_5" : {
                        "value" : "Rs "
                    },
                    "amenity_6" : {
                        "value" : "Rs "
                    }
                },
                "final_valuation" : {
                    "fair_market_value_on_date" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "fair_market_value_on_completion" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "distressed_sale_value" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                    "valuation_as_per_guideline" : {
                        "as_per_actual" : "Rs ",
                        "as_per_document_provided" : "Rs "
                    },
                }
            }
        }
        
        self.suffix_mapping = {
            "property_details" : {
                "location_detail" : {
                    "distance_from_city_center" : " KM"
                }
            },
            "technical_details" : {
                "plot_dimensons" : {
                    "north" : {
                        "as_per_actual" : " Ft.",
                        "as_per_document_provided" : " Ft.",
                        "as_per_approved_plan" : " Ft."
                    },
                    "south" : {
                        "as_per_actual" : " Ft.",
                        "as_per_document_provided" : " Ft.",
                        "as_per_approved_plan" : " Ft."
                    },
                    "east" : {
                        "as_per_actual" : " Ft.",
                        "as_per_document_provided" : " Ft.",
                        "as_per_approved_plan" : " Ft."
                    },
                    "west" : {
                        "as_per_actual" : " Ft.",
                        "as_per_document_provided" : " Ft.",
                        "as_per_approved_plan" : " Ft."
                    }
                },
                "land_area" : {
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    }
                },
                "bua_detail" : {
                    "basement_1" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "basement_2" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "ground_1" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "ground_2" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "ground_3" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "floor_1" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "floor_2" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "floor_3" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "floor_4" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "summation" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "non-rcc_1" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "non-rcc_2" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    },
                    "non-rcc_3" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                    }
                },
                "sbua_detail" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft.",
                        "as_per_approved_plan" : " Sq.Ft."
                },
                "additional_details" : {
                    "construction_progress" : "%",
                    "recommendation_for_fumding" : "%",
                    "age_of_property" : " Years",
                    "residual_age_of_property" : " Years",
                    "development_in_vicinity" : "%"
                }
            },            
            "property_value_assessment" : {
                "land" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "basement_1" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "basement_2" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "ground_1" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "ground_2" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "ground_3" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "floor_1" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "floor_2" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "floor_3" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "floor_4" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "non-rcc_1" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "non-rcc_2" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                },
                "non-rcc_3" : {
                    "government_price" : " /Sq.Ft.",
                    "consideration_price" : " /Sq.Ft.",
                    "area" : {
                        "as_per_actual" : " Sq.Ft.",
                        "as_per_document_provided" : " Sq.Ft."
                    }
                }
            }
        }

        for k, v in zip(self.property_value_assesment, self.property_value_assesment_map):
            self.data_json_map[k] = v

    def string_formatter(self, string, prefix="", suffix=""):

        if type(string) == type({}):
            string = string.values()
            string = ' '.join([str(s) for s in string])

        string = str(string)
        string = string.replace("_", " ")
        string = string.title()
        return prefix + string + suffix

    def value_formatter(self, string, prefix="", suffix=""):

        if type(string) == type({}):
            string = string.values()
            string = ' '.join([str(s) for s in string])

        string = str(string)
        string = string.replace("_", " ")
        string = string.title()
        
        if string: string = prefix + string + suffix

        v_styles = ParagraphStyle(name="Heading1", alignment=0,
                                  parent=styles['BodyText'], leading=15)
        t = Preformatted(string, v_styles, dedent=0, maxLineLength=45)
        return t

    def create_front_page(self):

        bordered_image = Image(bankImage, width=133, height=60)
        story = []

        story.append(bordered_image)
        story.append(Spacer(height=5, width=width))
        content_text = f"""<font size=22 color='white'>{self.organisation_name}</font>"""
        story.append(Paragraph(content_text, pStyles))
        story.append(Spacer(height=30, width=width))
        story.append(Image(report, width=420, height=98))
        story.append(Spacer(height=18, width=width))

        content_text = f"""<font size=32 style='800' color='white'>Valuation Report</font>"""
        story.append(Paragraph(content_text, pStyles))
        story.append(Spacer(height=290, width=width))
        # story.append(Spacer(height=350, width=width))
        story.append(PageBreak())

        return story

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
        content = self.create_index_page_content()

        story.append(Spacer(height=40, width=width))
        story.append(content)

        return story

    def create_section_heading(self, section="", j_section=""):

        # print("section",section)

        table_name_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=0,  # 0=left, 1=center, 2=right
            fontSize=12,
            # leading=18
        )

        switch = {
            "basic_valuation_detail" : basic_valuation_details,
            "property_details" : property_details,
            "building_detail" : building_details,
            "infrastructure_detail" :infrastructure_details,
            "technical_details": technical_details,
            "property_value_assessment": property_value_assesment,
            "valuer_remarks": valuer_remarks,
            "images": images,
            "valuer_detail" : valuer_details,
        }
        section_image = switch.get(j_section, basic_valuation_details)

        data = [
            [
                Image(section_image, width=20, height=20),
                Paragraph(f"{section}", table_name_styles),
                Image(table_title_sider, width=44.56, height=20)
            ]
        ]

        table_data = Table(data, colWidths=(40, 450, 80), rowHeights=(40))
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('BACKGROUND', (0, 0), (-1, -1), ACCENT_BG),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        return table_data

    def create_subsection_heading(self, subsection, j_subsection):

        table_name_styles = ParagraphStyle(
            'table_name_styles',
            parent=getSampleStyleSheet()['BodyText'],
            alignment=0,  # 0=left, 1=center, 2=right
            fontSize=12,
            # leading=18
        )
        
        sub_section_image = self.subsection_images.get(j_subsection, land_area)

        data = [
            [
                Image(sub_section_image, width=12, height=12),
                Paragraph(f"{subsection}", table_name_styles),
                Paragraph(f"", table_name_styles),
            ]
        ]

        table_data = Table(data, colWidths=(40, 450, 80), rowHeights=(40))
        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'CENTRE'),
            # ('BACKGROUND', (0, 0), (0, 0), ACCENT_BG),
            ('TEXTCOLOR', (0, 0), (1, -1), black)]))

        return table_data

    def create_subsection(self, data):

        table_data = Table(data, colWidths=(25, 260, 250))

        table_data.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
            ('TEXTCOLOR', (2, 0), (-1, -1), TEXT_HE),
        ]))

        return table_data

    def create_section(self, section=""):
        story = []
        j_section = self.data_json_map.get(section)
        # story.append(self.create_pdf_page_header())
        story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section, j_section))
        story.append(Spacer(width=width, height=15))

        sub_sections = self.subsections.get(section, "")
        for subsection in sub_sections:

            j_subsection = self.data_json_map.get(subsection)

            data_dict = {}

            if section in ("Basic Valuation Details", "Infrastructure Support", "Valuer Remarks", "Images"):
                data_dict = self.data.get(j_section, {})
            else:
                data_dict = self.data.get(j_section, {}).get(j_subsection, {})

            print(f"Data Dictionary {j_section} - {j_subsection} :: {data_dict}\n\n")
            
            prefix_data = self.prefix_mapping.get(j_section, {}).get(j_subsection, {})
            suffix_data = self.suffix_mapping.get(j_section, {}).get(j_subsection, {})
            
            print(prefix_data, suffix_data)

            data = []

            for key, value in data_dict.items():
                if type(value) == type({}):
                    data.append(["", self.string_formatter(key), ""])
                    for k, v in value.items():
                        prefix_x = prefix_data.get(key, {}).get(k, "")
                        suffix_x = suffix_data.get(key, {}).get(k, "")
                        data.append(["",self.string_formatter(k, "    - "),
                                    self.value_formatter(v, prefix_x, suffix_x)])
                else:
                    if key=="loan_application_number":
                        prefix = prefix_data.get(key, "")
                        suffix = suffix_data.get(key, "")
                        data.append(["", self.string_formatter(
                            key), value.upper()])
                    else:
                        prefix = prefix_data.get(key, "")
                        suffix = suffix_data.get(key, "")
                        data.append(["", self.string_formatter(
                            key), self.value_formatter(value, prefix, suffix)])

            if data:
                story.append(self.create_subsection_heading(subsection, j_subsection))
                story.append(self.create_subsection(data))
            story.append(Spacer(width=width, height=8))

        story.append(Spacer(width=width, height=15))
        # story.append(self.create_pdf_page_footer())

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
            
            if img_data["filename"].split(".")[-1] not in ("jpg", "png", "jpeg"): continue

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
        # story.append(self.create_pdf_page_footer())

        return story

    def destribute_images(self, images):

        data = []

        if len(images) % 2 == 0:
            for img in range(0, len(images), 2):
                data.append(["", Image(images[img], width=237.5, height=155), Image(
                    images[img+1], width=237.5, height=155)])
        else:
            for img in range(0, len(images)-1, 2):
                data.append(["", Image(images[img], width=237.5, height=155), Image(
                    images[img+1], width=237.5, height=155)])
            data.append(["", Image(images[-1], width=237.5, height=155), ""])

        return data

    def create_valuer_details_section(self, section):
        story = []
        # story.append(self.create_pdf_page_header())
        story.append(Spacer(width=width, height=8))
        story.append(self.create_section_heading(section))
        story.append(Spacer(width=width, height=15))
        
        valuer_detail = self.data.get("valuer_detail")
        
        data_d = [[ "", "Valuer Name", valuer_detail.get("first_name", "") + " " + valuer_detail.get("last_name","")]]
        
        table_data_d = Table(data_d, colWidths=(25, 260, 250))

        table_data_d.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # ('GRID', (0, 0), (-1, -1), 0.5, red),
            ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
            ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_HE),
        ]))
        
        story.append(Spacer(width=width, height=15))
        story.append(table_data_d)
        
        story.append(self.create_subsection_heading("Seal and Signature", ""))

        data = []
        all_images = []

        try:
            os.mkdir(f"assets/pdf_dynamic_images/{self.valle_lead_number}")
        except:
            print("Directory Already Exists")

        # valuer_detail = self.data.get("valuer_detail")
        
        # data_d = [[ "", "Valuer Name", valuer_detail.get("first_name", "") + " " + valuer_detail.get("last_name","")]]
        
        # table_data_d = Table(data_d, colWidths=(25, 260, 250))

        # table_data_d.setStyle(TableStyle([
        #     ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #     # ('GRID', (0, 0), (-1, -1), 0.5, red),
        #     ('TEXTCOLOR', (0, 0), (-2, -1), TEXT_ME),
        #     ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_HE),
        # ]))
        
        # story.append(Spacer(width=width, height=15))
        # story.append(table_data_d)
        
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
        # story.append(self.create_pdf_page_footer())

        return story

    def create_pdf_page(self, data=None):
        section_basic_valuation = self.create_section(
            "Basic Valuation Details")
        section_property_details = self.create_section("Property Details")
        section_building_details = self.create_section("Building Details")
        section_infrastructure_support = self.create_section(
            "Infrastructure Support")
        section_technical_details = self.create_section("Technical Details")
        section_property_value_assessement = self.create_section(
            "Property Value Assessment")
        section_valuer_remarks = self.create_section("Valuer Remarks")
        section_valuer_declaration = self.create_section("Valuer Declaration")
        section_valuer_details = self.create_valuer_details_section(
            "Valuer Details")
        images_data = self.data.get("images")
        if images_data:
            section_images = self.create_images_section("Images", images_data)

        story = []
        # story.append(Spacer(width=width, height=23))
        story.append(KeepTogether(section_basic_valuation))
        # story.append(PageBreak())
        story.append(KeepTogether(section_property_details))
        story.append(PageBreak())
        story.append(KeepTogether(section_building_details))
        story.append(PageBreak())
        story.append(KeepTogether(section_infrastructure_support))
        story.append(PageBreak())
        story.append(KeepTogether(section_technical_details))
        story.append(PageBreak())
        story.append(KeepTogether(section_property_value_assessement))
        story.append(PageBreak())
        story.append(KeepTogether(section_valuer_remarks))
        story.append(PageBreak())
        story.append(KeepTogether(section_valuer_declaration))
        story.append(PageBreak())
        story.append(KeepTogether(section_valuer_details))
        if images_data:
            story.append(PageBreak())
            story.append(KeepTogether(section_images))

        return story

    def draw_page_background(self, canvas, doc):
        height = doc.height
        width = doc.width
        canvas.linearGradient(x0=0, y0=height, x1=width /
                              0.5, y1=0, colors=[self.start_color, self.end_color])

    def generate_pdf(self, valle_lead_number, insititute_lead_number, organisation_name):

        self.valle_lead_number = valle_lead_number
        self.insititute_lead_number = insititute_lead_number
        self.organisation_name = organisation_name

        self.get_data(self.valle_lead_number)

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

        self.pdf_report = SimpleDocTemplate(
            self.buffer, pagesize=self.pagesize, topMargin=1*inch, bottomMargin=1*inch, title=f"Valluation Report{self.valle_lead_number}")

        self.frame_cover = Frame(
            self.pdf_report.leftMargin, self.pdf_report.bottomMargin,
            self.pdf_report.width, self.pdf_report.height,
            id='normal'
        )

        self.frame_index = Frame(
            self.pdf_report.leftMargin, self.pdf_report.bottomMargin,
            self.pdf_report.width, self.pdf_report.height,
            showBoundary=1,
            id='normal'
        )

        # Create a PageTemplate with the Frame
        self.page_template_cover = PageTemplate(
            id='cover_page', frames=[self.frame_cover])

        self.page_template = PageTemplate(id='index_page', frames=[
            self.frame_index])

        self.pdf_report.addPageTemplates(
            [self.page_template_cover, self.page_template])

        self.pdf_report.onFirstPage = lambda canvas, doc: self.draw_page_background(
            canvas, doc)

        self.pdf_queue = []

        # Cover page
        front_page = self.create_front_page()
        self.pdf_queue.extend(front_page)

        # Index page
        # index_page_content = self.create_index_page()
        # self.pdf_queue.append(toc)
        # self.pdf_queue.extend(index_page_content)

        # PDF Pages
        pdf_page = self.create_pdf_page()
        self.pdf_queue.extend(pdf_page)

        # Build the PDF document
        global VALLE_LEAD_NEMBER
        VALLE_LEAD_NEMBER = self.valle_lead_number
        
        self.pdf_report.build(
            self.pdf_queue,  canvasmaker=FooterCanvas)

        self.buffer.seek(0)

        # Create a response with the PDF content type
        self.pdf_response = make_response(self.buffer.read())
        self.pdf_response.headers['Content-Disposition'] = f'inline; filename={self.valle_lead_number}.pdf'
        self.pdf_response.headers['Content-Type'] = 'application/pdf'

        # Delete The Temporary Directory
        try:
            shutil.rmtree(
                f"assets/pdf_dynamic_images/{self.valle_lead_number}")
        except:
            print("Unable to Delete Temporary Directory")

        return self.pdf_response
    
    
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
# bankImage = "./assets/images/bank_image.jpeg"
# report = "./assets/images/report.png"
# valle_logo_white = "./assets/images/valle_logo_white.png"
# valle_logo_black = "./assets/images/valle_logo_black.jpeg"
# basic_valuation_details = "./assets/images/Basic Valuation Details.jpeg"
# property_details = "./assets/images/Property Details.jpg"
# building_details = "./assets/images/Building Details .jpeg"
# infrastructure_details = "./assets/images/Infrastructure Details.jpeg"
# technical_details = "./assets/images/Technical Details.jpeg"
# property_value_assesment = "./assets/images/Property Value Assesment.jpeg"
# valuer_remarks = "./assets/images/Valuer Remarks.png"
# valuer_details = "./assets/images/Valuer Details.png"
# images = "./assets/images/Images Icon.jpeg"
# shield = "./assets/images/shield.jpeg"
# table_title_sider = "./assets/images/table_title_sider.jpeg"
# property_image = "./assets/images/property_image.jpeg"
# mobile_image = "./assets/images/Mobile.jpg"
# email_image = "./assets/images/Email.jpg"
# amenities = "./assets/images/Amenitites.jpeg"
# additional_details = "./assets/images/additional_details.jpeg"
# basic_details = "./assets/images/basic_details.jpeg"
# bua_details = "./assets/images/BUA Details.jpeg"
# construction_details = "./assets/images/Construction Details.jpeg"
# final_valuation = "./assets/images/Final Valuation.jpeg"
# ground_floor = "./assets/images/ground_floor.jpeg"
# infrastructure_support = "./assets/images/Infrastructure Support.jpg"
# land_area = "./assets/images/Land area.jpg"
# loaction_details = "./assets/images/Loaction Details.jpeg"
# plan_details = "./assets/images/Plan Details.jpeg"
# plot_details = "./assets/images/Plot Details.jpeg"
# remarks = "./assets/images/Remarks.jpeg"
# sbua_details = "./assets/images/SBUA Details.png"
# schedule_details = "./assets/images/Schedule Details.jpeg"
# seal_signature_details = "./assets/images/seal_&_signature.jpeg"

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
        self.valle_lead_number = VALLE_LEAD_NEMBER
        
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
