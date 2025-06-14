import app

def test_index():
    tester = app.app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
