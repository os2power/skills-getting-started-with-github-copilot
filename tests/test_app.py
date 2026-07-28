from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert unregister_response.status_code == 200

    data = unregister_response.json()
    assert "removed" in data["message"].lower()

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_activities_endpoint_disables_caching():
    response = client.get("/activities")
    assert response.status_code == 200
    assert "no-store" in response.headers.get("Cache-Control", "")
