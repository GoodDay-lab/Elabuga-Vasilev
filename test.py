import pytest
import requests
from data import db_session


url = "http://127.0.0.1:7000/api/jobs/{}"
url1 = "http://127.0.0.1:7000/api/users/{}"


def test_add_job():
    assert requests.post(url.format(''), json={'team_leader': 5,
                                               'job': 'there',
                                               'work_size': 4,
                                               'collaborators': '4, 2, 3, 5'}).json()['status'] == True


def test_delete_job():
    assert requests.delete(url.format("3")).json()['status'] == True


def test_delete_job_wrong():
    assert requests.delete(url.format("abc")).json()['status'] == False


def test_get_jobs():
    assert len(requests.get(url.format('')).json()['data']) > 2


def test_add_job1():
    assert requests.post(url.format(''), json={'team_leader': 'abc',
                                               'job': 'there',
                                               'work_size': 4,
                                               'collaborators': '4, 2, 3, 5'}).json()['status'] == True


def test_get_user():
    assert requests.get(url1.format('')).json()['status'] == 1


def test_add_user():
    assert requests.post(url1.format(''), json={
            'surname': 'add',
            'name': 'add1',
            'age': 10,
            'speciality': 'engineer',
            'email': 'kali@gm.com'
        }).json()['status'] == 1


def test_edit():
    value_new = 'kali'
    requests.put(url.format("1"), json={'team_leader': value_new})
    assert requests.get(url.format('1')).json()['data']['team_leader'] == value_new
    


def test_add_job2():
    assert requests.post(url.format('')).json()['status'] == False


def test_get_job():
    assert requests.get(url.format('1')).json()['status'] != False


def test_get_job1():
    assert requests.get(url.format('100')).json()['status'] == False


def test_get_job2():
    assert requests.get(url.format('abc')).json()['status'] == False
