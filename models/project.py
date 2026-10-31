from extensions import db


class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    project_title = db.Column(
        db.String(200),
        nullable=False
    )

    project_type = db.Column(
        db.String(50),
        nullable=False
    )

    technology = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    start_date = db.Column(
        db.Date,
        nullable=True
    )

    end_date = db.Column(
        db.Date,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    github_link = db.Column(
        db.String(300),
        nullable=True
    )

    

    student = db.relationship(
        "Student",
        backref=db.backref(
            "projects",
            lazy=True
        )
    )

    

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):

        return f"<Project {self.project_title}>"
    

    faculty_feedback = db.Column(
        db.Text,
        nullable=True
    )
    
    evaluation_marks = db.Column(
        db.Integer,
        nullable=True
    )
    
    evaluated_at = db.Column(
        db.DateTime,
        nullable=True
    )