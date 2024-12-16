# import hashlib
# import os
# import random
# import string
# import time


# class UserSystem:
#     def __init__(self, user_data_file, backup_code_file):
#         self.user_data_file = os.path.join("Database_txt", user_data_file)
#         self.backup_code_file = os.path.join("Database_txt", backup_code_file)

#         # Ensure the Database_txt folder exists
#         if not os.path.exists("Database_txt"):
#             os.makedirs("Database_txt")

#     def hash_password(self, password, salt):
#         """Hashes the password using SHA256."""
#         return hashlib.sha256(salt + password.encode()).hexdigest()

#     def generate_backup_code(self, count=1):
#         """Generates multiple 8-digit unique backup codes."""
#         backup_codes = set()
#         while len(backup_codes) < count:
#             backup_codes.add(''.join(random.choices(string.digits, k=8)))
#         return list(backup_codes)

#     def validate_email(self, email):
#         """Validates if the email ends with '@gmail.com'."""
#         return email.endswith("@gmail.com")

#     def validate_phone(self, phone):
#         """Validates if the phone starts with '0' and contains 9-10 digits."""
#         return phone.startswith("0") and phone[1:].isdigit() and 9 <= len(phone) <= 10

#     def validate_password(self, password):
#         """Validates if the password meets complexity requirements."""
#         has_upper = any(char.isupper() for char in password)
#         has_lower = any(char.islower() for char in password)
#         has_special = any(char in string.punctuation for char in password)
#         return len(password) >= 8 and has_upper and has_lower and has_special

#     def show_error(self, message):
#         """Displays errors in a consistent format."""
#         print(f"\033[1;31m[Error] {message}\033[0m")

#     def show_success(self, message):
#         """Displays success messages in a consistent format."""
#         print(f"\033[1;32m[Success] {message}\033[0m")

#     def show_step(self, step_number, message):
#         """Displays steps in a consistent format."""
#         print(f"\033[1;34m[Step {step_number}] {message}\033[0m")

#     def register_user(self):
#         """Registers a new user with retry limits and delay enforcement."""
#         max_attempts = 3  # Maximum attempts for each step
#         delay_time = 30  # Delay in seconds after exceeding attempts

#         # Step 1: Get a unique email or phone number
#         self.show_step(1, "Enter your email or phone number.")
#         failed_attempts = 0
#         while failed_attempts < max_attempts:
#             email_or_phone = input("Enter your email or phone number: ").strip()

#             # Check if the email/phone already exists
#             if os.path.exists(self.user_data_file):
#                 with open(self.user_data_file, "r") as file:
#                     existing_users = file.readlines()
#                     if any(email_or_phone in user.split(",") for user in existing_users):
#                         self.show_error("This email or phone number is already registered.")
#                         failed_attempts += 1
#                         if failed_attempts >= max_attempts:
#                             self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
#                             time.sleep(delay_time)
#                             return
#                         continue

#             if "@" in email_or_phone:
#                 if not self.validate_email(email_or_phone):
#                     self.show_error("Invalid email format. Use a valid Gmail address (e.g., example@gmail.com).")
#                     failed_attempts += 1
#                 else:
#                     break
#             else:
#                 if not self.validate_phone(email_or_phone):
#                     self.show_error("Invalid phone number. Ensure it starts with '0' and is 9-10 digits long.")
#                     failed_attempts += 1
#                 else:
#                     break

#         # Step 2: Get a unique username
#         self.show_step(2, "Enter a unique username.")
#         failed_attempts = 0
#         while failed_attempts < max_attempts:
#             username = input("Enter your username: ").strip()

#             # Check if the username already exists
#             if os.path.exists(self.user_data_file):
#                 with open(self.user_data_file, "r") as file:
#                     existing_users = file.readlines()
#                     if any(username in user.split(",") for user in existing_users):
#                         self.show_error("This username is already taken. Please choose a different one.")
#                         failed_attempts += 1
#                         if failed_attempts >= max_attempts:
#                             self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
#                             time.sleep(delay_time)
#                             return
#                         continue

#             if not username:
#                 self.show_error("Username cannot be empty.")
#                 failed_attempts += 1
#             elif username == email_or_phone:
#                 self.show_error("Username and email/phone number cannot be the same.")
#                 failed_attempts += 1
#             else:
#                 break

#         # Step 3: Get and confirm password
#         self.show_step(3, "Enter and confirm your password.")
#         failed_attempts = 0
#         while failed_attempts < max_attempts:
#             password = input("Enter your password: ").strip()

#             if not self.validate_password(password):
#                 self.show_error("Password must be at least 8 characters long and include uppercase, lowercase, and special characters.")
#                 failed_attempts += 1
#                 if failed_attempts >= max_attempts:
#                     self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
#                     time.sleep(delay_time)
#                     return
#                 continue

#             confirm_password = input("Confirm your password: ").strip()
#             if password != confirm_password:
#                 self.show_error("Passwords do not match.")
#                 failed_attempts += 1
#             else:
#                 break

#         # Step 4: Save user and generate backup codes
#         salt = os.urandom(16)
#         hashed_password = self.hash_password(password, salt)
#         backup_codes = self.generate_backup_code(10)  # Generate 10 backup codes

#         # Save the user data
#         with open(self.user_data_file, "a") as file:
#             file.write(f"{email_or_phone},{username},{salt.hex()},{hashed_password}\n")

#         # Save backup codes
#         with open(self.backup_code_file, "a") as file:
#             for code in backup_codes:
#                 file.write(f"{email_or_phone},{code}\n")

#         # Show success messages
#         self.show_success(f"User '{username}' registered successfully!")
#         print("\nHere are your backup codes:")
#         for code in backup_codes:
#             print(f"\033[1;33m{code}\033[0m")
#         print("\n\033[1;31mPlease save these backup codes in a secure location.\033[0m")
# import hashlib
# import os
# import random
# import string
# import time


# class UserSystem:
#     def __init__(self, user_data_file, backup_code_file):
#         self.user_data_file = os.path.join("Database_txt", user_data_file)
#         self.backup_code_file = os.path.join("Database_txt", backup_code_file)

#         # Ensure the Database_txt folder exists
#         if not os.path.exists("Database_txt"):
#             os.makedirs("Database_txt")

#     def hash_password(self, password, salt):
#         """Hashes the password using SHA256."""
#         return hashlib.sha256(salt + password.encode()).hexdigest()

#     def generate_backup_code(self, count=1):
#         """Generates multiple 8-digit unique backup codes."""
#         backup_codes = set()
#         while len(backup_codes) < count:
#             backup_codes.add(''.join(random.choices(string.digits, k=8)))
#         return list(backup_codes)

#     def validate_email(self, email):
#         """Validates if the email ends with '@gmail.com'."""
#         return email.endswith("@gmail.com")

#     def validate_phone(self, phone):
#         """Validates if the phone starts with '0' and contains 9-10 digits."""
#         return phone.startswith("0") and phone[1:].isdigit() and 9 <= len(phone) <= 10

#     def validate_password(self, password):
#         """Validates if the password meets complexity requirements."""
#         has_upper = any(char.isupper() for char in password)
#         has_lower = any(char.islower() for char in password)
#         has_special = any(char in string.punctuation for char in password)
#         return len(password) >= 8 and has_upper and has_lower and has_special

#     def show_error(self, message):
#         """Displays errors in a consistent format."""
#         print(f"\033[1;31m[Error] {message}\033[0m")

#     def show_success(self, message):
#         """Displays success messages in a consistent format."""
#         print(f"\033[1;32m[Success] {message}\033[0m")

#     def show_step(self, step_number, message):
#         """Displays steps in a consistent format."""
#         print(f"\033[1;34m[Step {step_number}] {message}\033[0m")

#     def _read_file_lines(self, file_path):
#         """Safely reads lines from a file."""
#         try:
#             with open(file_path, "r") as file:
#                 return file.readlines()
#         except FileNotFoundError:
#             return []
#         except Exception as e:
#             self.show_error(f"Error reading file '{file_path}': {e}")
#             return []

#     def _write_to_file(self, file_path, data, mode="a"):
#         """Safely writes data to a file."""
#         try:
#             with open(file_path, mode) as file:
#                 file.writelines(data)
#         except Exception as e:
#             self.show_error(f"Error writing to file '{file_path}': {e}")

#     def register_user(self):
#         """Registers a new user with retry limits and delay enforcement."""
#         max_attempts = 3  # Maximum attempts for each step
#         delay_time = 30  # Delay in seconds after exceeding attempts

#         # Step 1: Get a unique email or phone number
#         self.show_step(1, "Enter your email or phone number.")
#         failed_attempts = 0
#         while failed_attempts < max_attempts:
#             email_or_phone = input("Enter your email or phone number: ").strip()

#             # Check if the email/phone already exists
#             existing_users = self._read_file_lines(self.user_data_file)
#             if any(email_or_phone in user.split(",") for user in existing_users):
#                 self.show_error("This email or phone number is already registered.")
#                 failed_attempts += 1
#                 if failed_attempts >= max_attempts:
#                     self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
#                     time.sleep(delay_time)
#                     return
#                 continue

#             if "@" in email_or_phone:
#                 if not self.validate_email(email_or_phone):
#                     self.show_error("Invalid email format. Use a valid Gmail address (e.g., example@gmail.com).")
#                     failed_attempts += 1
#                 else:
#                     break
#             else:
#                 if not self.validate_phone(email_or_phone):
#                     self.show_error("Invalid phone number. Ensure it starts with '0' and is 9-10 digits long.")
#                     failed_attempts += 1
#                 else:
#                     break

#         # Step 2: Get a unique username
#         self.show_step(2, "Enter a unique username.")
#         failed_attempts = 0
#         while failed_attempts < max_attempts:
#             username = input("Enter your username: ").strip()

#             # Check if the username already exists
#             if any(username in user.split(",") for user in existing_users):
#                 self.show_error("This username is already taken. Please choose a different one.")
#                 failed_attempts += 1
#                 if failed_attempts >= max_attempts:
#                     self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
#                     time.sleep(delay_time)
#                     return
#                 continue

#             if not username:
#                 self.show_error("Username cannot be empty.")
#                 failed_attempts += 1
#             elif username == email_or_phone:
#                 self.show_error("Username and email/phone number cannot be the same.")
#                 failed_attempts += 1
#             else:
#                 break

#         # Step 3: Get and confirm password
#         self.show_step(3, "Enter and confirm your password.")
#         failed_attempts = 0
#         while failed_attempts < max_attempts:
#             password = input("Enter your password: ").strip()

#             if not self.validate_password(password):
#                 self.show_error("Password must be at least 8 characters long and include uppercase, lowercase, and special characters.")
#                 failed_attempts += 1
#                 if failed_attempts >= max_attempts:
#                     self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
#                     time.sleep(delay_time)
#                     return
#                 continue

#             confirm_password = input("Confirm your password: ").strip()
#             if password != confirm_password:
#                 self.show_error("Passwords do not match.")
#                 failed_attempts += 1
#             else:
#                 break

#         # Step 4: Save user and generate backup codes
#         salt = os.urandom(16)
#         hashed_password = self.hash_password(password, salt)
#         backup_codes = self.generate_backup_code(10)  # Generate 10 backup codes

#         # Save the user data
#         self._write_to_file(self.user_data_file, [f"{email_or_phone},{username},{salt.hex()},{hashed_password}\n"])

#         # Save backup codes
#         self._write_to_file(self.backup_code_file, [f"{email_or_phone},{code}\n" for code in backup_codes])

#         # Show success messages
#         self.show_success(f"User '{username}' registered successfully!")
#         print("\nHere are your backup codes:")
#         for code in backup_codes:
#             print(f"\033[1;33m{code}\033[0m")
#         print("\n\033[1;32mPlease save these backup codes in a secure location.\033[0m")
import hashlib
import os
import random
import string
import time

class UserSystem:
    def __init__(self, user_data_file, backup_code_file):
        self.user_data_file = os.path.join("Database_txt", user_data_file)
        self.backup_code_file = os.path.join("Database_txt", backup_code_file)

        # Ensure the Database_txt folder exists
        if not os.path.exists("Database_txt"):
            os.makedirs("Database_txt")

    def hash_password(self, password, salt):
        """Hashes the password using SHA256."""
        return hashlib.sha256(salt + password.encode()).hexdigest()

    def generate_backup_code(self, count=1):
        """Generates multiple 8-digit unique backup codes."""
        backup_codes = set()
        while len(backup_codes) < count:
            backup_codes.add(''.join(random.choices(string.digits, k=8)))
        return list(backup_codes)

    def validate_email(self, email):
        """Validates if the email ends with '@gmail.com'."""
        return email.endswith("@gmail.com")

    def validate_phone(self, phone):
        """Validates if the phone starts with '0' and contains 9-10 digits."""
        return phone.startswith("0") and phone[1:].isdigit() and 9 <= len(phone) <= 10

    def validate_password(self, password):
        """Validates if the password meets complexity requirements."""
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_special = any(char in string.punctuation for char in password)
        return len(password) >= 8 and has_upper and has_lower and has_special

    def validate_username(self, username):
        """
        Validates the username according to the specified rules:
        - At least 2 characters.
        - Can contain only one space.
        - Can contain characters and digits, but not all digits.
        """
        # Check for at least 2 characters
        if len(username) < 2:
            self.show_error("Username must be at least 2 characters long.")
            return False
        
        # Check if there is more than one space
        if username.count(" ") > 1:
            self.show_error("Username can only contain one space.")
            return False
        
        # Check if the username contains only digits (disallowed)
        if username.isdigit():
            self.show_error("Username cannot be all digits.")
            return False
        
        # Check if the username contains at least one non-digit character
        if not any(c.isalpha() for c in username):
            self.show_error("Username must contain at least one letter.")
            return False
        
        return True

    def show_error(self, message):
        """Displays errors in a consistent format."""
        print(f"\033[1;31m[Error] {message}\033[0m")

    def show_success(self, message):
        """Displays success messages in a consistent format."""
        print(f"\033[1;32m[Success] {message}\033[0m")

    def show_step(self, step_number, message):
        """Displays steps in a consistent format."""
        print(f"\033[1;34m[Step {step_number}] {message}\033[0m")

    def _read_file_lines(self, file_path):
        """Safely reads lines from a file."""
        try:
            with open(file_path, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            return []
        except Exception as e:
            self.show_error(f"Error reading file '{file_path}': {e}")
            return []

    def _write_to_file(self, file_path, data, mode="a"):
        """Safely writes data to a file."""
        try:
            with open(file_path, mode) as file:
                file.writelines(data)
        except Exception as e:
            self.show_error(f"Error writing to file '{file_path}': {e}")

    def register_user(self):
        """Registers a new user with retry limits and delay enforcement."""
        max_attempts = 3  # Maximum attempts for each step
        delay_time = 30  # Delay in seconds after exceeding attempts

        # Step 1: Get a unique email or phone number
        self.show_step(1, "Enter your email or phone number.")
        failed_attempts = 0
        while failed_attempts < max_attempts:
            email_or_phone = input("Enter your email or phone number: ").strip()

            # Check if the email/phone already exists
            existing_users = self._read_file_lines(self.user_data_file)
            if any(email_or_phone in user.split(",") for user in existing_users):
                self.show_error("This email or phone number is already registered.")
                failed_attempts += 1
                if failed_attempts >= max_attempts:
                    self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
                    time.sleep(delay_time)
                    return
                continue

            if "@" in email_or_phone:
                if not self.validate_email(email_or_phone):
                    self.show_error("Invalid email format. Use a valid Gmail address (e.g., example@gmail.com).")
                    failed_attempts += 1
                else:
                    break
            else:
                if not self.validate_phone(email_or_phone):
                    self.show_error("Invalid phone number. Ensure it starts with '0' and is 9-10 digits long.")
                    failed_attempts += 1
                else:
                    break

        # Step 2: Get a unique username
        self.show_step(2, "Enter a unique username.")
        failed_attempts = 0
        while failed_attempts < max_attempts:
            username = input("Enter your username: ").strip()

            # Check if the username already exists
            if any(username in user.split(",") for user in existing_users):
                self.show_error("This username is already taken. Please choose a different one.")
                failed_attempts += 1
                if failed_attempts >= max_attempts:
                    self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
                    time.sleep(delay_time)
                    return
                continue

            if not self.validate_username(username):
                failed_attempts += 1
            else:
                break

        # Step 3: Get and confirm password
        self.show_step(3, "Enter and confirm your password.")
        failed_attempts = 0
        while failed_attempts < max_attempts:
            password = input("Enter your password: ").strip()

            if not self.validate_password(password):
                self.show_error("Password must be at least 8 characters long and include uppercase, lowercase, and special characters.")
                failed_attempts += 1
                if failed_attempts >= max_attempts:
                    self.show_error(f"Too many invalid attempts. Try again after {delay_time} seconds.")
                    time.sleep(delay_time)
                    return
                continue

            confirm_password = input("Confirm your password: ").strip()
            if password != confirm_password:
                self.show_error("Passwords do not match.")
                failed_attempts += 1
            else:
                break

        # Step 4: Save user and generate backup codes
        salt = os.urandom(16)
        hashed_password = self.hash_password(password, salt)
        backup_codes = self.generate_backup_code(10)  # Generate 10 backup codes

        # Save the user data
        self._write_to_file(self.user_data_file, [f"{email_or_phone},{username},{salt.hex()},{hashed_password}\n"])

        # Save backup codes
        self._write_to_file(self.backup_code_file, [f"{email_or_phone},{code}\n" for code in backup_codes])

        # Show success messages
        self.show_success(f"User '{username}' registered successfully!")
        print("\nHere are your backup codes:")
        for code in backup_codes:
            print(f"\033[1;33m{code}\033[0m")
        print("\n\033[1;32mPlease save these backup codes in a secure location.\033[0m")

