from model import User

def seed_data():
    test_key = User(username="testuser", password="passuser", learning_style="").put()
