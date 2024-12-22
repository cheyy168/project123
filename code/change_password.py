import hashlib
import os
import time

# Define color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # End color
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ChangePassword:
    def __init__(self, user_data_file):
        self.user_data_file = os.path.join("Database_txt", user_data_file)

    def hash_password(self, password, salt):
        return hashlib.sha256(salt + password.encode()).hexdigest()

    def validate_password_strength(self, password):
        print(f"{Colors.HEADER}Validating password strength...{Colors.ENDC}")
        if len(password) < 8:
            print(f"{Colors.WARNING}Password must be at least 8 characters long.{Colors.ENDC}")
            return False
        if not any(c.isupper() for c in password):
            print(f"{Colors.WARNING}Password must contain at least one uppercase letter.{Colors.ENDC}")
            return False
        if not any(c.isdigit() for c in password):
            print(f"{Colors.WARNING}Password must contain at least one number.{Colors.ENDC}")
            return False
        if not any(c in "!@#$%&*" for c in password):
            print(f"{Colors.WARNING}Password must contain at least one special character (!@#$%&*).{Colors.ENDC}")
            return False
        print(f"{Colors.OKGREEN}Password is strong!{Colors.ENDC}")
        return True

    def delay_and_retry(self, delay_seconds):
        print(f"{Colors.WARNING}Too many failed attempts. Please wait {delay_seconds} seconds...{Colors.ENDC}")
        time.sleep(delay_seconds)
        retry_choice = input(f"{Colors.OKCYAN}Do you want to try again? (yes/no): {Colors.ENDC}").strip().lower()
        return retry_choice == "yes"

    def change_password(self, user_identifier):
        max_attempts = 3
        delay_seconds = 30

        # Attempt loop for entering the current password
        while True:
            attempts = 0
            while attempts < max_attempts:
                current_password = input("Enter your current password: ").strip()

                # Validate current password
                current_password_valid = False
                try:
                    with open(self.user_data_file, "r") as file:
                        for line in file:
                            data = line.strip().split(",")
                            if len(data) < 4:
                                continue

                            email_or_phone, username, salt_hex, hashed_password = data

                            if user_identifier == email_or_phone:
                                salt = bytes.fromhex(salt_hex)
                                hashed_current_password = self.hash_password(current_password, salt)

                                if hashed_current_password == hashed_password:
                                    current_password_valid = True
                                    break
                except FileNotFoundError:
                    print(f"{Colors.FAIL}Error: User data file not found. Please check the file path.{Colors.ENDC}")
                    return
                except IOError:
                    print(f"{Colors.FAIL}Error: Unable to read the user data file.{Colors.ENDC}")
                    return

                if current_password_valid:
                    break  # Exit the attempts loop if password is valid

                attempts += 1
                print(f"{Colors.FAIL}Incorrect password. Attempts remaining: {max_attempts - attempts}.{Colors.ENDC}")

            if current_password_valid:
                break

            # Handle delay and retry decision after max attempts
            if not self.delay_and_retry(delay_seconds):
                print(f"{Colors.FAIL}Password change canceled.{Colors.ENDC}")
                return

            # Increase delay time after each set of 3 attempts
            delay_seconds *= 3

        # Step 3: Prompt for new password
        new_password = input("Enter your new password: ").strip()

        # Validate password strength
        if not self.validate_password_strength(new_password):
            print(f"{Colors.FAIL}Password does not meet the required standards.{Colors.ENDC}")
            return

        temp_file = self.user_data_file + ".tmp"
        password_updated = False

        # Step 4: Update password
        try:
            with open(self.user_data_file, "r") as file, open(temp_file, "w") as temp:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) < 4:
                        temp.write(line)
                        continue

                    email_or_phone, username, salt_hex, hashed_password = data

                    if user_identifier == email_or_phone:
                        # Generate a new salt and hash the new password
                        salt = os.urandom(16)
                        hashed_new_password = self.hash_password(new_password, salt)
                        temp.write(f"{email_or_phone},{username},{salt.hex()},{hashed_new_password}\n")
                        password_updated = True
                    else:
                        temp.write(line)

            # Replace the old data file with the updated one
            os.replace(temp_file, self.user_data_file)

        except FileNotFoundError:
            print(f"{Colors.FAIL}Error: User data file not found. Cannot update password.{Colors.ENDC}")
            return
        except IOError:
            print(f"{Colors.FAIL}Error: Unable to access or write to the user data file.{Colors.ENDC}")
            return

        # Provide feedback to the user
        if password_updated:
            print(f"{Colors.OKGREEN}Password changed successfully!{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}User not found. Password not changed.{Colors.ENDC}")
