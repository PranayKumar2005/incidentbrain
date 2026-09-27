from agent.incident_agent import IncidentAgent


agent = IncidentAgent()

incident = """
The Payment API is returning HTTP 503 errors.

Monitoring shows that the number of Redis connections
has increased significantly and is close to the configured
connection limit.
"""

action_taken = """
The engineering team increased the Redis connection pool
size from 100 to 250.
"""

outcome = """
The HTTP 503 error rate returned to normal and the
Payment API incident was resolved.
"""

print("Storing incident resolution in Hindsight...\n")

result = agent.resolve_incident(
    incident=incident,
    action_taken=action_taken,
    outcome=outcome
)

print("========== HINDSIGHT STORE RESULT ==========")
print(result)

agent.close()

print("\nHindsight client closed.")