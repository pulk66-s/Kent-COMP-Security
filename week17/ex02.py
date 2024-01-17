import json

def register_user(username, password_file):
    """Register a new user in the database.
    Parameters:
        username (str): The username of the new user.
        password_file (str): The filename of the password file.
    Returns:
        bool: True if the user was registered, False if the user already exists.
    """
    with open('user_db.json', 'r') as file:
        for line in file:
            data = json.loads(line)
            if data["username"] == username:
                return False
    data = {
        "username": username,
        "password_file": password_file
    }
    with open('user_db.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')
    return True

def login_user(username, password_file):
    """Login a user.
    Parameters:
        username (str): The username of the user.
        password_file (str): The filename of the password file.
    Returns:
        bool: True if the user was logged in, False if the user does not exist.
    """
    with open('user_db.json', 'r') as file:
        for line in file:
            data = json.loads(line)
            if data["username"] == username and data["password_file"] == password_file:
                return True
        return False

def main():
    name = "Hugo"
    password_file = "password.txt"
    if not register_user(name, password_file):
        print("Username already exists")
        return
    if not login_user(name, password_file):
        print("Login failed")
        return
    print("Login successful")

if __name__ == "__main__":
    main()
