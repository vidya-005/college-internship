from extensions import db


class Internship(db.Model):

    __tablename__ = "internships"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    company_name = db.Column(
        db.String(150),
        nullable=False
    )

    internship_title = db.Column(
        db.String(150),
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
    )

    mode = db.Column(
        db.String(30),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "internships",
            lazy=True
        )
    )

    def __repr__(self):
        return f"<Internship {self.company_name}>"