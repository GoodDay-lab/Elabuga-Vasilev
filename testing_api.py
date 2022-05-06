import pytest
import requests


url_user = "http://127.0.0.1:8080/api/v2/users/{}"
url_users = "http://127.0.0.1:8080/api/v2/users"
url_job = "http://127.0.0.1:8080/api/v2/jobs/{}"
url_jobs = "http://127.0.0.1:8080/api/v2/jobs"


def test_create_user():
    response = requests.post(url_users,json={
        'surname': "обычный",
        'name': 'Инженер',
        'age': 23,
        'email': 'abc214@gm.com',
    }).json()
    assert response['status'] == 1


def test_get_users():
    response = requests.get(url_users).json()
    assert len(response['users']) > 0


def test_get_user():
    response = requests.get(url_users).json()
    id_ = response['users'][0]['id']
    response2 = requests.get(url_user.format(id_)).json()
    assert 'user' in response2


def test_delete_corr():
    response = requests.get(url_users).json()
    length = len(response['users'])
    id_ = response['users'][0]['id']
    requests.delete(url_user.format(id_)).json()
    new_length = len(requests.get(url_users).json()['users'])
    assert length - new_length == 1


def test_create_job():
    response = requests.post(url_jobs,json={
        'team_leader': 10,
        'job': 'Инженер',
        'work_size': 24,
        'collaborators': '23, 24',
        'is_finished': False
    }).json()
    print(response)
    assert response['status'] == 1


def test_get_jobs():
    response = requests.get(url_jobs).json()
    assert len(response['jobs']) > 0


def test_get_job():
    response = requests.get(url_jobs).json()
    id_ = response['jobs'][0]['id']
    response2 = requests.get(url_job.format(id_)).json()
    assert 'job' in response2


def test_delete_corr_j():
    response = requests.get(url_jobs).json()
    length = len(response['jobs'])
    id_ = response['jobs'][0]['id']
    requests.delete(url_job.format(id_)).json()
    new_length = len(requests.get(url_jobs).json()['jobs'])
    assert length - new_length == 1
    
