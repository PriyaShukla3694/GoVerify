from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    inferred_literacy_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Metadata submitted by user
    provided_name = db.Column(db.String(255))
    provided_dob = db.Column(db.String(50))
    provided_address = db.Column(db.Text)
    
    # Status and metrics
    status = db.Column(db.String(50), default='uploaded')  # uploaded, processed, flagged_for_review, approved, rejected
    overall_confidence = db.Column(db.Float)
    recommendation = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = db.relationship('Document', backref='application', lazy=True)
    validation_results = db.relationship('ValidationResult', backref='application', uselist=False)
    officer_review = db.relationship('OfficerReview', backref='application', uselist=False)

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    application_id = db.Column(db.String(36), db.ForeignKey('applications.id'), nullable=False)
    
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    compressed_path = db.Column(db.String(500))
    file_size_bytes = db.Column(db.Integer)
    compressed_size_bytes = db.Column(db.Integer)
    
    document_type = db.Column(db.String(50)) # aadhaar, pan, etc.
    ocr_confidence = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # One to many extracted fields
    extracted_fields = db.relationship('ExtractedField', backref='document', lazy=True)

class ExtractedField(db.Model):
    __tablename__ = 'extracted_fields'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.String(36), db.ForeignKey('documents.id'), nullable=False)
    
    field_name = db.Column(db.String(100), nullable=False)
    field_value = db.Column(db.Text)
    confidence = db.Column(db.Float)

class ValidationResult(db.Model):
    __tablename__ = 'validation_results'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(36), db.ForeignKey('applications.id'), nullable=False)
    
    name_match = db.Column(db.Boolean)
    dob_match = db.Column(db.Boolean)
    address_match = db.Column(db.Boolean)
    
    # JSON-encoded array of mismatched properties/reasons
    mismatches = db.Column(db.Text) 
    field_confidence_scores = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OfficerReview(db.Model):
    __tablename__ = 'officer_reviews'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(36), db.ForeignKey('applications.id'), nullable=False)
    officer_id = db.Column(db.String(100), default="demo_officer")
    
    decision = db.Column(db.String(50)) # approved, rejected
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Legacy tables from the previous hackathon step (for telemetry/sync forms)
class FormSubmission(db.Model):
    __tablename__ = 'form_submissions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    district = db.Column(db.String(255))
    tehsil = db.Column(db.String(255))
    village = db.Column(db.String(255))
    form_mode_used = db.Column(db.String(50))
    is_synced = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class LocationDictionary(db.Model):
    __tablename__ = 'locations_dictionary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location_type = db.Column(db.String(50), nullable=False) # district, tehsil, village
    parent_id = db.Column(db.Integer)

class BehaviorLog(db.Model):
    __tablename__ = 'behavior_logs'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    typing_speed = db.Column(db.Float)
    error_rate = db.Column(db.Float)
    pause_time = db.Column(db.Float)
    classified_as = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
