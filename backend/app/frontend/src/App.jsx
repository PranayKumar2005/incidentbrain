import { useState } from "react";
import "./App.css";

function App() {
  const [incident, setIncident] = useState("");
  const [result, setResult] = useState(null);

  const [actionTaken, setActionTaken] = useState("");
  const [outcome, setOutcome] = useState("");

  const [loading, setLoading] = useState(false);
  const [resolving, setResolving] = useState(false);
  const [learned, setLearned] = useState(false);

  const investigate = async () => {
    if (!incident.trim()) return;

    setLoading(true);
    setResult(null);
    setLearned(false);

    try {
      const response = await fetch("http://127.0.0.1:8000/investigate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          incident: incident,
        }),
      });

      if (!response.ok) {
        throw new Error("Investigation request failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        error: "Could not connect to IncidentBrain backend.",
      });
    } finally {
      setLoading(false);
    }
  };

  const resolveIncident = async () => {
    if (!actionTaken.trim() || !outcome.trim()) return;

    setResolving(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/resolve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          incident: incident,
          action_taken: actionTaken,
          outcome: outcome,
        }),
      });

      if (!response.ok) {
        throw new Error("Resolution request failed");
      }

      await response.json();

      setLearned(true);
    } catch (error) {
      alert("Could not store the incident resolution.");
    } finally {
      setResolving(false);
    }
  };

  return (
    <div className="app">

      {/* Header */}
      <header>
        <h1>🧠 IncidentBrain</h1>
        <p>AI-powered SRE Incident Response Agent</p>
      </header>

      <main>

        {/* How IncidentBrain Learns */}
        <section className="card learning-flow">
          <h2>How IncidentBrain Learns</h2>

          <p className="flow-description">
            IncidentBrain uses Hindsight memory to turn past incident
            resolutions into reusable operational knowledge.
          </p>

          <div className="flow">

            <div className="flow-step">
              <div className="flow-icon">🚨</div>
              <h3>Incident</h3>
              <p>Production issue occurs</p>
            </div>

            <div className="flow-arrow">→</div>

            <div className="flow-step">
              <div className="flow-icon">🧠</div>
              <h3>Recall</h3>
              <p>Hindsight retrieves relevant experience</p>
            </div>

            <div className="flow-arrow">→</div>

            <div className="flow-step">
              <div className="flow-icon">🤖</div>
              <h3>Recommend</h3>
              <p>AI analyzes current and historical evidence</p>
            </div>

            <div className="flow-arrow">→</div>

            <div className="flow-step">
              <div className="flow-icon">🔧</div>
              <h3>Resolve</h3>
              <p>Engineer takes action</p>
            </div>

            <div className="flow-arrow">→</div>

            <div className="flow-step">
              <div className="flow-icon">💾</div>
              <h3>Learn</h3>
              <p>Outcome is stored in Hindsight</p>
            </div>

          </div>
        </section>

        {/* Architecture */}
        <section className="card architecture-section">
          <h2>System Architecture</h2>

          <p className="architecture-description">
            IncidentBrain connects the incident dashboard, backend agent,
            Hindsight memory, and Groq LLM to create a continuous incident
            learning loop.
          </p>

          <div className="architecture-flow">

            <div className="architecture-box">
              <div className="architecture-icon">🖥️</div>
              <h3>React Frontend</h3>
              <p>
                Incident dashboard for SRE engineers
              </p>
            </div>

            <div className="architecture-arrow">→</div>

            <div className="architecture-box">
              <div className="architecture-icon">⚙️</div>
              <h3>FastAPI Backend</h3>
              <p>
                Handles investigation and resolution requests
              </p>
            </div>

            <div className="architecture-arrow">→</div>

            <div className="architecture-box">
              <div className="architecture-icon">🤖</div>
              <h3>IncidentBrain Agent</h3>
              <p>
                Combines historical evidence with current incidents
              </p>
            </div>

          </div>

          <div className="architecture-branches">

            <div className="architecture-box">
              <div className="architecture-icon">🧠</div>
              <h3>Hindsight</h3>
              <p>
                Stores and recalls previous incident experiences
              </p>
            </div>

            <div className="architecture-box">
              <div className="architecture-icon">⚡</div>
              <h3>Groq + LLM</h3>
              <p>
                Analyzes evidence and generates recommendations
              </p>
            </div>

          </div>
        </section>

        {/* Incident Investigation */}
        <section className="card">
          <h2>Investigate Incident</h2>

          <textarea
            value={incident}
            onChange={(e) => setIncident(e.target.value)}
            placeholder="Describe the production incident..."
            rows="7"
          />

          <button onClick={investigate} disabled={loading}>
            {loading ? "Investigating..." : "Investigate"}
          </button>
        </section>

        {/* Investigation Result */}
        {result && (
          <section className="card">
            <h2>Investigation Result</h2>

            {result.error ? (
              <p>{result.error}</p>
            ) : (
              <>
                {/* Hindsight Memory */}
                <div className="memory-header">
                  <div>
                    <h3>🧠 Hindsight Memory</h3>

                    <div className="memory-status">
                      ✓ Previous incident knowledge retrieved
                    </div>
                  </div>
                </div>

                <div className="memory-learning-badge">
                  🧠 Memory retrieved from a previous incident
                </div>

                <div className="memory-count">
                  Showing the most relevant previous incident experience
                </div>

                {result.memories_found
                  ?.filter(
                    (memory, index, self) =>
                      index ===
                      self.findIndex((item) => item === memory)
                  )
                  .slice(0, 1)
                  .map((memory, index) => (
                    <div className="memory" key={index}>
                      <div className="memory-number">
                        Memory {index + 1}
                      </div>

                      <div className="memory-content">
                        {memory}
                      </div>
                    </div>
                  ))}

                {/* AI Recommendation */}
                <h3>AI Recommendation</h3>

                <pre className="recommendation">
                  {result.recommendation}
                </pre>

                {/* Resolution / Learning */}
                <div className="learning-section">
                  <h3>Incident Resolution</h3>

                  <p className="learning-description">
                    Tell IncidentBrain what action was taken and what happened.
                    This experience will be stored in Hindsight for future
                    incidents.
                  </p>

                  <label>Action Taken</label>

                  <textarea
                    value={actionTaken}
                    onChange={(e) => setActionTaken(e.target.value)}
                    placeholder="Example: Increased Redis connection pool from 100 to 250."
                    rows="4"
                  />

                  <label>Outcome</label>

                  <textarea
                    value={outcome}
                    onChange={(e) => setOutcome(e.target.value)}
                    placeholder="Example: HTTP 503 error rate returned to normal."
                    rows="4"
                  />

                  <button
                    onClick={resolveIncident}
                    disabled={
                      resolving ||
                      !actionTaken.trim() ||
                      !outcome.trim()
                    }
                  >
                    {resolving ? "Learning..." : "Resolve & Learn"}
                  </button>

                  {learned && (
                    <div className="success-message">
                      ✓ Incident resolution stored in Hindsight.
                      <br />

                      <strong>
                        IncidentBrain learned from this resolution.
                      </strong>
                    </div>
                  )}
                </div>
              </>
            )}
          </section>
        )}

      </main>
    </div>
  );
}

export default App;