import hashlib
import os
import time
from change_password import ChangePassword  # Import ChangePassword class


class LoginSystem:
    def __init__(self, user_data_file):
        self.user_data_file = os.path.join("Database_txt", user_data_file)
        self.max_failed_attempts = 4  # Configurable maximum attempts
        self.initial_delay_time = 30  # Configurable initial delay in seconds
        self.change_password_handler = ChangePassword(user_data_file)  # Instantiate ChangePassword class

    def hash_password(self, password, salt):
        """Hashes the password using SHA256."""
        return hashlib.sha256(salt + password.encode()).hexdigest()

    def find_user(self, email_or_phone):
        """Find user details in the database."""
        with open(self.user_data_file, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 4 and data[0] == email_or_phone:
                    return data
        return None

    def update_user_data(self, email_or_phone, new_data):
        """Updates user data for a given email or phone."""
        updated_lines = []
        with open(self.user_data_file, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 4 and data[0] == email_or_phone:
                    updated_lines.append(new_data + "\n")
                else:
                    updated_lines.append(line)
        with open(self.user_data_file, "w") as file:
            file.writelines(updated_lines)

    def change_password(self, email_or_phone):
        """Allows the user to change their password by delegating to the ChangePassword class."""
        print("\033[1;36m--- Change Password ---\033[0m")
        self.change_password_handler.change_password(email_or_phone)

    def user_menu(self, email_or_phone):
        """Displays the menu for logged-in users."""
        while True:
            print("=" * 30)
            print("\n\033[1;36m--- User Menu ---\033[0m")
            print("=" * 30)
            print("\033[1;33m1. Change Password\033[0m")
            print("\033[1;33m2. Logout\033[0m")
            print("=" * 30)
            choice = input("\033[1;34mEnter your choice: \033[0m").strip()

            if choice == "1":
                self.change_password(email_or_phone)
            elif choice == "2":
                print("\033[1;32mLogging out...\033[0m")
                break
            else:
                print("\033[1;31mInvalid choice. Please try again.\033[0m")

    def user_login(self):
        """Handles the user login with delays triggered after every failed attempt."""
        failed_attempts = 0
        delay_time = self.initial_delay_time
        email_or_phone = ""

        while True:
            if failed_attempts >= self.max_failed_attempts:
                print(f"\033[1;31mToo many failed attempts. Please wait {delay_time} seconds before trying again.\033[0m")
                time.sleep(delay_time)
                delay_time *= 3  # Exponential backoff
                failed_attempts = 0

            email_or_phone = input("\033[1;34mEnter your email or phone number: \033[0m").strip()
            user_data = self.find_user(email_or_phone)

            if not user_data:
                print("\033[1;31mNo account found with that email or phone number. Please try again.\033[0m")
                failed_attempts += 1
                continue

            password = input("\033[1;34mEnter your password: \033[0m").strip()
            salt_hex = user_data[2]
            stored_hashed_password = user_data[3]
            salt = bytes.fromhex(salt_hex)

            if self.hash_password(password, salt) == stored_hashed_password:
                print("\033[1;32mLogin successful!\033[0m")
                self.user_menu(email_or_phone)
                return
            else:
                print("\033[1;31mIncorrect password. Please try again.\033[0m")
                failed_attempts += 1
