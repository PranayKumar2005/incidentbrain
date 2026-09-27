\# 🧠 IncidentBrain



\### AI-Powered SRE Incident Response Agent with Hindsight Memory



IncidentBrain is an AI-powered Site Reliability Engineering (SRE) incident response agent that learns from previous production incidents.



Instead of treating every incident as a completely new problem, IncidentBrain uses \*\*Hindsight memory\*\* to recall previous incident experiences, including symptoms, actions taken, and observed outcomes.



When a similar incident happens again, the agent retrieves that historical knowledge and uses it as evidence while generating a new investigation and remediation recommendation.



\---



\## 🚨 Problem



Production incidents often repeat.



An engineering team may have already solved a similar incident in the past, but that knowledge can be difficult to retrieve quickly during a new outage.



Traditional incident-response workflows often depend on:



\- Human memory

\- Searching old incident tickets

\- Reading previous postmortems

\- Tribal knowledge

\- Manually comparing similar incidents



This can slow down incident investigation and remediation.



IncidentBrain addresses this problem by giving an AI SRE agent a persistent memory of previous incident experiences.



\---



\## 💡 Solution



IncidentBrain creates a continuous incident-learning loop:



```text

Incident

&#x20;  ↓

Recall previous experience

&#x20;  ↓

AI investigation

&#x20;  ↓

Recommended remediation

&#x20;  ↓

Engineer resolves incident

&#x20;  ↓

Store outcome in Hindsight

&#x20;  ↓

Future incidents benefit from the experience



The key idea is that the agent does not simply generate an answer.



It learns from operational experience and uses that experience during future investigations.



🧠 How Hindsight Memory Works



Hindsight is the core learning component of IncidentBrain.



When an incident is resolved, IncidentBrain stores an experience containing:



Incident symptoms

Action taken

Observed outcome

Historical lesson



For example:



Incident:

Payment API returned HTTP 503 errors.



Action:

Redis connection pool was increased from 100 to 250.



Outcome:

HTTP 503 error rate returned to normal.



Later, when a similar Payment API incident occurs, IncidentBrain searches Hindsight for relevant previous experiences.



The retrieved memory is then provided to the LLM as historical evidence.



This creates the learning loop:



Past incident

&#x20;    ↓

Hindsight retains experience

&#x20;    ↓

Similar incident occurs

&#x20;    ↓

Hindsight recalls experience

&#x20;    ↓

LLM uses historical evidence

&#x20;    ↓

Engineer resolves incident

&#x20;    ↓

New outcome is retained

🔄 Example: IncidentBrain Learning

Incident 1



The Payment API starts returning HTTP 503 errors.



Monitoring shows that Redis connections are approaching the configured connection limit.



IncidentBrain investigates the incident.



The engineering team resolves it by increasing the Redis connection pool size.



The observed outcome is stored in Hindsight.



Incident 2



Later, the Payment API again starts returning HTTP 503 errors.



Redis connections are again approaching the configured connection limit.



IncidentBrain searches its memory.



Hindsight retrieves the previous Payment API experience.



The agent can now use that previous resolution as historical evidence while investigating the new incident.



This demonstrates that the second investigation benefits from the first incident.



🏗️ System Architecture

&#x20;                   ┌──────────────────────┐

&#x20;                   │    React Frontend    │

&#x20;                   │   Incident Dashboard │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   FastAPI Backend     │

&#x20;                   │ Investigation /       │

&#x20;                   │ Resolution APIs      │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   IncidentBrain      │

&#x20;                   │       Agent          │

&#x20;                   └───────┬───────┬──────┘

&#x20;                           │       │

&#x20;              ┌────────────┘       └─────────────┐

&#x20;              ▼                                  ▼

&#x20;     ┌──────────────────┐              ┌──────────────────┐

&#x20;     │    Hindsight     │              │   Groq + LLM     │

&#x20;     │      Memory      │              │    Reasoning     │

&#x20;     └──────────────────┘              └──────────────────┘

Components

React Frontend



Provides the SRE incident dashboard.



It allows engineers to:



Submit incidents

View investigation results

View recalled Hindsight memories

Review AI recommendations

Record actions taken

Record incident outcomes

FastAPI Backend



Provides the backend API for the application.



Main endpoints:



GET  /

GET  /health

POST /investigate

POST /resolve

IncidentBrain Agent



The agent coordinates:



Incident investigation

Hindsight memory retrieval

LLM reasoning

Incident resolution storage

Hindsight



Provides persistent incident memory.



It stores previous incident experiences and retrieves relevant knowledge for future incidents.



Groq + LLM



The LLM analyzes the current incident together with the historical evidence retrieved from Hindsight.



🛠️ Tech Stack

Technology	Purpose

React	Frontend dashboard

Vite	Frontend development/build tooling

FastAPI	Backend API

Python	Backend and agent implementation

Hindsight	Persistent agent memory

Groq	LLM inference

OpenAI GPT-OSS 120B	Reasoning model

Uvicorn	FastAPI server

📁 Project Structure

incidentbrain/

│

├── README.md

│

└── backend/

&#x20;   │

&#x20;   ├── app/

&#x20;   │   │

&#x20;   │   ├── \_\_init\_\_.py

&#x20;   │   ├── main.py

&#x20;   │   │

&#x20;   │   ├── agent/

&#x20;   │   │   ├── \_\_init\_\_.py

&#x20;   │   │   └── incident\_agent.py

&#x20;   │   │

&#x20;   │   ├── test\_hindsight.py

&#x20;   │   ├── memory\_test.py

&#x20;   │   ├── recall\_test.py

&#x20;   │   ├── groq\_test.py

&#x20;   │   ├── agent\_test.py

&#x20;   │   ├── resolve\_test.py

&#x20;   │   └── learning\_test.py

&#x20;   │

&#x20;   ├── frontend/

&#x20;   │   ├── src/

&#x20;   │   │   ├── App.jsx

&#x20;   │   │   ├── App.css

&#x20;   │   │   └── ...

&#x20;   │   │

&#x20;   │   ├── package.json

&#x20;   │   └── ...

&#x20;   │

&#x20;   ├── requirements.txt

&#x20;   ├── .env

&#x20;   └── .gitignore

⚙️ Environment Variables



Create a .env file inside the backend directory:



HINDSIGHT\_API\_KEY=your\_hindsight\_api\_key

HINDSIGHT\_BASE\_URL=https://api.hindsight.vectorize.io

HINDSIGHT\_BANK\_ID=incidentbrain

GROQ\_API\_KEY=your\_groq\_api\_key



Never commit .env or API keys to GitHub.



The project .gitignore includes:



venv/

.env

\_\_pycache\_\_/

\*.pyc

🚀 Running the Project

1\. Clone the repository

git clone <your-repository-url>

cd incidentbrain

2\. Create and activate the Python environment



From the backend directory:



Windows PowerShell

cd backend

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

3\. Install Python dependencies

pip install -r requirements.txt

4\. Start the FastAPI backend



From:



incidentbrain/backend



run:



uvicorn app.main:app --reload



The backend will run at:



http://127.0.0.1:8000

5\. Start the React frontend



Open another terminal:



cd incidentbrain\\backend\\app\\frontend

npm install

npm run dev



The Vite development server will display the local frontend URL.



🧪 Demo Workflow

Step 1 — Submit the first incident



Example:



The Payment API is returning HTTP 503 errors.



Monitoring shows that Redis connections have increased significantly

and are close to the configured connection limit.



Click:



Investigate

Step 2 — Resolve the incident



Enter the action taken:



The engineering team increased the Redis connection pool size from 100 to 250.



Enter the outcome:



The HTTP 503 error rate returned to normal and the Payment API incident was resolved.



Click:



Resolve \& Learn



IncidentBrain stores the experience in Hindsight.



Step 3 — Trigger a similar incident



Submit:



The Payment API is again returning HTTP 503 errors.



Monitoring shows that Redis connections are approaching

the configured connection limit again.



Click:



Investigate

Step 4 — Observe the memory



IncidentBrain retrieves the previous incident experience.



The dashboard displays:



🧠 Previous incident knowledge retrieved



The AI recommendation then uses the historical incident as evidence.



This demonstrates the central learning behavior of IncidentBrain.



🎯 Key Features

🧠 Persistent Incident Memory



Stores previous incident experiences using Hindsight.



🔍 Historical Recall



Retrieves relevant incidents when a similar production problem occurs.



🤖 Evidence-Based AI Investigation



Combines the current incident with retrieved historical evidence.



🔧 Resolution Tracking



Captures the action taken by the engineer and the observed outcome.



🔄 Continuous Learning Loop



Every resolved incident can become useful knowledge for future incidents.



⚠️ Uncertainty Awareness



The agent distinguishes historical evidence from current observations and can request additional investigation when information is missing.



🔐 Safety and Evidence Handling



IncidentBrain is designed to treat previous incidents as evidence rather than absolute truth.



The agent is instructed to:



Distinguish historical facts from current observations.

Avoid inventing technical details.

Avoid inventing configuration values or metrics.

Verify current configuration before making changes.

State when information is unknown.

Consider risks associated with remediation.

Request additional investigation when evidence is insufficient.



This helps prevent blindly applying an old incident resolution to a new production environment.



📊 Why Memory Matters



A conventional LLM can analyze the current incident.



IncidentBrain adds another capability:



Current Incident

&#x20;      +

Past Operational Experience

&#x20;      ↓

Context-Aware Investigation



The important difference is that the agent can carry operational knowledge from previous incidents into future interactions.



As more incidents are resolved, the memory store can contain more operational experience that can be recalled when relevant.



🔮 Future Improvements



Potential future improvements include:



Integration with real monitoring systems

Integration with incident management platforms

Kubernetes investigation workflows

Log and trace analysis

Automatic incident timeline generation

Incident similarity scoring

Richer post-incident summaries

Automated verification of remediation outcomes

Team-specific operational knowledge

Production deployment

📌 Current Scope



IncidentBrain currently focuses on a single workflow:



Learning from previous production incidents to assist investigation of similar future incidents.



The project uses realistic/synthetic incident scenarios to demonstrate the memory and learning workflow.



👨‍💻 Project



IncidentBrain — SRE Incident Response Agent



Built to demonstrate how persistent agent memory can transform previous operational experiences into reusable incident-response knowledge.





\### Important



Do \*\*not\*\* put your actual API keys anywhere in the README.



At the bottom of the README, we intentionally leave:



```text

<your-repository-url>

