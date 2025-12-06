from flask import Flask
from flask_restful import Resource, Api, marshal_with, fields, reqparse
from models import AssignmentModel, db
from datetime import datetime

app = Flask(__name__)
api = Api(app)

def parse_datetime(value):
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise ValueError("Date must be in ISO format: YYYY-MM-DDTHH:MM:SS")
    
assignment_args = reqparse.RequestParser()
assignment_args.add_argument('course_id', type=int, required=True, help='Course ID is required.')
assignment_args.add_argument('title', type=str, required=True, help='Title is required.')
assignment_args.add_argument('description', type=str, help='Add a Description is an optional', default='NO Desctiption provided')
assignment_args.add_argument('start_date', type=parse_datetime, required=True, help='Start date must be in ISO format.')
assignment_args.add_argument('due_date', type=parse_datetime, required=True, help='Due date must be in ISO format.')
# assignment_args.add_argument('status', type=str, default='Pending')

put_parser = reqparse.RequestParser()
put_parser.add_argument('title', type=str)
put_parser.add_argument('description', type=str)
put_parser.add_argument('start_date', type=parse_datetime) # Will still return a datetime obj if present
put_parser.add_argument('due_date', type=parse_datetime)

assignmentFields = {
    'id': fields.Integer,
    'course_id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'start_date': fields.String,
    'due_date': fields.String,
    # 'status': fields.String
}

class Assignments(Resource):
    @marshal_with(assignmentFields)
    def get(self):
        assignments = AssignmentModel.query.all()
        return assignments, 200
    
    @marshal_with(assignmentFields)
    def post(self):
        args = assignment_args.parse_args()
        assignment = AssignmentModel(
            course_id=args['course_id'],
            title=args['title'],
            description=args['description'],
            start_date=args['start_date'],
            due_date=args['due_date'],
            # status=args.get('status', 'Pending')
        )
        db.session.add(assignment)
        db.session.commit()
        return assignment, 201

class Assignment(Resource):
    @marshal_with(assignmentFields)
    def put(self, id):
        assignment = AssignmentModel.query.get_or_404(id)

        data = put_parser.parse_args()

        if data['title']:
            assignment.title = data.get('title', assignment.title)
        if data['description']:
            assignment.description = data.get('description', assignment.description)
        if data['start_date']:
            assignment.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        if data['due_date']:
            assignment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        # assignment.status = data.get('status', assignment.status)

        db.session.commit()

        return {'message': 'Assignment updated'}, 200

    def delete(self, id):
        assignment = Assignment.query.get_or_404(id)
        db.session.delete(assignment)
        db.session.commit()
        return {'message': 'Assignment deleted'}, 204