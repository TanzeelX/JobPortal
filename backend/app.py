from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from db import db
from routes.job_routes import bp as jobs_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    CORS(app)


    app.register_blueprint(jobs_bp, url_prefix="/api/jobs")


    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to Job Portal API"})

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    def error_response(error, message, code):
        return jsonify({"error": error, "message": message}), code

    @app.errorhandler(400)
    def bad_request(e):
        return error_response("Bad Request", str(getattr(e, "description", e)), 400)

    @app.errorhandler(404)
    def not_found(e):
        return error_response("Not Found", str(getattr(e, "description", e)), 404)

    @app.errorhandler(500)
    def server_error(e):
        return error_response("Server Error", "Unexpected error.", 500)

    return app


if __name__ == "__main__":
    app = create_app()


    with app.app_context():
        db.create_all()


        print("\n✅ Registered routes:")
        for rule in app.url_map.iter_rules():
            methods = ",".join(rule.methods)
            print(f"{rule} -> [{methods}]")

    app.run(host="0.0.0.0", port=5000, debug=True)
