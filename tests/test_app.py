from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seeded_data(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    chess_club = data["Chess Club"]
    assert chess_club["description"]
    assert chess_club["schedule"]
    assert isinstance(chess_club["max_participants"], int)
    assert "michael@mergington.edu" in chess_club["participants"]


def test_signup_for_activity_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{quote(activity)}/signup?email={quote(email)}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_unregister_from_activity_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{quote(activity)}/unregister?email={quote(email)}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
