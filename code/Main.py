from register import UserSystem
from login import LoginSystem
from change_password import ChangePassword
from forget_password import Recovery

def display_menu():
    """Displays the main menu options in a column-style layout."""
    print("\n")
    print("=" * 50)
    print(f"{'--- Welcome To Our User Management System ---':^50}")
    print("=" * 50)
    print(f"{'Option':<10}{'Description':<40}")
    print("-" * 50)
    print(f"{'1':<10}{'Register':<40}")
    print(f"{'2':<10}{'Login':<40}")
    print(f"{'3':<10}{'Forgot Password':<40}")
    print(f"{'4':<10}{'Exit':<40}")
    print("=" * 50)

def main():
    user_data_file = "database.txt"
    backup_code_file = "backup_codes.txt"

    # Initialize systems
    user_system = UserSystem(user_data_file, backup_code_file)
    change_password_system = ChangePassword(user_data_file)
    login_system = LoginSystem(user_data_file)
    recover_password_system = Recovery(user_data_file, backup_code_file)

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("=" * 50)
            print("\n            \033[1;36m*** User Registration ***\033[0m")
            print("=" * 50)
            print("\nPlease follow the instructions below to register:\n")
            user_system.register_user()

        elif choice == "2":
            print("=" * 50)
            print("\n               \033[1;36m*** User Login ***\033[0m")
            print("=" * 50)
            user_identifier = login_system.user_login()

            # If login is successful (assume user_identifier is returned on success)
            if user_identifier:
                change_choice = input(
                    "Do you want to change your password? (yes/no): ").strip().lower()
                if change_choice == "yes":
                    change_password_system.change_password(user_identifier)
                else:
                    print("Continuing without changing password.")

        elif choice == "3":
            print("\n--- Password Recovery ---")
            recover_password_system.recover_password()

        elif choice == "4":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()