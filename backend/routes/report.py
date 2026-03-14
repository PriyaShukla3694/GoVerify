from flask import Blueprint, jsonify
from services.reporter import generate_report

report_bp = Blueprint('report', __name__)

@report_bp.route('/api/v1/applications/<application_id>/report', methods=['GET'])
def get_report(application_id):
    report = generate_report(application_id)
    if "error" in report:
        return jsonify(report), 404
    return jsonify(report), 200
