import uuid
import random
from datetime import datetime

class TransactionFactory:
    """Factory for creating transaction test data."""

    @staticmethod
    def create_transaction(user_id, recipient_id=None, amount=None):
        if not recipient_id:
            recipient_id = str(uuid.uuid4())

        if not amount:
            amount = round(random.uniform(10, 1000), 2)

        transaction = {
            "user_id": user_id,
            "recipient_id": recipient_id,
            "amount": amount,
            "type": "transfer",
            "timestamp": datetime.now().isoformat()
        }
        return transaction

