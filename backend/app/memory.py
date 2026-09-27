import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()


class IncidentMemory:

    def __init__(self):
        self.client = Hindsight(
            base_url=os.getenv("HINDSIGHT_BASE_URL"),
            api_key=os.getenv("HINDSIGHT_API_KEY")
        )

        self.bank_id = os.getenv("HINDSIGHT_BANK_ID")

    def remember_incident(self, incident: str):
        return self.client.retain(
            bank_id=self.bank_id,
            content=incident
        )

    def find_similar_incidents(self, query: str):
        return self.client.recall(
            bank_id=self.bank_id,
            query=query
        )