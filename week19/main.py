def has_error(user_input):
    if len(user_input) != 9:
        return True
    permissions = ["r", "w", "x"]
    for i, char in enumerate(user_input):
        if char != permissions[i % 3] and char != "-":
            return True
    return False

def get_octal_value(user_input):
    octal_value = 0
    for i in range(0, len(user_input)):
        if user_input[i] == "r":
            octal_value += 4
        elif user_input[i] == "w":
            octal_value += 2
        elif user_input[i] == "x":
            octal_value += 1
        if (i + 1) % 3 == 0:
            octal_value *= 10
    octal_value /= 10
    return int(octal_value)

def main():
    user_input = input("Enter a permission: ")
    if has_error(user_input):
        print("Error: Invalid permission")
        return
    octal_value = get_octal_value(user_input)
    print("Octal value:", octal_value)

if __name__ == "__main__":
    main()
