import hashlib
import secrets
import json

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

def create_otp():
    """Generates a mixed-letter-and-digit OTP.
    Returns:
        str: The OTP.
    """
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    otp = ""
    for i in range(6):
        otp += secrets.choice(chars)
    return otp

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
    if new_hashed_pwd != hashed_pwd:
        return "Login failed. Incorrect password."
    otp = create_otp()
    print(f"OTP sent to user: {otp}")
    entered_otp = input("Enter the OTP received via SMS: ")
    if entered_otp == otp:
        return f"Login successful. Welcome, {username}!"
    return "Login failed. Incorrect OTP."


def main():
    database_filename = "user_database.json"
    user_database = db_init(database_filename)
    username_register = input("Enter a username for registration: ")
    password_register = input("Enter a password for registration: ")
    profile_info_register = input("Enter profile info: ")
    for user_data in user_database:
        if user_data["username"] == username_register:
            print("Username already taken.")
            return
    result_register = user_register(username_register, password_register, profile_info_register, user_database, database_filename)
    print(result_register)
    username_login_correct = input("Enter username for login: ")
    password_login_correct = input("Enter password for login: ")
    result_login_correct = login_user(username_login_correct, password_login_correct, user_database)
    print(result_login_correct)
    db_save(database_filename, user_database)

if __name__ == "__main__":
    main()
