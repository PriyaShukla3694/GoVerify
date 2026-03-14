import os
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, User, Application, BehaviorLog, LocationDictionary, FormSubmission

app = Flask(__name__)
app.config.from_object(Config)

CORS(app) # Allow React frontend to access API
db.init_app(app)

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model_trainer', 'exported_model.joblib')
classifier = None
try:
    if os.path.exists(MODEL_PATH):
        classifier = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Could not load model from {MODEL_PATH}")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

# Legacy Endpoints from the Dashboard Hackathon Step
@app.route('/api/v1/session', methods=['GET'])
def get_session():
    import uuid
    return jsonify({"session_id": str(uuid.uuid4())})

@app.route('/api/v1/metrics/classify', methods=['POST'])
def classify_metrics():
    data = request.json
    typing_speed = data.get('typing_speed', 0)
    error_rate = data.get('error_rate', 0.0)
    pause_time = data.get('pause_time', 0.0)
    session_id = data.get('session_id')

    literacy_level = "medium"
    suggest_easy_mode = False

    if classifier:
        prediction = classifier.predict([[typing_speed, error_rate, pause_time]])
        literacy_level = prediction[0]
        if literacy_level == 'low':
            suggest_easy_mode = True

    if session_id:
        user = User.query.filter_by(session_id=session_id).first()
        if not user:
            user = User(session_id=session_id)
            db.session.add(user)
        
        log = BehaviorLog(
            session_id=session_id,
            typing_speed=typing_speed,
            error_rate=error_rate,
            pause_time=pause_time,
            classified_as=literacy_level
        )
        db.session.add(log)
        
        user.inferred_literacy_level = literacy_level
        db.session.commit()

    return jsonify({"literacy_level": literacy_level, "suggest_easy_mode": suggest_easy_mode}), 200

@app.route('/api/v1/locations/suggest', methods=['GET'])
def suggest_locations():
    query = request.args.get('query', '')
    loc_type = request.args.get('type', 'district')
    if len(query) < 2:
        return jsonify({"suggestions": []})
        
    results = LocationDictionary.query.filter(
        LocationDictionary.location_type == loc_type,
        LocationDictionary.name.like(f"{query}%")
    ).limit(5).all()

    return jsonify({"suggestions": [{"id": r.id, "name": r.name, "type": r.location_type} for r in results]}), 200

@app.route('/api/v1/form/submit', methods=['POST'])
def submit_form():
    data = request.json
    session_id = data.get('session_id')
    payload = data.get('payload', {})
    metadata = data.get('metadata', {})
    
    if session_id:
        user = User.query.filter_by(session_id=session_id).first()
        if not user:
            user = User(session_id=session_id)
            db.session.add(user)
            
        submission = FormSubmission(
            session_id=session_id,
            district=payload.get('district'),
            tehsil=payload.get('tehsil'),
            village=payload.get('village'),
            form_mode_used=metadata.get('mode', 'standard'),
            is_synced=metadata.get('background_synced', False)
        )
        db.session.add(submission)
        db.session.commit()

    return jsonify({"status": "success", "message": "Form registered dynamically"}), 201

# Allow app routes to be registered from other files
from routes import init_app_routes
init_app_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
