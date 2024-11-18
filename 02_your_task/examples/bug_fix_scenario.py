"""
🐛 Bug Fix Challenge: The Data Pipeline Mystery

Background:
-----------
Our data processing pipeline is experiencing intermittent failures when handling
user analytics data. The bug seems to appear more frequently during peak hours
and with certain types of user data.

Your Task:
----------
Investigate and fix the bug in the DataProcessor class. Pay special attention to:
- Data validation
- Error handling
- Edge cases
- Performance implications

The Bug Report:
--------------
"Sometimes user sessions aren't being recorded correctly. The total session time
is showing as negative in some cases, and some user events are being dropped."

Remember: Document your thought process as you work! 💭
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class DataProcessor:
    def __init__(self):
        # @probe:architecture 🤔 How do you decide what data structures to use?
        # What factors influence your choice between different options?
        self.sessions: Dict[str, Dict] = {}
        self.events: List[Dict] = []
    
    def process_event(self, event_data: Dict) -> Optional[Dict]:
        """Process a single user event."""
        # @probe:debugging 🔍 When you encounter a bug:
        # - What's your first step?
        # - Which tools do you reach for?
        # - How do you reproduce the issue?
        
        try:
            # Validate event data
            if not self._validate_event(event_data):
                return None
            
            # Process timestamp
            timestamp = self._parse_timestamp(event_data.get('timestamp', ''))
            
            # Update session data
            user_id = event_data.get('user_id')
            if user_id:
                self._update_session(user_id, timestamp)
            
            # Store processed event
            processed_event = {
                'user_id': user_id,
                'timestamp': timestamp,
                'type': event_data.get('type'),
                'data': event_data.get('data', {})
            }
            self.events.append(processed_event)
            return processed_event
            
        except Exception as e:
            # @probe:error_handling 🚨 How do you approach error handling?
            # - Do you prefer detailed or minimal error messages?
            # - How do you decide what information to log?
            print(f"Error processing event: {str(e)}")
            return None

    def _validate_event(self, event: Dict) -> bool:
        """Validate event data structure."""
        # @probe:validation ✅ What's your validation strategy?
        # - Do you prefer strict or loose validation?
        # - How do you handle partial/malformed data?
        required_fields = ['user_id', 'timestamp', 'type']
        return all(field in event for field in required_fields)

    def _parse_timestamp(self, timestamp_str: str) -> float:
        """Parse and validate timestamp."""
        # @probe:edge_cases 🎯 How do you identify potential edge cases?
        # What's your strategy for handling them?
        try:
            if isinstance(timestamp_str, (int, float)):
                return float(timestamp_str)
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.timestamp()
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid timestamp format: {timestamp_str}")

    def _update_session(self, user_id: str, timestamp: float) -> None:
        """Update user session data."""
        # @probe:performance 🚀 How do you balance between:
        # - Code readability
        # - Performance optimization
        # - Memory usage
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                'start_time': timestamp,
                'last_seen': timestamp,
                'events': 1
            }
        else:
            session = self.sessions[user_id]
            if timestamp < session['start_time']:
                session['start_time'] = timestamp
            session['last_seen'] = timestamp
            session['events'] += 1

    def get_session_duration(self, user_id: str) -> float:
        """Calculate total session duration for a user."""
        # @probe:testing 🧪 What's your testing approach?
        # - How do you verify the fix works?
        # - What test cases do you create?
        if user_id not in self.sessions:
            return 0.0
        session = self.sessions[user_id]
        return session['last_seen'] - session['start_time']

# Example usage and test cases
def main():
    # @probe:workflow 🔄 How do you organize your debugging workflow?
    # Do you prefer to:
    # - Start with failing tests?
    # - Add logging/print statements?
    # - Use a debugger?
    
    processor = DataProcessor()
    
    # Test cases to help identify the bug
    test_events = [
        {
            'user_id': 'user1',
            'timestamp': '2023-01-01T10:00:00Z',
            'type': 'page_view',
            'data': {'page': 'home'}
        },
        {
            'user_id': 'user1',
            'timestamp': '2023-01-01T09:59:00Z',  # Earlier timestamp!
            'type': 'click',
            'data': {'element': 'button'}
        },
        {
            'user_id': 'user2',
            'timestamp': 1672567200,  # Unix timestamp
            'type': 'page_view',
            'data': {'page': 'profile'}
        },
        {
            'user_id': 'user2',
            'timestamp': '2023-01-01T10:00:00',  # Missing timezone
            'type': 'scroll',
            'data': {'position': 0.5}
        }
    ]
    
    # Process events
    for event in test_events:
        processor.process_event(event)
    
    # Check results
    for user_id in ['user1', 'user2']:
        duration = processor.get_session_duration(user_id)
        print(f"Session duration for {user_id}: {duration} seconds")

if __name__ == "__main__":
    main()
