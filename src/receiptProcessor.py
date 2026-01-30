# import os
# import json
# from pathlib import Path
# from dotenv import load_dotenv
# from src.receipt import Receipt, LineItem

# # =====================================
# # Importing Landing ai specific api's
# # =====================================
# from landingai_ade import LandingAIADE
# from landingai_ade.types import ParseResponse, ExtractResponse


# # Importing helper functions
# # from helper import print_document, draw_bounding_boxes, draw_bounding_boxes_2
# # from helper import create_cropped_chunk_images


# # Load envrironment variables from dotenv
# load_dotenv()


# # Initialize the client
# client = LandingAIADE()

# receipt_schema = {
#         "type": "object",
#         "properties": {
#             "merchant_name": {"type": "string"},
#             "date": {"type": "string", "description": "YYYY-MM-DD format"},
#             "time": {"type": "string", "description": "HH:MM"},
#             "total_amount": {"type": "number"},
#             "currency": {"type": "string"},
#             "items": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "description": {"type": "string", "description": "name of individual item on line"},
#                         "amount": {"type": "number", "description": "The cost of an individual item"},
#                         "category": {"type": "string", "description": "food, alcohol, travel, other"}
#                     },
#                     "required": ["description", "amount"]
#                 }
#             }
#         },
#         "required": ["merchant_name", "total_amount", "date"]
#     }

# # this method will handle the overall processing of the receipt and will return the receipt object
# def process_receipt(image_path: str) -> Receipt:

#     document = Path(image_path)
#     parse_result : ParseResponse = client.parse(
#          document=document,
#          split="page",
#          model="dpt-2-latest"
#     )

#     extraction_result : ExtractResponse = client.extract(
#         markdown=parse_result.markdown,
#         schema=json.dumps(receipt_schema)
#     )
#     raw_json = extraction_result.extraction
#     metadata = extraction_result.extraction_metadata

#     chunk_map = create_chunk_map(parse_result)
#     receipt = map_to_object(raw_json, metadata, chunk_map)

    
#     return receipt

# def create_chunk_map(parse_result: ParseResponse):
#     chunk_map = {}
#     for chunk in parse_result.chunks:
#         if chunk.grounding.box:
#             box = chunk.grounding.box
#             chunk_map[chunk.id] = [box.left, box.top, box.right, box.bottom]

#     return chunk_map 

# def map_to_object(data: dict, metadata: dict, chunk_map: dict) -> Receipt:
    
#     receipt = Receipt(
#         merchant_name=data.get("merchant_name", "Unknown"),
#         date=data.get("date"),
#         time=data.get("time"),
#         total_amount=float(data.get("total_amount", 0.0)),
#         currency=data.get("currency", "USD"),
#         items=[]
#     )

#     if "items" in data and "items" in metadata:
#         for i, item in enumerate(data["items"]):
#             new_item = LineItem(
#                 description=item.get("description", "Unknown"),
#                 amount=float(item.get("amount", 0.0)),
#                 category=item.get("category", "Unknown")
#             )

#             try:
#                 item_meta = metadata["items"][i]
#                 if "description" in item_meta and item_meta["description"]["references"]:
#                     ref_id = item_meta["description"]["references"][0]

#                     if ref_id in chunk_map:
#                         new_item.bbox = chunk_map[ref_id]
#             except(KeyError, IndexError):
#                 pass

#             receipt.items.append(new_item)
    
#     return receipt
import json
from pathlib import Path
from dotenv import load_dotenv
from src.receipt import Receipt, LineItem

# =====================================
# Importing Landing ai specific api's
# =====================================
from landingai_ade import LandingAIADE
from landingai_ade.types import ParseResponse, ExtractResponse

load_dotenv()

# Schema definition (Keep your existing one)
receipt_schema = {
    "type": "object",
    "properties": {
        "merchant_name": {"type": "string"},
        "date": {"type": "string"},
        "time": {"type": "string"},
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

def process_receipt(image_path: str) -> Receipt:
    client = LandingAIADE()
    document = Path(image_path)
    
    # 1. Parse (Get the Map of all text)
    parse_result_list = client.parse(
         document=document,
         split="page",
         model="dpt-2-latest"
    )
    first_page = parse_result_list

    # 2. Extract (Get the Clean Data)
    extraction_result = client.extract(
        markdown=first_page.markdown,
        schema=json.dumps(receipt_schema)
    )
    raw_json = extraction_result.extraction
    
    # 3. Map Data to Object using TEXT MATCHING (The Fix)
    # We pass the 'first_page' which contains all the raw chunks
    receipt = map_to_object(raw_json, first_page)
    
    return receipt

def map_to_object(data: dict, page_result) -> Receipt:
    
    receipt = Receipt(
        merchant_name=data.get("merchant_name", "Unknown"),
        date=data.get("date"),
        time=data.get("time"),
        total_amount=float(data.get("total_amount", 0.0)),
        currency=data.get("currency", "USD"),
        items=[]
    )

    if "items" in data:
        for item_data in data["items"]:
            new_item = LineItem(
                description=item_data.get("description", "Unknown"),
                amount=float(item_data.get("amount", 0.0)),
                category=item_data.get("category", "Unknown")
            )

            # === THE NEW LOGIC: FIND THE TEXT ===
            # We loop through every raw text chunk on the page
            found_match = False
            for chunk in page_result.chunks:
                # We need chunks that contain text
                # (Some chunks are logos or tables, we skip those)
                if hasattr(chunk, "text") and chunk.text:
                    chunk_text = chunk.text.lower().strip()
                    item_desc = new_item.description.lower().strip()
                    
                    # LOGIC: If the Chunk Text is inside the Item Description (or vice versa)
                    # Example: Chunk="Marlboro" is inside Item="Marlboro Gold"
                    if chunk_text in item_desc and len(chunk_text) > 3:
                        
                        # Grab the box from grounding
                        grounding = getattr(chunk, 'grounding', None)
                        if grounding and grounding.box:
                            box = grounding.box
                            new_item.bbox = [box.left, box.top, box.right, box.bottom]
                            found_match = True
                            break # We found it, stop searching
            
            receipt.items.append(new_item)
    
    return receipt
