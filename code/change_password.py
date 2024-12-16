import hashlib
import os

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
        """
        Initializes the ChangePassword class with a user data file.
        Args:
            user_data_file (str): Path to the user data file.
        """
        self.user_data_file = os.path.join("Database_txt", user_data_file)

    def hash_password(self, password, salt):
        """
        Hashes the password using SHA256.
        Args:
            password (str): The password to hash.
            salt (bytes): The salt value for hashing.
        Returns:
            str: The hashed password as a hex digest.
        """
        return hashlib.sha256(salt + password.encode()).hexdigest()

    def validate_password_strength(self, password):
        """
        Validates the strength of a password.
        Args:
            password (str): The password to validate.
        Returns:
            bool: True if the password is strong, False otherwise.
        """
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

    def change_password(self, user_identifier):
        """
        Handles the process of changing a user's password.
        Args:
            user_identifier (str): The user's email or phone number to identify their account.
        """
        print(f"{Colors.OKCYAN}=== Change Password ==={Colors.ENDC}")

        # Step 1: Prompt for current password
        current_password = input("Enter your current password: ").strip()

        # Step 2: Validate current password
        current_password_valid = False
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

        # If current password is incorrect, exit
        if not current_password_valid:
            print(f"{Colors.FAIL}Current password is incorrect. Password change failed.{Colors.ENDC}")
            return

        # Step 3: Prompt for new password
        new_password = input("Enter your new password: ").strip()

        # Validate password strength
        if not self.validate_password_strength(new_password):
            print(f"{Colors.FAIL}Password does not meet the required standards.{Colors.ENDC}")
            return

        temp_file = self.user_data_file + ".tmp"
        password_updated = False

        # Step 4: Update password
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

        # Provide feedback to the user
        if password_updated:
            print(f"{Colors.OKGREEN}Password changed successfully!{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}User not found. Password not changed.{Colors.ENDC}")
