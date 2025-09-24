from .conftest import fake_data3

def test_create_course(test_client, course_create):
    course, *_ = course_create

    assert course.status_code == 201
    assert course.json()['data']['title'] == fake_data3['title']

def test_get_courses(test_client, course_create):
    _, instructor, *_ = course_create
    response = test_client.get(
        '/courses/',
        headers={
            'Authorization': instructor.json()['data']['token']
        }
    )

    assert response.status_code == 200
    assert len(response.json()['data']) >= 1

def test_get_course(test_client, course_create):
    _, instructor, *_ = course_create
    response = test_client.get(
        '/courses/Computer Science/',
        headers={
            'Authorization': instructor.json()['data']['token']
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['title'] == fake_data3['title']

def test_update_course(test_client, course_create):
    _, admin, instructor, student = course_create
    title = 'Biochemistry'

    response = test_client.patch(
        '/courses/1/',
        json={
            'title': title
        },
        headers={
            'Authorization': instructor.json()['data']['token']
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['title'] == title

def test_delete_course(test_client, course_create):
    course, instructor, *_ = course_create
    test_client.delete(
        '/courses/1/',
        headers={
            'Authorization': instructor.json()['data']['token']
        }
    )

    response = test_client.get(
        '/courses/',
        headers={
            'Authorization': instructor.json()['data']['token']
        }
    )

    assert course not in response.json()['data']
