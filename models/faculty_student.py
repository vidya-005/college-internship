from extensions import db


class FacultyStudent(db.Model):

    __tablename__ = "faculty_students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculty.id"),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    assigned_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    faculty = db.relationship(
        "Faculty",
        backref=db.backref(
            "student_assignments",
            lazy=True
        )
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "faculty_assignments",
            lazy=True
        )
    )

    __table_args__ = (
        db.UniqueConstraint(
            "faculty_id",
            "student_id",
            name="unique_faculty_student"
        ),
    )