import hashlib
import secrets
import json
from json.decoder import JSONDecodeError

def db_init(filename):
    """Initializes the database from a JSON file.
    If the file does not exist, it returns an empty list.
    Parameters:
        filename (str): The name of the JSON file.
    Returns:
        list: The list of users.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        return []

def db_save(filename, user_db):
    """Saves the database to a JSON file.
    Parameters:
        filename (str): The name of the JSON file.
        user_db (list): The list of users.
    """
    with open(filename, 'w') as file:
        json.dump(user_db, file, indent=4)

def user_register(username, pwd, profile_info, db, filename):
    """Registers a user.
    Parameters:
        username (str): The username.
        pwd (str): The password.
        profile_info (str): The profile info.
        db (list): The list of users.
        filename (str): The name of the JSON file.
    Returns:
        str: The registration status.
    """
    salt = secrets.token_hex(16)
    salted_pwd = pwd + salt
    hashed_password = hashlib.sha256(salted_pwd.encode('utf-8')).hexdigest()
    data = {
        'username': username,
        'salt': salt,
        'hashed_password': hashed_password,
        'profile_info': profile_info
    }
    db.append(data)
    db_save(filename, db)
    return f"User {username} registered successfully."

def get_user(username, user_db):
    """Gets a user from the database.
    Parameters:
        username (str): The username.
        user_db (list): The list of users.
    Returns:
        dict: The user data.
    """
    for user_data in user_db:
        if user_data['username'] == username:
            return user_data
    return None

def login_user(username, password, user_db):
    """Logs in a user.
    Parameters:
        username (str): The username.
        password (str): The password.
        user_db (list): The list of users.
    Returns:
        str: The login status.
    """
    user = get_user(username, user_db)
    if user is None:
        return "Login failed. User not found."
    salt = user['salt']
    hashed_pwd = user['hashed_password']
    salted_pwd = password + salt
    new_hashed_pwd = hashlib.sha256(salted_pwd.encode('utf-8')).hexdigest()
    if new_hashed_pwd == hashed_pwd:
        return f"Login successful. Welcome, {username}!"
    return "Login failed. Incorrect password."

def main():
    db_name = 'user_db.json'
    user_db = db_init(db_name)
    user = input("Enter a username for registration: ")
    pwd = input("Enter a password for registration: ")
    info = input("Enter profile info: ")
    for user_data in user_db:
        if user_data['username'] == user:
            print("Username already taken.")
            return
    res = user_register(user, pwd, info, user_db, db_name)
    print(res)
    login_name = input("Enter username for login: ")
    login_pwd = input("Enter password for login: ")
    login_res = login_user(login_name, login_pwd, user_db)
    print(login_res)
    db_save(db_name, user_db)

if __name__ == '__main__':
    main()
