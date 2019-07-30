from model import H2JUser

def seed_data():
    test_key = H2JUser(username="testuser", password="passuser", learning_style="",
        email="", first_name="", last_name="").put()
