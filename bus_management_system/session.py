# session.py
class UserSession:
    """Manage current user session"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.current_user = None
        self.is_authenticated = False
        
    def login(self, user_data):
        """Login user"""
        self.current_user = user_data
        self.is_authenticated = True
        
    def logout(self):
        """Logout user"""
        self.current_user = None
        self.is_authenticated = False
        
    def get_current_user(self):
        """Get current user"""
        return self.current_user
    
    def get_username(self):
        """Get current username"""
        return self.current_user.get('username') if self.current_user else None
    
    def get_role(self):
        """Get current user role"""
        return self.current_user.get('role') if self.current_user else None
    
    def get_user_id(self):
        """Get current user ID"""
        return self.current_user.get('id') if self.current_user else None
    
    def get_full_name(self):
        """Get current user full name"""
        return self.current_user.get('full_name') if self.current_user else None
    
    def has_permission(self, module):
        """Check if user has permission for module"""
        if not self.current_user:
            return False
        
        role = self.current_user.get('role')
        
        # Define permissions
        permissions = {
            'Super Admin': ['Dashboard', 'Buses', 'Drivers', 'Schools', 'Reports', 'User Management', 'System Settings', 'Help'],
            'Admin': ['Dashboard', 'Buses', 'Drivers', 'Schools', 'Reports', 'User Management', 'System Settings', 'Help'],
            'Manager': ['Dashboard', 'Buses', 'Drivers', 'Schools', 'Reports', 'Help'],
            'Accountant': ['Dashboard', 'Reports', 'Help'],
            'Driver': ['Dashboard', 'Help'],
            'Viewer': ['Dashboard', 'Reports', 'Help'],
            'User': ['Dashboard', 'Reports', 'Help']
        }
        
        return module in permissions.get(role, [])