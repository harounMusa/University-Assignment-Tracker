from flask import Flask, request
from flask_restful import Resource, Api, abort, marshal_with, fields, reqparse
from models import CourseModel, db

app = Flask(__name__)
api = Api(app)

course_args = reqparse.RequestParser()
course_args.add_argument('name', type=str, required=True, help='please add a name for this course')
course_args.add_argument('semester', type=str, required=True, help='please add a semester for this course')

courseFields = {
    'id': fields.Integer,
    'name': fields.String,
    'semester': fields.String,
}

class Courses(Resource):
    @marshal_with(courseFields)
    def get(self):
        semester_filter = request.args.get('semester')
        if semester_filter:
            courses = CourseModel.query.filter_by(semester=semester_filter).all()
        else:
            courses = CourseModel.query.all()
        return courses, 200
    
    @marshal_with(courseFields)
    def post(self):
        args = course_args.parse_args()
        course = CourseModel(name=args['name'], semester=args['semester'])
        db.session.add(course)
        db.session.commit()
        return course, 201
    
class Course(Resource):
    @marshal_with(courseFields)
    def get(self, id):
        result = CourseModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message='Course not found')
        return result

    @marshal_with(courseFields)
    def put(self):
        result = CourseModel.query.filter_by(id=id).first()
        data = course_args.parse_args()

        if not result:
            abort(404, message='Course not found')
        
        if data['name']:
            result.name = data['name']

        if data['semester']:
            result.semester = data['semester']
        
        db.session.commit()

        return result, 200
            
    def delete(self, id):
        course = Course.query.get_or_404(id)
        db.session.delete(course)
        db.session.commit()
        return {'message': 'Course deleted'}, 204