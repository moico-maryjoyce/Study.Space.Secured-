from flask import Flask

from app.views.login import bp as login_bp
from app.views.dashboard import bp as dashboard_bp
from app.views.check_inout import bp as check_inout_bp
from app.views.my_profile import bp as profile_bp
from app.views.my_profile_2 import bp as profile2_bp
from app.views.users import bp as users_bp
from app.views.audit_logs import bp as audit_bp
from app.views.settings import bp as settings_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(check_inout_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(profile2_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(settings_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
