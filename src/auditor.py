import datetime

class Auditor:
    def __init__(self):
        self.alcohol_keywords = ['wine', 'beer', 'alcohol', 'vodka', 'merlot']

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
        items = receipt.items
        for lineitem in items:
            for word in self.alcohol_keywords:
                if (word in lineitem.description.lower()):
                    receipt.flagged = True
                    receipt.flag_reason.append("Alcohol Violation")
                    return

# it will have a class auditor which will take the receipt object as input and manipulate it
# it will be main brain of the logic that handles logic and all that stuff…