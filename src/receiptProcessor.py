import os
import json
import pymupdf
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# =====================================
# Importing Landing ai specific api's
# =====================================
from landingai_ade import LandingAIADE
from landingai_ade.types import ParseResponse, ExtractResponse


# Importing helper functions
from helper import print_document, draw_bounding_boxes, draw_bounding_boxes_2
from helper import create_cropped_chunk_images


# Load envrironment variables from dotenv
_ = load_dotenv(override=True)


# Initialize the client
client = LandingAIADE()

# this will contain these two methods 
# - parse_document --- that will call parse api of ade
# - extract_document --- that will call extract api of ade
# - a schema will be defined
# - other functionalities will be considered later