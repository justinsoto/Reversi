from database.db_management.user_manager import UserManager
import re

class UserManagerProxy:
    """
    A proxy class for UserManager that adds input validation and SQL injection checks
    before performing operations related to user management in the database.
    """    
    def __init__(self, connection):
        """
        Initializes a new instance of UserManagerProxy with a database connection.

        Parameters:
        connection: A database connection object, which will be used to initialize the UserManager.
        """        
        self.user_manager = UserManager(connection)

    def validate_input(self, input_string):
        """
        Validates the user input using a regular expression to ensure it only contains
        allowed characters.

        Parameters:
        input_string (str): The input string to validate.

        Returns:
        bool: True if the input string matches the allowed pattern, False otherwise.
        """        
        pattern = r'^[a-zA-Z0-9_!&$?-]+$'
        if re.match(pattern, input_string):
            return True
        else:
            return False

    def check_sql_injection(self, input_string):
        """
        Checks if the input string contains SQL injection risks.

        Parameters:
        input_string (str): The input string to check for potential SQL injection patterns.

        Returns:
        bool: True if no SQL injection risks are found, False if risks are detected.
        """        
        sql_injections = ["'", '"', ";", "DROP TABLE", "SELECT * FROM"]
        for injection in sql_injections:
            if injection in input_string:
                return False
        return True

    def create_user(self, username, password):
        """
        Creates a new user in the database, first validating the username and password.

        Parameters:
        username (str): The desired username.
        password (str): The desired password.

        Returns:
        str: A success message if the user is created, or an error message if input validation fails.
        """        
        if self.validate_input(username) and self.validate_input(password)\
        and self.check_sql_injection(username)\
        and self.check_sql_injection(password):
            self.user_manager.create_user(username, password)
        else:
            return "Invalid input. Please try again."

    def login(self, username, password):
        """
        Attempts to log a user in by first validating the username and password.

        Parameters:
        username (str): The username of the user trying to log in.
        password (str): The password of the user trying to log in.

        Returns:
        str: The user details if login is successful, or an error message if validation fails.
        """        
        if self.validate_input(username) and self.validate_input(password)\
        and self.check_sql_injection(username)\
        and self.check_sql_injection(password):
            return self.user_manager.login(username, password)
        else:
            return "Invalid input. Please try again."

    def get_current_user(self):
        """
        Retrieves the currently logged-in user.

        Returns:
        User: The user object of the currently logged-in user.
        """        
        return self.user_manager.get_current_user()

    def get_user_by_id(self, user_id):
        """
        Retrieves a user by their ID after validating that the ID is numeric.

        Parameters:
        user_id (str): The user ID to lookup.

        Returns:
        str/User: The user object if found and valid, or an error message if the ID format is invalid.
        """        
        if user_id.isdigit():
            return self.user_manager.get_user_by_id(user_id)
        else:
            return "Invalid user ID format."

    def get_user_by_username(self, username):
        """
        Retrieves a user by their username after validating for input format and SQL injection.

        Parameters:
        username (str): The username to lookup.

        Returns:
        str/User: The user object if found and valid, or an error message if the username format is invalid.
        """
        if self.validate_input(username) and self.check_sql_injection(username):
            return self.user_manager.get_user_by_username(username)
        else:
            return "Invalid username format."

    def delete_user(self, username):
        """
        Deletes a user by their username after validating the username format and checking for SQL injections.

        Parameters:
        username (str): The username of the user to delete.

        Returns:
        str: A success message if the user is deleted, or an error message if the username format is invalid.
        """        
        if self.validate_input(username) and self.check_sql_injection(username):
            return self.user_manager.delete_user(username)
        else:
            return "Invalid username format."