import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")


query = """
The Payment API is returning HTTP 503 errors.
Redis connections are very high and the connection pool
appears to be exhausted.

What similar incidents have we experienced before?
What was the root cause and what solution worked?
"""


result = client.recall(
    bank_id=bank_id,
    query=query
)

print("Recall completed!")
print(result)