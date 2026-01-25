from flask import Flask
from flask_restful import Api
from models import db
import config
from flask_cors import CORS
from routes.course_route import Courses
from routes.course_route import Course
from routes.assignments_route import Assignments, Assignment
from routes.auth_routes import AdminLogin, AdminCheck, AdminLogout

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://assignments-tracker.onrender.com"}}, supports_credentials=True)
# Session Cookie Security for local development
app.config.update(
    SESSION_COOKIE_SAMESITE= None, # Set to 'None' if using HTTPS and different domains
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,   # Set to True only if using HTTPS
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

