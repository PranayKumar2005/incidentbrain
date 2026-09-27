import os

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight


load_dotenv()


class IncidentAgent:

    def __init__(self):
        # Groq
        self.groq = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        # Hindsight
        self.memory = Hindsight(
            base_url=os.getenv("HINDSIGHT_BASE_URL"),
            api_key=os.getenv("HINDSIGHT_API_KEY")
        )

        self.bank_id = os.getenv("HINDSIGHT_BANK_ID")

    def investigate(self, incident: str):

        # 1. Search Hindsight for previous incidents
        memory_result = self.memory.recall(
            bank_id=self.bank_id,
            query=incident
        )

        # 2. Convert memories into text
        memories = []

        for result in memory_result.results:
            memories.append(result.text)

        memory_context = "\n\n".join(memories)

        # 3. Ask Groq to analyze the incident
        prompt = f"""
You are IncidentBrain, an SRE incident response assistant.

Analyze the current production incident using the previous
incident memories provided below.

CURRENT INCIDENT:
{incident}

PREVIOUS INCIDENT MEMORIES:
{memory_context}

IMPORTANT RULES:

- Treat previous incidents as evidence, not absolute truth.

- Use only information explicitly present in the CURRENT INCIDENT
  or the retrieved Hindsight memories.

- Do not invent configuration values, metrics, causes, outcomes,
  thresholds, percentages, limits, dates, or capacity numbers.

- NEVER introduce a numeric value unless that exact numeric value
  appears in the CURRENT INCIDENT or PREVIOUS INCIDENT MEMORIES.

- This includes percentages, thresholds, pool sizes, limits,
  counts, durations, rates, and capacity values.

- A historical numeric value may be mentioned only as a historical
  fact from the retrieved memories.

- NEVER assume that a historical value is the current configuration.

- NEVER describe a historical value as the "current", "existing",
  "present", or "configured" value unless the CURRENT INCIDENT
  explicitly provides that value.

- Do not infer historical thresholds, baselines, limits, usage
  levels, capacity, or alert thresholds that are not explicitly
  stated in the memories.

- Do not calculate, estimate, extrapolate, or derive new numeric
  values from existing values.

- Do not convert a historical value into a recommendation unless
  the historical evidence explicitly supports that action for the
  current incident.

- Clearly distinguish historical facts from current observations
  and recommendations.

- If a required value is unknown, write "value not provided".

- If the current configuration is unknown, explicitly instruct
  the engineer to verify it before making a configuration change.

- Never claim that a remediation is guaranteed to work.

- Do not recommend a new numeric configuration value.

- When referring to a previous incident, state only facts that
  are explicitly present in the retrieved memories.

- Do not introduce hypothetical values such as "80%", "350",
  "400 connections", or similar values unless they are explicitly
  present in the evidence.

- Recommendations should focus on verification, investigation,
  and previously documented actions.

- If the available evidence is insufficient, say:
  "Additional investigation is required."

Provide:

1. Likely root cause
2. Evidence from previous incidents
3. Recommended remediation
4. Why this remediation is relevant
5. Risks or uncertainty
"""

        response = self.groq.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an experienced SRE incident response "
                        "assistant. Be strictly evidence-driven. "
                        "Use only facts present in the current incident "
                        "or retrieved Hindsight memories. "
                        "Never invent technical details, numeric values, "
                        "thresholds, metrics, configuration, or outcomes. "
                        "Never assume that historical values are current "
                        "values."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        recommendation = response.choices[0].message.content

        return {
            "incident": incident,
            "memories_found": memories,
            "recommendation": recommendation
        }

    def resolve_incident(
        self,
        incident: str,
        action_taken: str,
        outcome: str
    ):
        """
        Store a structured incident experience in Hindsight
        so IncidentBrain can learn from this experience.
        """

        experience = f"""
HISTORICAL SRE INCIDENT EXPERIENCE

Incident:
{incident.strip()}

Action that was taken:
{action_taken.strip()}

Observed outcome:
{outcome.strip()}

Historical lesson:
This incident and its resolution should be treated as
evidence when investigating future incidents with similar
symptoms.

Important:
Only use the facts explicitly stated above.
Do not infer or invent additional configuration values,
metrics, causes, or outcomes.
"""

        result = self.memory.retain(
            bank_id=self.bank_id,
            content=experience
        )

        return result

    def close(self):
        self.memory.close()