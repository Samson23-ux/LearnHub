from app.main import app
from pathlib import Path
import json
import pytest, asyncio
from fastapi.testclient import TestClient

path = Path('app')

fake_data = {
    'username': 'jojojojo',
    'email': 'jojo@email.com',
    'password': 'jojojojo123',
    'role': 'Admin'
}

fake_data1 = {
    'username': 'gasmine jojo',
    'email': 'jojo123@email.com',
    'password': 'thailand345t',
    'role': 'Instructor'
}

fake_data2 = {
    'username': 'gasmine rabbit',
    'email': 'jojo6123@email.com',
    'password': 'thailand345t',
    'role': 'Student'
}

fake_data3 = {
    'title': 'Computer Science',
    'instructor': 'Ajifowoke Samson',
    'duration': 4
}

fake_data4 = {
    'title': 'Medicine and Surgery',
    'instructor': 'Ajifowoke Samson',
    'duration': 6
}

fake_data5 = {
    'course_title': 'Computer Science',
    'course_instructor': 'Ajifowoke Samson',
    'student': 'gasmine rabbit'
}

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def account_create(test_client):
    response = test_client.post(
        '/auth/sign-up/',
        json=fake_data
    )

    test_client.post(
        '/auth/sign-up/',
        json=fake_data1
    )

    test_client.post(
        '/auth/sign-up/',
        json=fake_data2
    )
    return response

@pytest.fixture
def account_sign_in(test_client, account_create):
    response = test_client.post(
        '/auth/sign-in/1/',
        json={
            'email': fake_data['email'],
            'password': fake_data['password']
        }
    )

    response1 = test_client.post(
        '/auth/sign-in/2/',
        json={
            'email': fake_data1['email'],
            'password': fake_data1['password']
        }
    )

    response2 = test_client.post(
        '/auth/sign-in/3/',
        json={
            'email': fake_data2['email'],
            'password': fake_data2['password']
        }
    )
    return response, response1, response2

@pytest.fixture
def course_create(test_client, account_sign_in):
    admin, instructor, student = account_sign_in
    response = test_client.post(
        '/courses/',
        headers={
            'Authorization': instructor.json()['data']['token']
        },
        json=fake_data3
    )

    test_client.post(
        '/courses/',
        headers={
            'Authorization': instructor.json()['data']['token']
        },
        json=fake_data4
    )

    return response, admin, instructor, student

@pytest.fixture
def enrol_create(test_client, course_create):
    response, admin, instructor, student = course_create
    response = test_client.post(
        '/courses/enrolments/',
        json=fake_data5,
        headers={
            'Authorization': student.json()['data']['token']
        }
    )

    return response, admin, instructor, student

@pytest.fixture(autouse=True)
def reset_files():
    (path/'data\\users.json').write_text(json.dumps([]))
    (path/'data\\courses.json').write_text(json.dumps([]))
    (path/'data\\enrolments.json').write_text(json.dumps([]))
    yield
    (path/'data\\users.json').write_text(json.dumps([]))
    (path/'data\\courses.json').write_text(json.dumps([]))
    (path/'data\\enrolments.json').write_text(json.dumps([]))
