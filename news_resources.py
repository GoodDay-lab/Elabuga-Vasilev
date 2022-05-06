from flask_restful import Api, reqparse, abort, Resource
from flask import Flask, jsonify
from data import db_session
from data.__all_models import *


def abort_if_user_not_found(job_id):
    s = db_session.create_session()
    new = s.query(User).filter(User.id == job_id).first()
    s.close()
    if not new:
        abort(404, message=f"User with id ({job_id}) not found.")


def abort_if_job_not_found(job_id):
    s = db_session.create_session()
    new = s.query(Jobs).filter(Jobs.id == job_id).first()
    s.close()
    if not new:
        abort(404, message=f"Job with id ({job_id}) not found.")


parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True, type=str)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True, type=str)
parser.add_argument('is_finished', required=True, type=bool)


uparser = reqparse.RequestParser()
uparser.add_argument('surname', required=True, type=str)
uparser.add_argument('name', required=True, type=str)
uparser.add_argument('age', required=True, type=int)
uparser.add_argument('email', required=True, type=str)


class UsersResource(Resource):
    def get(self, job_id):
        abort_if_user_not_found(job_id)
        s = db_session.create_session()
        job = s.query(User).get(job_id)
        s.close()
        return jsonify({
            'user': {key: job.__dict__[key] 
                    for key in job.__dict__.keys()
                    if not key.startswith('_')}
        })
    
    def delete(self, job_id):
        abort_if_user_not_found(job_id)
        s = db_session.create_session()
        s.query(User).filter(User.id == job_id).delete()
        s.commit()
        s.close()
        return jsonify({
            'status': True
        })


class UsersListResource(Resource):
    def get(self):
        s = db_session.create_session()
        jobs = s.query(User).all()
        s.close()
        return jsonify({
            'users': [{key: job.__dict__[key] 
                    for key in job.__dict__.keys()
                    if not key.startswith('_')}
                    for job in jobs]
        })
    
    def post(self):
        args = uparser.parse_args()
        s = db_session.create_session()
        job = User(
            surname = args['surname'],
            name = args['name'],
            age = args['age'],
            email = args['email'],
        )
        s.add(job)
        s.commit()
        s.close()
        return jsonify({
            'status': True
        })


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        s = db_session.create_session()
        job = s.query(Jobs).get(job_id)
        s.close()
        return jsonify({
            'job': {key: job.__dict__[key] 
                    for key in job.__dict__.keys()
                    if not key.startswith('_')}
        })
    
    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        print("[!]")
        s = db_session.create_session()
        s.query(Jobs).filter(Jobs.id == job_id).delete()
        s.commit()
        s.close()
        return jsonify({
            'status': True
        })


class JobsListResource(Resource):
    def get(self):
        s = db_session.create_session()
        jobs = s.query(Jobs).all()
        s.close()
        return jsonify({
            'jobs': [{key: job.__dict__[key] 
                    for key in job.__dict__.keys()
                    if not key.startswith('_')}
                    for job in jobs]
        })
    
    def post(self):
        args = parser.parse_args()
        s = db_session.create_session()
        job = Jobs(
            team_leader = args['team_leader'],
            job = args['job'],
            work_size = args['work_size'],
            collaborators = args['collaborators'],
            is_finished = args['is_finished']
        )
        s.add(job)
        s.commit()
        s.close()
        return jsonify({
            'status': True
        })
        
    
db_session.global_init("/db/blogs.sqlite")
app = Flask(__name__)
api = Api(app)
api.add_resource(UsersResource, '/api/v2/users/<int:job_id>')
api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')
api.add_resource(JobsListResource, '/api/v2/jobs')
app.run(port=8080)


