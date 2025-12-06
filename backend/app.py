from flask import Flask
from flask_restful import Api
from models import db
import config
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.course_route import Courses
from routes.course_route import Course
from routes.assignments_route import Assignments, Assignment
from routes.auth_routes import Register, Login

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
CORS(app)
app.config.from_object(config)
api = Api(app)
db.init_app(app)
jwt = JWTManager(app)

# Register API endpoints
api.add_resource(Courses, '/courses')
api.add_resource(Course, '/course/<int:id>')
api.add_resource(Assignments, '/assignments')
api.add_resource(Assignment, '/assignments/<int:id>')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

