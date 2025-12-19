import hashlib
from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = True

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == self._hash_password(password)

class Administrator(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password)
        self.permissions = permissions if permissions else []

    def add_permission(self, permission):
        self.permissions.append(permission)

class RegularUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.last_login = None

    def update_last_login(self):
        self.last_login = datetime.now()

class GuestUser(User):
    def __init__(self, username="guest"):
        super().__init__(username, "guest_password")
        self.access_rights = "read_only"

class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        if user.username in self.users:
            print(f"User {user.username} already exists.")
        else:
            self.users[user.username] = user

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password):
            if user.is_active:
                if isinstance(user, RegularUser):
                    user.update_last_login()
                return user
        return None

if __name__ == "__main__":
    access_system = AccessControl()

    admin = Administrator("admin_max", "admin123", ["manage_users", "delete_db"])
    user_bob = RegularUser("bob_jones", "bobby2023")
    guest = GuestUser("guest_01")

    access_system.add_user(admin)
    access_system.add_user(user_bob)
    access_system.add_user(guest)

    print("--- Test Authentication ---")
    
    logged_in_admin = access_system.authenticate_user("admin_max", "admin123")
    if logged_in_admin:
        print(f"Logged in as: {logged_in_admin.username} (Role: Administrator)")
        print(f"Permissions: {logged_in_admin.permissions}")

    logged_in_user = access_system.authenticate_user("bob_jones", "wrong_password")
    if not logged_in_user:
        print("Login failed for bob_jones (wrong password)")

    logged_in_user = access_system.authenticate_user("bob_jones", "bobby2023")
    if logged_in_user:
        print(f"Logged in as: {logged_in_user.username} (Role: RegularUser)")
        print(f"Last login: {logged_in_user.last_login}")
