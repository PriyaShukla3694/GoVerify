# System Architecture

## 1. High-Level Architecture
Given the aggressive 48-hour timeline and zero-cost constraints, the system focuses on a clean client-server architecture combined with local offline resilience.

- **Client (Frontend)**: React.js application equipped with Progressive Web App (PWA) configurations. It orchestrates the adaptive UI structure and captures behavioral telemetry organically.
- **Server (Backend)**: Python Flask lightweight API backend. It coordinates incoming data streams, executes machine learning models via serialized objects, and manages persistent relational data.
- **Database**: SQLite. A highly reliable, serverless database ideal for a 48-hour hackathon, eliminating networking and external service overhead.

## 2. Data Flow Architecture
1. **User Interaction**: Citizen begins typing out the form in the React interface. The browser runtime starts aggregating behavioral data.
2. **Behavior Inference Request**: After initial signals are aggregated, an asynchronous background request sends this telemetry payload to the Flask backend.
3. **ML Processing**: The Python runtime passes the payload to a pre-trained scikit-learn Logistic Regression engine, retrieving an interference decision.
4. **Adaptive UI Activation**: If marked 'Low Literacy', the React API receives a flag to interrupt the citizen and suggest switching cleanly into "Easy Mode" conversation interface.
5. **Offline Data Pipeline**: If internet is not available, form data and telemetry are dumped into local `IndexedDB`. When a network ping successfully completes, a background Service Worker synchronizes the local cache with the remote Flask DB.

## 3. Conceptual Component Diagram
```text
[ React PWA (UI & Offline Storage) ] <---> [ Service Worker (Network Proxy) ]
                 |                                      |
         (Offline Data)                         (REST API Calls)
                 v                                      v
       [ LocalStorage / IndexedDB ]             [ Flask Backend ]
                                                        |
                                       +----------------+----------------+
                                       |                                 |
                          [ SQLite Database ]               [ scikit-learn ML Model ]
```
