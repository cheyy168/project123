import hashlib
import os
import random
import re


class Recovery:
    def __init__(self, user_data_file, backup_code_file):
        self.user_data_file = os.path.join("Database_txt", user_data_file)
        self.backup_code_file = os.path.join("Database_txt", backup_code_file)

    def generate_backup_code(self):
        """Generates a backup code with 8 digits."""
        return ''.join(random.choices('0123456789', k=8))

    def save_backup_code(self, user_identifier, code):
        """Saves the backup code for a user."""
        try:
            os.makedirs(os.path.dirname(self.backup_code_file), exist_ok=True)
            with open(self.backup_code_file, "a") as file:
                file.write(f"{user_identifier},{code}\n")
        except Exception as e:
            print(f"Error saving backup code: {e}")

    def recover_password(self):
        """Handles password recovery using a backup code."""
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            email_or_phone = input("Enter your email or phone number: ").strip()
            backup_code = input("Enter your backup code: ").strip()

            try:
                lines = []
                code_verified = False

                with open(self.backup_code_file, "r") as file:
                    for line in file:
                        try:
                            stored_identifier, stored_code = line.strip().split(",")
                        except ValueError:
                            continue

                        if email_or_phone == stored_identifier and backup_code == stored_code:
                            code_verified = True
                        else:
                            lines.append(line)  # Keep unused codes

                if code_verified:
                    print("Backup code verified successfully!")
                    with open(self.backup_code_file, "w") as file:
                        file.writelines(lines)  # Remove used code
                    self.reset_password(email_or_phone)
                    return

            except FileNotFoundError:
                print("Backup code file not found. Please contact support.")
                return
            except ValueError:
                print("Error reading backup codes. Please contact support.")
                return

            attempts += 1
            remaining_attempts = max_attempts - attempts
            print(f"Invalid backup code. You have {remaining_attempts} attempt(s) remaining.")

        print("Maximum attempts reached. Password recovery failed.")

    def reset_password(self, user_identifier):
        """Allows the user to reset their password."""
        temp_file = self.user_data_file + ".tmp"
        password_updated = False

        for _ in range(3):  # Allow up to 3 attempts for a valid password
            new_password = input("Enter your new password: ").strip()

            if not self.validate_password_strength(new_password):
                print("Password does not meet the required standards. Try again.")
                continue

            try:
                with open(self.user_data_file, "r") as file, open(temp_file, "w") as temp:
                    for line in file:
                        data = line.strip().split(",")
                        if len(data) < 4:
                            temp.write(line)
                            continue

                        email_or_phone, username, salt_hex, hashed_password = data


                        if user_identifier == email_or_phone:
                            salt = os.urandom(16)  # Generate a new salt
                            hashed_new_password = self.hash_password(new_password, salt)
                            temp.write(f"{email_or_phone},{username},{salt.hex()},{hashed_new_password}\n")
                            password_updated = True
                        else:
                            temp.write(line)
            except FileNotFoundError:
                print("User data file not found. Please contact support.")
                return
            except Exception as e:
                print(f"Error resetting password: {e}")
                return

            os.replace(temp_file, self.user_data_file)

            if password_updated:
                print("Password reset successfully!")
                return
            else:
                print("User not found. Password not reset.")
                return

        print("Failed to reset password after multiple attempts.")

    def hash_password(self, password, salt):
        """Hashes the password using SHA256."""
        return hashlib.sha256(salt + password.encode()).hexdigest()

    def validate_password_strength(self, password):
        """Validates the strength of a password."""
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return False
        if not re.search(r"[A-Z]", password):
            print("Password must contain at least one uppercase letter.")
            return False
        if not re.search(r"[a-z]", password):
            print("Password must contain at least one lowercase letter.")
            return False
        if not re.search(r"[0-9]", password):
            print("Password must contain at least one digit.")
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            print("Password must contain at least one special character.")
            return False
        return True
