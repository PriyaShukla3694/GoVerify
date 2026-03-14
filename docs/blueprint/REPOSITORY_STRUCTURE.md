# Repository Structure Blueprint

This strict separation of concerns allows distinct team members to operate parallelly over the 48-hour timeline cleanly.

```text
adaptive-citizen-interface/
├── frontend/                  # React + PWA workspace
│   ├── public/                # Static caching boundaries, service_worker.js hooks
│   ├── src/
│   │   ├── components/        # Isolated UI components (StandardView, EasyView)
│   │   ├── hooks/             # telemetry tracking (useKeyboardMetrics.jsx)
│   │   ├── api/               # Abstracted fetch integrations / idb wrapper logic
│   │   ├── App.jsx            # State context manager matching screens
│   │   └── index.css          # Tailwind pipeline
│   ├── package.json
│   └── vite.config.js         
│
├── backend/                   # Flask python orchestration
│   ├── app.py                 # Core routing file & CORS setup
│   ├── database.py            # SQLite wrapper class implementations
│   ├── model_runner.py        # Isolated layer targeting loading joblib artifacts
│   ├── requirements.txt
│   └── data/
│       └── db.sqlite          # Actual physical db location 
│
├── model_trainer/             # Purely isolated modeling scripting (not ran in prod)
│   ├── generate_synthetic_data.py
│   ├── train_classifier.py
│   └── exported_model.joblib  # Artifact strictly copied over to the backend/ dir
│
└── docs/                      # Architectural logic (current)
    └── blueprint/
```
