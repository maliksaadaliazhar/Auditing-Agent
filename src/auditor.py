import datetime
from google import genai
from google.genai import types
from pydantic import BaseModel


class AuditResult(BaseModel):
    is_compiant : bool
    violation_reason : str


class Auditor:
    def __init__(self):
        self.client = genai.Client()

    def audit_receipt(self, receipt):
        self.check_weekend(receipt)
        self.check_alcohol(receipt)

    def check_weekend(self, receipt):
        # it date is empty, it will be flagged…
        if not receipt.datetime_object:
            receipt.flagged = True
            receipt.flag_reason.append("Date unreadable or not mentioned")

        elif (receipt.datetime_object.weekday() >= 5):
            receipt.flagged = True
            receipt.flag_reason.append("Weekend Policy Violation")
        

    def check_alcohol(self, receipt):
        items_list = "\n".join([item.description for item in receipt.items])
        prompt = f"List of items in receipt :\n{items_list}"
        
        response = self.client.models.generate_content(
            model="gemini-3-flash-preview", 
            config=types.GenerateContentConfig(
                system_instruction="You are a strict corporate auditor. Your role is to identify" \
                "if a receipt contains a tobacco or alcohol or any other drug product",
                response_mime_type="application/json",
                response_schema=AuditResult),
            contents=prompt
        )

        if not response['is_compiant']:
            receipt.flagged = True
            receipt.flag_reason.append(response['violation_reason'])

# it will have a class auditor which will take the receipt object as input and manipulate it
# it will be main brain of the logic that handles logic and all that stuff…