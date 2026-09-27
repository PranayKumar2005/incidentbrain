from agent.incident_agent import IncidentAgent


agent = IncidentAgent()

new_incident = """
The Payment API is again returning HTTP 503 errors.

Monitoring shows that Redis connections are approaching
the configured connection limit again.
This appears similar to a previous Payment API incident.
"""

print("Investigating new incident...\n")

result = agent.investigate(new_incident)

print("========== RECALLED MEMORIES ==========")

for memory in result["memories_found"]:
    print("\n- " + memory)

print("\n========== INCIDENTBRAIN RECOMMENDATION ==========")
print(result["recommendation"])

agent.close()

print("\nHindsight client closed.")