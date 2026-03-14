from flask import Blueprint, jsonify, request
from models import db, Application, OfficerReview
from services.reporter import generate_report

officer_bp = Blueprint('officer', __name__)

@officer_bp.route('/api/v1/officer/queue', methods=['GET'])
def get_queue():
    # Filter applications by confidence / review status
    confidence_filter = request.args.get('confidence') # low, medium, all
    
    query = Application.query.filter(Application.status == 'flagged_for_review')
    
    if confidence_filter == 'low':
        query = query.filter(Application.overall_confidence < 0.70)
    elif confidence_filter == 'medium':
        query = query.filter(Application.overall_confidence >= 0.70, Application.overall_confidence < 0.90)
        
    apps = query.order_by(Application.created_at.asc()).all()
    
    results = []
    for app in apps:
        results.append({
            "id": app.id,
            "submitted_name": app.provided_name,
            "overall_confidence": app.overall_confidence,
            "timestamp": app.created_at
        })
        
    return jsonify({"queue": results, "total": len(results)}), 200

@officer_bp.route('/api/v1/officer/applications/<application_id>', methods=['GET'])
def get_application(application_id):
    report = generate_report(application_id)
    if "error" in report:
        return jsonify(report), 404
        
    # We could also bundle original and compressed image paths securely here 
    # but for Hackathon MVP, the report data suffices
    return jsonify(report), 200

@officer_bp.route('/api/v1/officer/applications/<application_id>/review', methods=['POST'])
def submit_review(application_id):
    app = Application.query.get(application_id)
    if not app:
        return jsonify({"error": "Application not found"}), 404
        
    data = request.json
    decision = data.get('decision') # 'approved' or 'rejected'
    notes = data.get('notes', '')
    
    if decision not in ['approved', 'rejected']:
        return jsonify({"error": "Invalid decision"}), 400
        
    review = OfficerReview(
        application_id=application_id,
        decision=decision,
        notes=notes
    )
    db.session.add(review)
    
    app.status = decision
    db.session.commit()
    
    return jsonify({"status": "success", "message": f"Application {decision}"}), 200

@officer_bp.route('/api/v1/officer/stats', methods=['GET'])
def get_stats():
    total_reviewed = OfficerReview.query.count()
    total_approved = OfficerReview.query.filter_by(decision='approved').count()
    
    rate = (total_approved / total_reviewed * 100) if total_reviewed > 0 else 0
    
    return jsonify({
        "total_reviewed": total_reviewed,
        "approval_rate": round(rate, 2)
    }), 200
