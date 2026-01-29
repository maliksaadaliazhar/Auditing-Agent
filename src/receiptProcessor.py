import os
import json
import pymupdf
from pathlib import Path
from dotenv import load_dotenv
from src.receipt import Receipt, LineItem

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

# this method will handle the overall processing of the receipt and will return the receipt object
def process_receipt(self, image_path: str) -> Receipt:
        
        # Step A: Parse (Image -> Markdown)
        markdown = parse_image(image_path)
        
        # Step B: Extract (Markdown -> JSON)
        raw_json = extract_data(markdown)
        
        # Step C: Map (JSON -> Receipt Object)
        receipt = map_to_object(raw_json)
        
        return receipt

def parse_image(self, image_path: str) -> str:

    with open(image_path, "rb") as f:
        image_bytes = f.read()
        
    parse_result = self.client.parse(image_bytes)
    return parse_result[0].markdown

def extract_data(self, markdown_text: str) -> dict:
    
    receipt_schema = {
        "type": "object",
        "properties": {
            "merchant_name": {"type": "string"},
            "date": {"type": "string", "description": "YYYY-MM-DD format"},
            "total_amount": {"type": "number"},
            "currency": {"type": "string"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number"},
                        "category": {"type": "string"}
                    },
                    "required": ["description", "amount"]
                }
            }
        },
        "required": ["merchant_name", "total_amount", "date"]
    }

    extraction_result = self.client.extract(
        markdown=markdown_text,
        schema=json.dumps(receipt_schema)
    )
    return extraction_result.extraction

def map_to_object(self, data: dict) -> Receipt:
    
    receipt = Receipt(
        merchant_name=data.get("merchant_name", "Unknown"),
        date=data.get("date"),
        total_amount=float(data.get("total_amount", 0.0)),
        currency=data.get("currency", "USD"),
        items=[]
    )

    if "items" in data:
        for item in data["items"]:
            new_item = LineItem(
                description=item.get("description", "Unknown"),
                amount=float(item.get("amount", 0.0)),
                category=item.get("category", "Unknown")
            )
            receipt.items.append(new_item)
    
    return receipt

# this will contain these two methods 
# - parse_document --- that will call parse api of ade
# - extract_document --- that will call extract api of ade
# - a schema will be defined
# - other functionalities will be considered later