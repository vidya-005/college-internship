import os

class Config:
    SECRET_KEY = "change-this-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:root@localhost/internship"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False