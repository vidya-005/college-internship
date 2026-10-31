from extensions import db


class DailyLog(db.Model):

    __tablename__ = "daily_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False
    )

    log_date = db.Column(
        db.Date,
        nullable=False
    )

    task = db.Column(
        db.Text,
        nullable=False
    )

    hours_worked = db.Column(
        db.Float,
        nullable=False
    )

    technology_used = db.Column(
        db.String(300),
        nullable=True
    )

    remarks = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    review_status = db.Column(
        db.String(30),
        nullable=False,
        default="Submitted"
    )

    faculty_remarks = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    student = db.relationship(
        "Student",
        backref=db.backref("daily_logs", lazy=True)
    )

    project = db.relationship(
        "Project",
        backref=db.backref("daily_logs", lazy=True)
    )

    def __repr__(self):
        return f"<DailyLog {self.log_date}>"