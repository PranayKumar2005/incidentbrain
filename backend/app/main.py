from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent.incident_agent import IncidentAgent


app = FastAPI(
    title="IncidentBrain",
    description="AI-powered SRE Incident Response Agent",
    version="0.1.0"
)


# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentRequest(BaseModel):
    incident: str


class ResolveRequest(BaseModel):
    incident: str
    action_taken: str
    outcome: str


@app.get("/")
def root():
    return {
        "project": "IncidentBrain",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/investigate")
def investigate(request: IncidentRequest):

    agent = IncidentAgent()

    try:
        result = agent.investigate(request.incident)

        return result

    finally:
        agent.close()


@app.post("/resolve")
def resolve(request: ResolveRequest):

    agent = IncidentAgent()

    try:
        result = agent.resolve_incident(
            incident=request.incident,
            action_taken=request.action_taken,
            outcome=request.outcome
        )

        return {
            "status": "success",
            "message": "Incident resolution stored in Hindsight.",
            "result": str(result)
        }

    finally:
        agent.close()