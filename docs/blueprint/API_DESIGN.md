# REST API Architecture

A minimal, deterministic JSON-based REST API managed by Flask routes.

---

### POST `/api/v1/metrics/classify`
Receives current DOM metrics, calls the Logistic Regression Joblist, and responds with the targeted classification output map.

**Request:**
```json
{
  "typing_speed": 34.5,
  "error_rate": 0.45,
  "pause_time": 6800.0
}
```

**Response (200 OK):**
```json
{
  "literacy_level": "low",
  "suggest_easy_mode": true
}
```

---

### GET `/api/v1/locations/suggest`
Smart Autofill fuzzy matching API endpoint. Looks up geographic parameters directly via SQLite `LIKE` or manual Levenshtein implementations if supported directly via Python extensions. 

**Query Parameters:**
- `query` (ex: "pau")
- `type` (ex: "district")

**Response (200 OK):**
```json
{
  "suggestions": [
    {"id": 16, "name": "Pauri Garhwal", "type": "district"}
  ]
}
```

---

### POST `/api/v1/form/submit`
The overarching submission route. This handles both normal live connections and background-synced drops from IndexedDB.

**Request:**
```json
{
  "session_id": "45d-r38",
  "payload": {
    "district": "Pauri Garhwal",
    "tehsil": "Bironkhal",
    "village": "Sila"
  },
  "metadata": {
    "mode": "easy",
    "background_synced": false
  }
}
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Form registered dynamically"
}
```
