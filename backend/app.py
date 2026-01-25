from flask import Flask
from flask_restful import Api
from models import db
import config
from flask_cors import CORS
import os
from routes.course_route import Courses
from routes.course_route import Course
from routes.assignments_route import Assignments, Assignment
from routes.auth_routes import AdminLogin, AdminCheck, AdminLogout

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://assignments-tracker.onrender.com",
            "http://127.0.0.1:5500", # VS Code Live Server
            "http://localhost:5500"
        ]
    }
}, supports_credentials=True)
# Detect if we are running on Render
IS_PRODUCTION = os.getenv('RENDER') is not None

app.config.update(
    SESSION_COOKIE_SAMESITE='None', 
    SESSION_COOKIE_HTTPONLY=True,
    # Only force Secure if we are in production (HTTPS)
    SESSION_COOKIE_SECURE=IS_PRODUCTION,
)
app.config.from_object(config)
api = Api(app)
db.init_app(app)

# Register API endpoints
api.add_resource(Courses, '/courses')
api.add_resource(Course, '/course/<int:id>')
api.add_resource(Assignments, '/assignments')
api.add_resource(Assignment, '/assignments/<int:id>')
api.add_resource(AdminLogin, '/admin/login')
api.add_resource(AdminCheck, '/admin/check')
api.add_resource(AdminLogout, '/admin/logout')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)

