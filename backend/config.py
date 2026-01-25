import os
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:ap1122@localhost/university_tracker'
SQLALCHEMY_DATABASE_URI = 'sqlite:///./university_tracker.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY')