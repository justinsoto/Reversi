from database.db_management.user_manager import UserManager
import re

class UserManagerProxy:
    def __init__(self, connection):
        self.user_manager = UserManager(connection)

    def validate_input(self, input_string):
        pattern = r'^[a-zA-Z0-9_!&$?-]+$'
        if re.match(pattern, input_string):
            return True
        else:
            return False

    def check_sql_injection(self, input_string):
        sql_injections = ["'", '"', ";", "DROP TABLE", "SELECT * FROM"]
        for injection in sql_injections:
            if injection in input_string:
                return False
        return True

    def create_user(self, username, password):
        if self.validate_input(username) and self.validate_input(password)\
        and self.check_sql_injection(username)\
        and self.check_sql_injection(password):
            self.user_manager.create_user(username, password)
        else:
            return "Invalid input. Please try again."

    def login(self, username, password):
        if self.validate_input(username) and self.validate_input(password)\
        and self.check_sql_injection(username)\
        and self.check_sql_injection(password):
            return self.user_manager.login(username, password)
        else:
            return "Invalid input. Please try again."

    def get_current_user(self):
        return self.user_manager.get_current_user()

    def get_user_by_id(self, user_id):
        if user_id.isdigit():
            return self.user_manager.get_user_by_id(user_id)
        else:
            return "Invalid user ID format."

    def get_user_by_username(self, username):
        if self.validate_input(username) and self.check_sql_injection(username):
            return self.user_manager.get_user_by_username(username)
        else:
            return "Invalid username format."

    def delete_user(self, username):
        if self.validate_input(username) and self.check_sql_injection(username):
            return self.user_manager.delete_user(username)
        else:
            return "Invalid username format."
