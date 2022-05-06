import flask as fl
from data import db_session
from data.__all_models import *


blueprint = fl.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route("/api/jobs/", methods=["POST", "GET"])
def get_jobs():
    if fl.request.method == "GET":
        s = db_session.create_session()
        all_jobs = s.query(Jobs).all()
        s.close()
        return fl.jsonify(
            {'data': [{key: data.__dict__[key] for key in data.__dict__.keys() if key != '_sa_instance_state'} for data in all_jobs]}
        )
    else:
        if not fl.request.json:
            return fl.jsonify(
                {
                    'status': 0,
                    'comment': "Your forgot to give a json"
                }
            )
        if not all(key for key in fl.request.json.keys() 
                if key in ['team_leader', 'job', 'work_size', 'collaborators']):
            return fl.jsonify({
                    'status': 0,
                    'comment': "Your forgot to give a neccesseary args"
                })
        if 'id' in fl.request.json.keys():
            return fl.jsonify(
                {
                    'status': 0,
                    'comment': "Bad args"
                }
            )
        s = db_session.create_session()
        job = Jobs(**fl.request.json)
        s.add(job)
        s.commit()
        return fl.jsonify(
            {
                'status': 1,
            }
        )


@blueprint.route("/api/jobs/<job_id>", methods=["GET", "DELETE", "PUT"])
def get_job(job_id):
    if fl.request.method == "GET":
        for char in job_id:
            if not ('0' <= char <= '9'): return fl.jsonify(
                {'status': 0, 'comment': f"Bad id ({job_id})"}
            )
        job_id = int(job_id)
        s = db_session.create_session()
        job = s.query(Jobs).filter(Jobs.id == job_id).first()
        s.close()
        if job == None:
            return fl.jsonify(
                {'status': 0, 'comment': f"There's no job with id = {job_id}"}
            )
        return fl.jsonify(
            {'status': 1, 'data': {key: job.__dict__[key] for key in job.__dict__.keys() if key != '_sa_instance_state'}}
        )
    elif fl.request.method == "DELETE":
        for char in job_id:
            if not ("0" <= char <= "9"): return fl.jsonify(
                {'status': 0, 'comment': f'Bad id ({job_id})'}
            )
        job_id = int(job_id)
        s = db_session.create_session()
        job = s.query(Jobs).filter(Jobs.id == job_id).delete()
        s.commit()
        s.close()
        return fl.jsonify(
            {'status': 1, 'comment': 'Job has been deleted'}
        )
    elif fl.request.method == "PUT":
        if not fl.request.json:
            return fl.jsonify(
                {
                    'status': 0,
                    'comment': "Your forgot to give a json"
                }
            )
        if 'id' in fl.request.json.keys():
            return fl.jsonify(
                {
                    'status': 0,
                    'comment': "Bad args"
                }
            )
        for char in job_id:
            if not ("0" <= char <= "9"): return fl.jsonify(
                {'status': 0, 'comment': f'Bad id ({job_id})'}
            )
        job_id = int(job_id)
        s = db_session.create_session()
        job = s.query(Jobs).filter(Jobs.id == job_id).first()
        for key in fl.request.json.keys():
            if hasattr(job, key):
                setattr(job, key, fl.request.json[key])
        s.add(job)
        s.commit()
        return fl.jsonify(
            {
                'status': 1,
            }
        )


@blueprint.route("/api/users/", methods=["POST", "GET"])
def get_users():
    if fl.request.method == "GET":
        s = db_session.create_session()
        all_jobs = s.query(User).all()
        s.close()
        return fl.jsonify(
            {
                'status': 1,
                'data': [{key: data.__dict__[key] for key in data.__dict__.keys() if key != '_sa_instance_state'} for data in all_jobs]
            }
        )
    elif fl.request.method == "POST":
        if not fl.request.json:
            return fl.jsonify(
                {
                    'status': 0,
                    'comment': "Your forgot to give a json"
                }
            )
        if not all(key for key in fl.request.json.keys() 
                if key in ['name', 'surname',
                           'age', 'email', 'speciality']):
            return fl.jsonify({
                    'status': 0,
                    'comment': "Your forgot to give a neccesseary args"
                })
        s = db_session.create_session()
        job = Jobs()
        for key in fl.request.json.keys():
            if hasattr(job, key) and key != 'id':
                setattr(job, key, fl.request.json.get(key))
        s.add(job)
        s.commit()
        return fl.jsonify(
            {
                'status': 1
            }
        )


@blueprint.route("/api/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def get_user(user_id):
    for char in user_id:
        if not ('0' <= char <= '9'): return fl.jsonify(
            {'status': 0, 'comment': f"Bad id ({user_id})"}
        )
    user_id = int(user_id)
    if fl.request.method == "GET":
        s = db_session.create_session()
        job = s.query(User).filter(User.id == user_id).first()
        s.close()
        if job == None:
            return fl.jsonify(
                {'status': 0, 'comment': f"There's no job with id = {user_id}"}
            )
        return fl.jsonify(
            {'status': 1, 'data': {key: job.__dict__[key] for key in job.__dict__.keys() if key != '_sa_instance_state'}}
        )
    elif fl.request.method == "DELETE":
        s = db_session.create_session()
        job = s.query(User).filter(User.id == user_id).delete()
        s.commit()
        s.close()
        return fl.jsonify(
            {'status': 1, 'comment': 'Job has been deleted'}
        )
    elif fl.request.method == "PUT":
        if not fl.request.json:
            return fl.jsonify(
                {
                    'status': 0,
                    'comment': "Your forgot to give a json"
                }
            )
        s = db_session.create_session()
        job = s.query(User).filter(User.id == user_id).first()
        for key in fl.request.json.keys():
            if hasattr(job, key) and key != 'id':
                setattr(job, key, fl.request.json[key])
        s.add(job)
        s.commit()
        return fl.jsonify(
            {
                'status': 1,
            }
        )

