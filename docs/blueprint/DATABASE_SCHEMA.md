# Database Schema Design

Optimized strictly for SQLite relation handling targeting the minimal requirements of the 48-hour BLOCKATHON.

```sql
-- Track generic user sessions uniquely interacting with the demo platform
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    inferred_literacy_level TEXT, -- Enum-like string: 'low', 'medium', 'high'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Store final government form submissions
CREATE TABLE form_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    district TEXT,
    tehsil TEXT,
    village TEXT,
    form_mode_used TEXT, -- 'standard' or 'easy'
    is_synced BOOLEAN DEFAULT 1,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES users(session_id)
);

-- Internal Geographic Dictionary lookup table targeting the Smart Autofill API
CREATE TABLE locations_dictionary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_type TEXT NOT NULL, -- 'district', 'tehsil', 'village'
    name TEXT NOT NULL,
    parent_id INTEGER NULL -- Enables strict hierarchical geographical filtering
);

-- Analytical log data evaluating AI metric performances
CREATE TABLE behavior_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    typing_speed FLOAT,
    error_rate FLOAT,
    pause_time FLOAT,
    classified_as TEXT
);
```
