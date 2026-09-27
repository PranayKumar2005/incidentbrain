from hindsight_client import Hindsight
from dotenv import load_dotenv
import os


load_dotenv()


def main():
    client = Hindsight(
        base_url=os.getenv("HINDSIGHT_BASE_URL"),
        api_key=os.getenv("HINDSIGHT_API_KEY")
    )

    bank_id = os.getenv("HINDSIGHT_BANK_ID")

    incident = """
    The Search API returned HTTP 500 errors.

    Root cause:
    The PostgreSQL connection pool was exhausted.

    Action taken:
    The connection pool size was increased from 50 to 150.

    Outcome:
    The error rate returned to normal and the incident was resolved.
    """

    print("Storing incident...")

    store_result = client.retain(
        bank_id=bank_id,
        content=incident
    )

    print(store_result)

    print("\nSearching memory...")

    query = """
    The Search API is returning HTTP 500 errors.
    The PostgreSQL connection pool is exhausted.

    Have we experienced a similar incident before?
    What solution worked?
    """

    recall_result = client.recall(
        bank_id=bank_id,
        query=query
    )

    print(recall_result)

    # Close the Hindsight client properly
    client.close()

    print("\nHindsight client closed.")


if __name__ == "__main__":
    main()