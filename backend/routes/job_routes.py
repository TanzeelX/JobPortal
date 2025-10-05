from flask import Blueprint, request, jsonify, abort, current_app
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models import Job
from db import db
import traceback

bp = Blueprint("jobs", __name__)


ALLOWED_JOB_TYPES = ['full-time', 'part-time', 'contract', 'internship', 'temporary', 'remote']


def validate_required_fields(data, required_fields):
    missing = [f for f in required_fields if not data.get(f) or (isinstance(data.get(f), str) and not data.get(f).strip())]
    if missing:
        abort(400, description=f"Missing or empty required fields: {', '.join(missing)}")


def validate_string_length(value, field_name, max_length):
    if value and len(value) > max_length:
        abort(400, description=f"{field_name} exceeds maximum length of {max_length} characters")


def parse_iso_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        abort(400, description="Invalid date format. Use ISO 8601 format (e.g., 2024-01-01T10:30:00)")


def normalize_tags(tags):
    if tags is None:
        return None
    if isinstance(tags, list):
        normalized = [t.strip().lower() for t in tags if isinstance(t, str) and t.strip()]
    elif isinstance(tags, str):
        normalized = [t.strip().lower() for t in tags.split(",") if t.strip()]
    else:
        abort(400, description="Tags must be a string or array of strings")
    return ",".join(normalized) if normalized else None


def validate_job_type(job_type):
    if job_type and job_type.lower() not in ALLOWED_JOB_TYPES:
        abort(400, description=f"Invalid job_type. Allowed values: {', '.join(ALLOWED_JOB_TYPES)}")
    return job_type.lower() if job_type else None


def sanitize_query_param(value):
    if not value:
        return None
    dangerous_chars = ['%', '_', '\\', "'", '"', ';', '--']
    sanitized = str(value).strip()
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized if sanitized else None



@bp.route("", methods=["GET"])
@bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Job Portal API",
        "version": "1.0",
        "endpoints": {
            "list_jobs": "GET /api/jobs",
            "create_job": "POST /api/jobs",
            "get_job": "GET /api/jobs/<id>",
            "update_job": "PUT/PATCH /api/jobs/<id>",
            "delete_job": "DELETE /api/jobs/<id>"
        }
    }), 200


@bp.route("", methods=["POST"])
def create_job():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Validation error", "message": "Request body must be valid JSON"}), 400


        title = (data.get("title") or "").strip()
        company = (data.get("company") or "").strip()
        locations = data.get("locations") or []
        if isinstance(locations, str):
            locations = [loc.strip() for loc in locations.split(",") if loc.strip()]
        location = locations[0] if locations else (data.get("location") or "").strip()

        if not title or not company or not location:
            return jsonify({"error": "Validation error", "message": "Title, company, and location required"}), 400


        tags = data.get("tags") or []
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(",") if tag.strip()]


        tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags or "")

        posting_date = parse_iso_date(data.get("posting_date")) or datetime.utcnow()
        job_type = validate_job_type(data.get("job_type"))


        validate_string_length(title, "title", 120)
        validate_string_length(company, "company", 120)
        validate_string_length(location, "location", 120)
        validate_string_length(tags_str, "tags", 255)


        existing = Job.query.filter_by(title=title, company=company, location=location).first()
        if existing:
            return jsonify({"error": "Duplicate", "message": "Job already exists"}), 400


        job = Job(
            title=title,
            company=company,
            location=location,
            posting_date=posting_date,
            job_type=job_type,
            tags=tags_str
        )

        db.session.add(job)
        db.session.commit()

        return jsonify({"message": "Job created successfully", "job": job.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating job: {e}")
        traceback.print_exc()
        return jsonify({"error": "Server Error", "message": str(e)}), 500

        
@bp.route("/list", methods=["GET"])
def list_jobs():
    """List jobs with optional pagination & sorting"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        sort_by = request.args.get("sort_by", "posting_date")
        order = request.args.get("order", "desc")

        query = Job.query

        if hasattr(Job, sort_by):
            query = query.order_by(desc(getattr(Job, sort_by)) if order == "desc" else asc(getattr(Job, sort_by)))

        jobs = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            "jobs": [job.to_dict() for job in jobs.items],
            "page": jobs.page,
            "pages": jobs.pages,
            "total": jobs.total
        })
    except SQLAlchemyError:
        abort(500, description="Failed to fetch jobs")



@bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        abort(404, description=f"Job with id {job_id} not found")
    return jsonify(job.to_dict()), 200


@bp.route("/<int:job_id>", methods=["PUT", "PATCH"])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        abort(404, description=f"Job with id {job_id} not found")

    data = request.get_json()

    if "title" in data:
        job.title = data["title"].strip()
    if "company" in data:
        job.company = data["company"].strip()
    if "location" in data:
        job.location = data["location"].strip()
    if "posting_date" in data:
        try:
            job.posting_date = datetime.fromisoformat(data["posting_date"])
        except ValueError:
            abort(400, description="Invalid posting_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
    if "job_type" in data:
        job.job_type = validate_job_type(data["job_type"])
    if "tags" in data:
        job.tags = ", ".join(data["tags"]) if isinstance(data["tags"], list) else data["tags"]

    db.session.commit()
    return jsonify(job.to_dict()), 200

@bp.route("/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        abort(404, description=f"Job with id {job_id} not found")

    try:
        db.session.delete(job)
        db.session.commit()
        return jsonify({"message": f"Job ID {job_id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting job: {e}")
        traceback.print_exc()
        return jsonify({"error": "Server Error", "message": str(e)}), 500
