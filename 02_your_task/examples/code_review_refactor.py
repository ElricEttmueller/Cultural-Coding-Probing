"""
🔄 Code Review Challenge: API Service Optimization

Background:
-----------
Our team has built a REST API service that handles user authentication and
data management. The code works but needs improvement in terms of:
- Performance
- Error handling
- Code organization
- Documentation

Your Task:
----------
Review and improve the code while maintaining functionality.
Focus on:
1. Code structure and organization
2. Error handling and validation
3. Performance optimization
4. Documentation and clarity

Remember: Document your thought process as you refactor! 🤔
"""

from typing import Dict, List, Optional, Union
import json
import time
from datetime import datetime
from pathlib import Path
import logging
from functools import wraps

# Current implementation with room for improvement
class UserAPI:
    def __init__(self, data_dir: str = "./data"):
        # @probe:architecture 🏗️ What architectural issues do you see?
        # - How would you organize this better?
        # - What patterns would you apply?
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.users: Dict[str, Dict] = {}
        self._load_users()
        
        # Basic caching
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
    
    def _load_users(self) -> None:
        """Load user data from files."""
        # @probe:performance 🚀 How would you improve data loading?
        # - What bottlenecks do you see?
        # - How would you optimize this?
        for user_file in self.data_dir.glob("*.json"):
            try:
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    self.users[user_data['id']] = user_data
            except json.JSONDecodeError as e:
                print(f"Error loading {user_file}: {e}")
                continue
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return token."""
        # @probe:security 🔒 What security concerns do you see?
        # - How would you handle authentication better?
        # - What vulnerabilities exist?
        for user_id, user in self.users.items():
            if user['username'] == username and user['password'] == password:
                return f"token_{user_id}_{int(time.time())}"
        return None
    
    def get_user(self, user_id: str, token: str) -> Optional[Dict]:
        """Get user data if token is valid."""
        # @probe:validation ✅ How would you improve validation?
        # - What checks are missing?
        # - How would you handle errors?
        if not self._validate_token(token):
            return None
            
        # Check cache first
        cache_key = f"user_{user_id}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached_data
        
        user_data = self.users.get(user_id)
        if user_data:
            # Cache the result
            self.cache[cache_key] = (user_data, time.time())
            return user_data
        return None
    
    def update_user(self, user_id: str, token: str, data: Dict) -> bool:
        """Update user data if token is valid."""
        # @probe:consistency 🤝 How would you ensure data consistency?
        # - What race conditions might occur?
        # - How would you handle concurrent updates?
        if not self._validate_token(token):
            return False
            
        if user_id not in self.users:
            return False
            
        # Update user data
        self.users[user_id].update(data)
        
        # Save to file
        try:
            user_file = self.data_dir / f"{user_id}.json"
            with open(user_file, 'w') as f:
                json.dump(self.users[user_id], f)
            
            # Invalidate cache
            cache_key = f"user_{user_id}"
            if cache_key in self.cache:
                del self.cache[cache_key]
                
            return True
        except Exception as e:
            print(f"Error saving user data: {e}")
            return False
    
    def _validate_token(self, token: str) -> bool:
        """Validate authentication token."""
        # @probe:security 🔒 How would you improve token validation?
        # - What additional checks would you add?
        # - How would you handle token expiration?
        try:
            parts = token.split('_')
            if len(parts) != 3 or parts[0] != "token":
                return False
            
            user_id = parts[1]
            timestamp = int(parts[2])
            
            # Check if token is expired (1 hour)
            if time.time() - timestamp > 3600:
                return False
                
            return user_id in self.users
        except:
            return False

def main():
    # @probe:testing 🧪 How would you test this code?
    # - What test cases would you add?
    # - How would you structure tests?
    
    # Example usage with issues to identify
    api = UserAPI()
    
    # Create test user
    test_user = {
        "id": "user123",
        "username": "testuser",
        "password": "password123",  # Security issue!
        "email": "test@example.com",
        "created_at": datetime.now().isoformat()
    }
    
    # Save test user
    with open(api.data_dir / "user123.json", 'w') as f:
        json.dump(test_user, f)
    
    # Reload users
    api._load_users()
    
    # Test authentication
    token = api.authenticate("testuser", "password123")
    if token:
        print("Authentication successful!")
        
        # Test user retrieval
        user_data = api.get_user("user123", token)
        if user_data:
            print("User data retrieved!")
            
            # Test user update
            update_success = api.update_user("user123", token, {
                "last_login": datetime.now().isoformat()
            })
            if update_success:
                print("User data updated!")
            else:
                print("Failed to update user data!")
        else:
            print("Failed to retrieve user data!")
    else:
        print("Authentication failed!")

if __name__ == "__main__":
    main()
