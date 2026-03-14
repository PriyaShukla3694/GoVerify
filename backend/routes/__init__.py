from .upload import upload_bp
from .process import process_bp
from .report import report_bp
from .officer import officer_bp

def init_app_routes(app):
    app.register_blueprint(upload_bp)
    app.register_blueprint(process_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(officer_bp)
