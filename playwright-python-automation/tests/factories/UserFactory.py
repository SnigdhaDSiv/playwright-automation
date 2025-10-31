
import random
from faker import Faker

fake = Faker()

class UserFactory:
    """Factory for creating user test data."""

    @staticmethod
    def create_user(active=True, custom_data=None):
        """Returns a fake user dict."""
        accounttype = random.choice(["premium", "basic"])
        user = {
      
            "name": fake.name(),
            "email": fake.email(),
            "accountType": accounttype, 
        }
        if custom_data:
            user.update(custom_data)

        return user
