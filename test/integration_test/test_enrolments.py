from .conftest import fake_data5

def test_create_enrol(test_client, enrol_create):
    enrolment, *_ = enrol_create

    assert enrolment.status_code == 201
    assert enrolment.json()['data']['course_title'] == fake_data5['course_title']

def test_get_enrolments(test_client, enrol_create):
    _, admin, instructor, student = enrol_create
    response = test_client.get(
        '/courses/Ajifowoke Samson/enrolments/',
        headers={
            'Authorization': instructor.json()['data']['token']
        }
    )

    assert response.status_code == 200
    assert response.json()['data'][0]['course_instructor'] == 'Ajifowoke Samson'

def test_get_student_enrolments(test_client, enrol_create):
    *_, student = enrol_create
    response = test_client.get(
        '/courses/enrolments/gasmine rabbit/',
        headers={
            'Authorization': student.json()['data']['token']
        }
    )

    assert response.status_code == 200
    assert response.json()['data'][0]['student'] == 'gasmine rabbit'

def test_delete_enrolment(test_client, enrol_create):
    *_, student = enrol_create
    test_client.delete(
        '/courses/enrolments/1/',
        headers={
            'Authorization': student.json()['data']['token']
        }
    )

    response = test_client.get(
        '/courses/enrolments/gasmine rabbit/',
        headers={
            'Authorization': student.json()['data']['token']
        }
    )

    assert response.status_code == 404
