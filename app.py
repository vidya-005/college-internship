from flask import Flask, render_template, request, redirect, url_for, session,flash

from config import Config
from extensions import db

from models.user import User
from models.student import Student
from models.faculty import Faculty
from models.internship import Internship
from models.project import Project
from models.daily_log import DailyLog
from models.faculty_student import FacultyStudent
from datetime import datetime


app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize database
db.init_app(app)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template("home.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            # Admin
            if user.role == "admin":
                return redirect(url_for("dashboard"))

            # Student
            elif user.role == "student":
                return redirect(url_for("student_dashboard"))
            elif user.role == "faculty":
                return redirect(url_for("faculty_dashboard"))

            else:
                flash("Invalid user role.", "danger")
                return redirect(url_for("login"))

        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")



@app.route("/student-dashboard")
def student_dashboard():

    # Make sure user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Make sure only students can access this page
    if session.get("role") != "student":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("login"))

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("login"))

    # Get this student's projects
    projects = Project.query.filter_by(
        student_id=student.id
    ).order_by(
        Project.created_at.desc()
    ).all()

    # Get a GitHub link from the student's latest project
    github_link = next(
        (
            project.github_link
            for project in projects
            if project.github_link
        ),
        None
    )

    return render_template(
        "student_dashboard.html",
        student=student,
        github_link=github_link
    )
@app.route("/faculty-dashboard")
def faculty_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "faculty":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    faculty = Faculty.query.filter_by(
        user_id=user.id
    ).first()

    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("login"))

    return render_template(
        "faculty_dashboard.html",
        faculty=faculty
    )


@app.route("/faculty-profile")
def faculty_profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "faculty":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    faculty = Faculty.query.filter_by(
        user_id=user.id
    ).first()

    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("faculty_dashboard"))

    return render_template(
        "faculty_profile.html",
        faculty=faculty
    )

@app.route("/student-profile")
def student_profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "student":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("student_dashboard"))

    return render_template(
        "student_profile.html",
        student=student
    )



@app.route("/student-internship")
def student_internship():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "student":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("student_dashboard"))

    internships = Internship.query.filter_by(
        student_id=student.id
    ).order_by(
        Internship.start_date.desc()
    ).all()

    return render_template(
        "student_internship.html",
        student=student,
        internships=internships
    )


@app.route("/student-project")
def student_project():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "student":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("student_dashboard"))

    projects = Project.query.filter_by(
        student_id=student.id
    ).order_by(
        Project.start_date.desc()
    ).all()

    return render_template(
        "student_project.html",
        student=student,
        projects=projects
    )


@app.route("/student-daily-logs")
def student_daily_logs():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "student":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("student_dashboard"))

    logs = DailyLog.query.filter_by(
        student_id=student.id
    ).order_by(
        DailyLog.log_date.desc()
    ).all()

    return render_template(
        "student_daily_logs.html",
        student=student,
        logs=logs
    )

@app.route("/student-daily-logs/add", methods=["GET", "POST"])
def add_student_daily_log():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "student":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    student = Student.query.filter_by(
        user_id=user.id
    ).first()

    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("student_dashboard"))

    # Get only this student's projects
    projects = Project.query.filter_by(
        student_id=student.id
    ).order_by(
        Project.project_title.asc()
    ).all()

    if request.method == "POST":

        project_id = request.form["project_id"]

        # Security check:
        # Make sure the selected project belongs to this student
        project = Project.query.filter_by(
            id=project_id,
            student_id=student.id
        ).first()

        if not project:
            flash("Invalid project selected.", "danger")
            return redirect(url_for("add_student_daily_log"))

        log = DailyLog(
            student_id=student.id,
            project_id=project.id,
            log_date=request.form["log_date"],
            task=request.form["task"],
            hours_worked=request.form["hours_worked"],
            technology_used=request.form["technology_used"],
            remarks=request.form["remarks"],
            status=request.form["status"],
            review_status="Submitted"
        )

        db.session.add(log)
        db.session.commit()

        flash("Daily log submitted successfully.", "success")

        return redirect(url_for("student_daily_logs"))

    return render_template(
        "add_student_daily_log.html",
        student=student,
        projects=projects
    )

@app.route("/faculty-daily-logs")
def faculty_daily_logs():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "faculty":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    faculty = Faculty.query.filter_by(
        user_id=user.id
    ).first()

    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("login"))

    logs = DailyLog.query.order_by(
        DailyLog.log_date.desc()
    ).all()

    return render_template(
        "faculty_daily_logs.html",
        faculty=faculty,
        logs=logs
    )
    
@app.route("/faculty-daily-logs/review/<int:id>", methods=["GET", "POST"])
def review_daily_log(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "faculty":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    faculty = Faculty.query.filter_by(
        user_id=user.id
    ).first()

    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("login"))

    log = DailyLog.query.get_or_404(id)

    if request.method == "POST":

        review_status = request.form["review_status"]
        faculty_remarks = request.form["faculty_remarks"]

        if review_status not in ["Approved", "Rejected"]:
            flash("Invalid review status.", "danger")
            return redirect(
                url_for("review_daily_log", id=id)
            )

        log.review_status = review_status
        log.faculty_remarks = faculty_remarks

        db.session.commit()

        flash(
            f"Daily log {review_status.lower()} successfully.",
            "success"
        )

        return redirect(url_for("faculty_daily_logs"))

    return render_template(
        "review_daily_log.html",
        faculty=faculty,
        log=log
    )
# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"]
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ==========================================
# TEST DATABASE
# ==========================================

@app.route("/test-db")
def test_db():

    try:

        db.session.execute(
            db.text("SELECT 1")
        )

        return """
        <h1>Database Connected Successfully!</h1>
        <p>Flask is connected to MySQL.</p>
        """

    except Exception as e:

        return f"""
        <h1>Database Connection Failed</h1>
        <p>{e}</p>
        """


# ==========================================
# VIEW + SEARCH STUDENTS
# ==========================================

@app.route("/students")
def students():

    if "user_id" not in session:

        return redirect(url_for("login"))

    search = request.args.get("search", "")

    if search:

        student_list = Student.query.filter(
            db.or_(
                Student.name.like(f"%{search}%"),
                Student.usn.like(f"%{search}%")
            )
        ).all()

    else:

        student_list = Student.query.all()

    return render_template(
        "students.html",
        students=student_list,
        search=search
    )


# ==========================================
# ADD STUDENT
# ==========================================

@app.route("/students/add", methods=["GET", "POST"])
def add_student():

    if "user_id" not in session:

        return redirect(url_for("login"))

    if request.method == "POST":

        usn = request.form["usn"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        semester = request.form["semester"]

        student = Student(
            usn=usn,
            name=name,
            email=email,
            phone=phone,
            course=course,
            semester=semester
        )

        db.session.add(student)

        db.session.commit()

        return redirect(url_for("students"))

    return render_template("add_student.html")


# ==========================================
# EDIT STUDENT
# ==========================================

@app.route(
    "/students/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_student(id):

    if "user_id" not in session:

        return redirect(url_for("login"))

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.usn = request.form["usn"]
        student.name = request.form["name"]
        student.email = request.form["email"]
        student.phone = request.form["phone"]
        student.course = request.form["course"]
        student.semester = request.form["semester"]

        db.session.commit()

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student
    )


# ==========================================
# DELETE STUDENT
# ==========================================

@app.route("/students/delete/<int:id>")
def delete_student(id):

    if "user_id" not in session:

        return redirect(url_for("login"))

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    return redirect(url_for("students"))



@app.route("/students/create-login/<int:id>", methods=["GET", "POST"])
def create_student_login(id):

    student = Student.query.get_or_404(id)

    # Check whether login already exists
    if student.user_id:
        flash("Login account already exists for this student.", "warning")
        return redirect(url_for("students"))

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Check username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists. Please choose another username.", "danger")
            return render_template(
                "create_student_login.html",
                student=student
            )

        # Create user account
        user = User(
            username=username,
            role="student"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Connect student with user
        student.user_id = user.id

        db.session.commit()

        flash("Student login account created successfully.", "success")

        return redirect(url_for("students"))

    return render_template(
        "create_student_login.html",
        student=student
    )



@app.route("/faculty/create-login/<int:id>", methods=["GET", "POST"])
def create_faculty_login(id):

    faculty = Faculty.query.get_or_404(id)

    if faculty.user_id:
        flash(
            "Login account already exists for this faculty.",
            "warning"
        )
        return redirect(url_for("faculty"))

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash(
                "Username already exists. Please choose another username.",
                "danger"
            )

            return render_template(
                "create_faculty_login.html",
                faculty=faculty
            )

        user = User(
            username=username,
            role="faculty"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        faculty.user_id = user.id

        db.session.commit()

        flash(
            "Faculty login account created successfully.",
            "success"
        )

        return redirect(url_for("faculty"))

    return render_template(
        "create_faculty_login.html",
        faculty=faculty
    )


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

@app.route("/faculty")
def faculty():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    if search:

        faculty_list = Faculty.query.filter(
            db.or_(
                Faculty.name.like(f"%{search}%"),
                Faculty.faculty_id.like(f"%{search}%")
            )
        ).all()

    else:

        faculty_list = Faculty.query.all()

    return render_template(
        "faculty.html",
        faculty_list=faculty_list,
        search=search
    )


@app.route("/faculty/add", methods=["GET", "POST"])
def add_faculty():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        faculty_id = request.form["faculty_id"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        designation = request.form["designation"]

        faculty_member = Faculty(
            faculty_id=faculty_id,
            name=name,
            email=email,
            phone=phone,
            department=department,
            designation=designation
        )

        db.session.add(faculty_member)
        db.session.commit()

        return redirect(url_for("faculty"))

    return render_template("add_faculty.html")

@app.route(
    "/faculty/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_faculty(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    faculty_member = Faculty.query.get_or_404(id)

    if request.method == "POST":

        faculty_member.faculty_id = request.form["faculty_id"]
        faculty_member.name = request.form["name"]
        faculty_member.email = request.form["email"]
        faculty_member.phone = request.form["phone"]
        faculty_member.department = request.form["department"]
        faculty_member.designation = request.form["designation"]

        db.session.commit()

        return redirect(url_for("faculty"))

    return render_template(
        "edit_faculty.html",
        faculty=faculty_member
    )


@app.route("/faculty/delete/<int:id>")
def delete_faculty(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    faculty_member = Faculty.query.get_or_404(id)

    db.session.delete(faculty_member)
    db.session.commit()

    return redirect(url_for("faculty"))


@app.route("/internships")
def internships():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    if search:

        internship_list = Internship.query.join(
            Student
        ).filter(
            db.or_(
                Internship.company_name.like(
                    f"%{search}%"
                ),
                Student.name.like(
                    f"%{search}%"
                )
            )
        ).all()

    else:

        internship_list = Internship.query.all()

    return render_template(
        "internships.html",
        internships=internship_list,
        search=search
    )

@app.route(
    "/internships/add",
    methods=["GET", "POST"]
)
def add_internship():

    if "user_id" not in session:
        return redirect(url_for("login"))

    students = Student.query.all()

    if request.method == "POST":

        student_id = request.form["student_id"]
        company_name = request.form["company_name"]
        internship_title = request.form["internship_title"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        mode = request.form["mode"]
        status = request.form["status"]
        description = request.form["description"]

        internship = Internship(
            student_id=student_id,
            company_name=company_name,
            internship_title=internship_title,
            start_date=start_date,
            end_date=end_date,
            mode=mode,
            status=status,
            description=description
        )

        db.session.add(internship)

        db.session.commit()

        return redirect(url_for("internships"))

    return render_template(
        "add_internship.html",
        students=students
    )

@app.route(
    "/internships/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_internship(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    internship = Internship.query.get_or_404(id)

    students = Student.query.all()

    if request.method == "POST":

        internship.student_id = request.form["student_id"]

        internship.company_name = request.form[
            "company_name"
        ]

        internship.internship_title = request.form[
            "internship_title"
        ]

        internship.start_date = request.form[
            "start_date"
        ]

        internship.end_date = request.form[
            "end_date"
        ]

        internship.mode = request.form["mode"]

        internship.status = request.form["status"]

        internship.description = request.form[
            "description"
        ]

        db.session.commit()

        return redirect(url_for("internships"))

    return render_template(
        "edit_internship.html",
        internship=internship,
        students=students
    )

@app.route("/internships/delete/<int:id>")
def delete_internship(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    internship = Internship.query.get_or_404(id)

    db.session.delete(internship)

    db.session.commit()

    return redirect(url_for("internships"))


@app.route("/projects")
def projects():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    if search:

        project_list = Project.query.join(
            Student
        ).filter(
            db.or_(
                Project.project_title.like(
                    f"%{search}%"
                ),
                Student.name.like(
                    f"%{search}%"
                )
            )
        ).all()

    else:

        project_list = Project.query.all()

    return render_template(
        "projects.html",
        projects=project_list,
        search=search
    )


@app.route(
    "/projects/add",
    methods=["GET", "POST"]
)
def add_project():

    if "user_id" not in session:
        return redirect(url_for("login"))

    students = Student.query.all()

    if request.method == "POST":

        student_id = request.form["student_id"]

        project_title = request.form[
            "project_title"
        ]

        project_type = request.form[
            "project_type"
        ]

        technology = request.form[
            "technology"
        ]

        description = request.form[
            "description"
        ]

        start_date = request.form[
            "start_date"
        ]

        end_date = request.form[
            "end_date"
        ]

        status = request.form[
            "status"
        ]

        github_link = request.form[
            "github_link"
        ]

        project = Project(

            student_id=student_id,

            project_title=project_title,

            project_type=project_type,

            technology=technology,

            description=description,

            start_date=start_date,

            end_date=end_date,

            status=status,

            github_link=github_link

        )

        db.session.add(project)

        db.session.commit()

        return redirect(
            url_for("projects")
        )

    return render_template(
        "add_project.html",
        students=students
    )

@app.route(
    "/projects/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_project(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    project = Project.query.get_or_404(id)

    students = Student.query.all()

    if request.method == "POST":

        project.student_id = request.form[
            "student_id"
        ]

        project.project_title = request.form[
            "project_title"
        ]

        project.project_type = request.form[
            "project_type"
        ]

        project.technology = request.form[
            "technology"
        ]

        project.description = request.form[
            "description"
        ]

        project.start_date = request.form[
            "start_date"
        ]

        project.end_date = request.form[
            "end_date"
        ]

        project.status = request.form[
            "status"
        ]

        project.github_link = request.form[
            "github_link"
        ]

        db.session.commit()

        return redirect(
            url_for("projects")
        )

    return render_template(
        "edit_project.html",
        project=project,
        students=students
    )

@app.route("/projects/delete/<int:id>")
def delete_project(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    project = Project.query.get_or_404(id)

    db.session.delete(project)

    db.session.commit()

    return redirect(
        url_for("projects")
    )

@app.route("/daily-logs")
def daily_logs():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    if search:

        log_list = DailyLog.query.join(
            Student
        ).join(
            Project
        ).filter(
            db.or_(
                Student.name.like(
                    f"%{search}%"
                ),
                Project.project_title.like(
                    f"%{search}%"
                )
            )
        ).all()

    else:

        log_list = DailyLog.query.order_by(
            DailyLog.log_date.desc()
        ).all()

    return render_template(
        "daily_logs.html",
        logs=log_list,
        search=search
    )


@app.route(
    "/daily-logs/add",
    methods=["GET", "POST"]
)
def add_daily_log():

    if "user_id" not in session:
        return redirect(url_for("login"))

    students = Student.query.all()
    projects = Project.query.all()

    if request.method == "POST":

        student_id = request.form["student_id"]

        project_id = request.form["project_id"]

        log_date = request.form["log_date"]

        task = request.form["task"]

        hours_worked = request.form[
            "hours_worked"
        ]

        technology_used = request.form[
            "technology_used"
        ]

        status = request.form["status"]

        remarks = request.form["remarks"]

        daily_log = DailyLog(

            student_id=student_id,

            project_id=project_id,

            log_date=log_date,

            task=task,

            hours_worked=hours_worked,

            technology_used=technology_used,

            status=status,

            remarks=remarks

        )

        db.session.add(daily_log)

        db.session.commit()

        return redirect(
            url_for("daily_logs")
        )

    return render_template(
        "add_daily_log.html",
        students=students,
        projects=projects
    )

@app.route(
    "/daily-logs/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_daily_log(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    log = DailyLog.query.get_or_404(id)

    students = Student.query.all()
    projects = Project.query.all()

    if request.method == "POST":

        log.student_id = request.form[
            "student_id"
        ]

        log.project_id = request.form[
            "project_id"
        ]

        log.log_date = request.form[
            "log_date"
        ]

        log.task = request.form[
            "task"
        ]

        log.hours_worked = request.form[
            "hours_worked"
        ]

        log.technology_used = request.form[
            "technology_used"
        ]

        log.status = request.form[
            "status"
        ]

        log.remarks = request.form[
            "remarks"
        ]

        db.session.commit()

        return redirect(
            url_for("daily_logs")
        )

    return render_template(
        "edit_daily_log.html",
        log=log,
        students=students,
        projects=projects
    )

@app.route("/daily-logs/delete/<int:id>")
def delete_daily_log(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    log = DailyLog.query.get_or_404(id)

    db.session.delete(log)

    db.session.commit()

    return redirect(
        url_for("daily_logs")
    )



with app.app_context():

    db.create_all()


@app.route("/faculty-assignments", methods=["GET", "POST"])
def faculty_assignments():

    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":

        faculty_id = request.form.get("faculty_id", type=int)
        student_id = request.form.get("student_id", type=int)

        if not faculty_id or not student_id:
            flash("Please select both faculty and student.", "danger")
            return redirect(url_for("faculty_assignments"))

        faculty = db.session.get(Faculty, faculty_id)
        student = db.session.get(Student, student_id)

        if not faculty or not student:
            flash("Invalid faculty or student selection.", "danger")
            return redirect(url_for("faculty_assignments"))

        existing = FacultyStudent.query.filter_by(
            faculty_id=faculty_id,
            student_id=student_id
        ).first()

        if existing:
            flash("This student is already assigned to this faculty.", "warning")
            return redirect(url_for("faculty_assignments"))

        assignment = FacultyStudent(
            faculty_id=faculty_id,
            student_id=student_id
        )

        db.session.add(assignment)
        db.session.commit()

        flash("Student assigned to faculty successfully.", "success")
        return redirect(url_for("faculty_assignments"))

    faculties = Faculty.query.order_by(Faculty.name).all()
    students = Student.query.order_by(Student.name).all()

    assignments = FacultyStudent.query.order_by(
        FacultyStudent.assigned_at.desc()
    ).all()

    return render_template(
        "faculty_assignments.html",
        faculties=faculties,
        students=students,
        assignments=assignments
    )

@app.route("/faculty-my-students")
def faculty_my_students():

    if "user_id" not in session or session.get("role") != "faculty":
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("login"))

    faculty = Faculty.query.filter_by(user_id=user.id).first()

    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("login"))

    assignments = FacultyStudent.query.filter_by(
        faculty_id=faculty.id
    ).all()

    students = [
        assignment.student
        for assignment in assignments
    ]

    return render_template(
        "faculty_my_students.html",
        students=students
    )

@app.route(
    "/faculty-assignments/delete/<int:id>",
    methods=["POST"]
)
def delete_faculty_assignment(id):

    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    assignment = db.session.get(FacultyStudent, id)

    if not assignment:
        flash("Assignment not found.", "danger")
        return redirect(url_for("faculty_assignments"))

    db.session.delete(assignment)
    db.session.commit()

    flash("Faculty-student assignment removed successfully.", "success")

    return redirect(url_for("faculty_assignments"))


@app.route("/faculty-projects")
def faculty_projects():

    if "user_id" not in session or session.get("role") != "faculty":
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("login"))

    faculty = Faculty.query.filter_by(
        user_id=user.id
    ).first()

    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("login"))

    assignments = FacultyStudent.query.filter_by(
        faculty_id=faculty.id
    ).all()

    student_ids = [
        assignment.student_id
        for assignment in assignments
    ]

    if student_ids:
        projects = Project.query.filter(
            Project.student_id.in_(student_ids)
        ).order_by(
            Project.created_at.desc()
        ).all()
    else:
        projects = []

    return render_template(
        "faculty_projects.html",
        projects=projects
    )

@app.route("/faculty-reports")
def faculty_reports():
    if "user_id" not in session or session.get("role") != "faculty":
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("login"))

    faculty = Faculty.query.filter_by(user_id=user.id).first()

    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("faculty_dashboard"))

    assignments = FacultyStudent.query.filter_by(
        faculty_id=faculty.id
    ).all()

    student_ids = [assignment.student_id for assignment in assignments]

    projects = Project.query.filter(
        Project.student_id.in_(student_ids)
    ).order_by(Project.created_at.desc()).all() if student_ids else []

    return render_template(
        "faculty_reports.html",
        faculty=faculty,
        projects=projects
    )

@app.route(
    "/faculty-projects/evaluate/<int:id>",
    methods=["GET", "POST"]
)
def evaluate_project(id):

    if "user_id" not in session or session.get("role") != "faculty":
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("login"))

    faculty = Faculty.query.filter_by(
        user_id=user.id
    ).first()

    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("login"))

    project = Project.query.get_or_404(id)

    assignment = FacultyStudent.query.filter_by(
        faculty_id=faculty.id,
        student_id=project.student_id
    ).first()

    if not assignment:
        flash(
            "You are not authorized to evaluate this project.",
            "danger"
        )
        return redirect(url_for("faculty_projects"))

    if request.method == "POST":

        marks = request.form.get(
            "evaluation_marks",
            type=int
        )

        feedback = request.form.get(
            "faculty_feedback", ""
        ).strip()

        if marks is None or not 0 <= marks <= 100:
            flash(
                "Enter valid evaluation marks between 0 and 100.",
                "danger"
            )
            return render_template(
                "evaluate_project.html",
                project=project
            )

        project.evaluation_marks = marks
        project.faculty_feedback = feedback
        project.evaluated_at = datetime.now()

        db.session.commit()

        flash("Project evaluation saved successfully.", "success")
        return redirect(url_for("faculty_projects"))

    return render_template(
        "evaluate_project.html",
        project=project
    )


@app.route("/admin/project-report")
def admin_project_report():

    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    projects = Project.query.order_by(
        Project.created_at.desc()
    ).all()

    return render_template(
        "admin_project_report.html",
        projects=projects
    )
# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)