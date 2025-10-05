from db import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    posting_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    job_type = db.Column(db.String(50))
    tags = db.Column(db.String(255))
    link = db.Column(db.String(255), nullable=True, default="")  # ✅ Added safely

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "posting_date": self.posting_date.isoformat() if self.posting_date else None,
            "job_type": self.job_type,
            "tags": self.tags,
            "link": self.link
        }
