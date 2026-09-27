from agent.incident_agent import IncidentAgent


agent = IncidentAgent()


incident = """
The Payment API is returning HTTP 503 errors.

Monitoring shows that the number of Redis connections
has increased significantly and is close to the configured
connection limit.
"""


print("Investigating incident...\n")

result = agent.investigate(incident)


print("========== PREVIOUS MEMORIES ==========")

for memory in result["memories_found"]:
    print("\n- " + memory)


print("\n========== INCIDENTBRAIN RECOMMENDATION ==========")

print(result["recommendation"])


agent.close()