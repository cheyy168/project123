#Project Overview 
The project, "Verify Me," is designed to provide a secure and user-friendly experience for account management and authentication. Its primary purpose is to protect users' sensitive information while offering a simple and reliable way to access their accounts. Key functionalities include:

1. Password Hashing: User passwords are securely hashed, ensuring they are never stored in plain text, providing protection against cyberattacks.

2. Secure Account Recovery: In case of forgotten credentials, users can recover access through secure methods like email verification, ensuring they aren’t locked out of their accounts.

3. Unique Identifiers: Each user is required to have a unique username and email address, preventing conflicts and simplifying account management.

#Steps to Run the Code:
First when we run the code there are 4 option to choose 
1.Register
2.Login
3.Forget Password
4.Exit

Option 1 :
Enter Email or Phone number : (email must be end with @gmail.com , Phone number must start with 0 and 9 number)
Enter Username : ( must be more than 2 letter and can only 1 space , can not input only number )
Enter password : (Must be match with the requirement ,one symbol ,upper letter , at least 8 letter )
Confirm password : ( must be the same as the password )

Backup codes will be generated: After successful registration, the program will generate 10 unique 8-digit backup codes for the user.
These codes will be displayed, and you should save them in a secure location.
Option 2 : 
 1.Login:
  	The user enters user@example.com as their email.
    .If this email exists in the database, the system prompts for the password.
Option 4: Exit the prgram.
    .If the password is correct, the user is logged in successfully and can access the user menu.
 2.Invalid Login:
    If the email does not exist or the password is incorrect, the user will be prompted to try again. After 3 failed attempts, the system will delay further attempts for 30 seconds.

 3.Change Password:
   After logging in, the user selects the option to change their password. The system will delegate this to the ChangePassword class, where the user will be asked to enter a new password and confirm it.
Option 3:
  Input your email or phone number:
    .The system will prompt you to enter your registered email or phone number.
    .The script will check if the provided email or phone matches a stored identifier in the backup_code_file.txt.
  Enter the backup code:
    .If you’ve received a backup code, input it when prompted. The system will validate the code.
    .If the code is valid, it will allow you to reset your password.
    .If the code is incorrect, you have a limited number of attempts (3 by default).
  Reset your password:
    .If the backup code is verified, the system will prompt you to enter a new password.
    .The new password must meet certain strength criteria (at least 8 characters long, containing uppercase, lowercase, numbers, and special characters).
    .You will have 3 attempts to enter a valid password.
  After successfully entering the new password, the system will hash it and update the user data file.
  #Dependencies or Installation Instructions:
    list of the libraries in use: [hashlib,os,time,random,string,re]
  	These libraries come pre-installed with Python, so do not need to install anything separately. If running Python 3, they should all be available by default.
   
      
