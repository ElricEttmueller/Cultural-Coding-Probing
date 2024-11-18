"""
Example scenario: Feature Development
This example demonstrates how probes can gather insights during new feature development.
"""

from typing import List, Dict, Optional
import json

class UserPreferences:
    # @probe:environment How do you organize your workspace when working
    # on a new feature? Do you have specific window arrangements?
    def __init__(self):
        self.preferences: Dict = {}
        
    def save(self, filepath: str) -> None:
        # @probe:sustainability Do you consider file I/O performance when
        # deciding how often to save user preferences?
        with open(filepath, 'w') as f:
            json.dump(self.preferences, f)
    
    def load(self, filepath: str) -> None:
        # @probe:workflow When adding error handling, do you prefer to
        # handle all edge cases upfront or add them iteratively?
        try:
            with open(filepath, 'r') as f:
                self.preferences = json.load(f)
        except FileNotFoundError:
            self.preferences = {}

class ThemeManager:
    # @probe:tools What IDE features do you use most when implementing
    # new classes? (autocomplete, documentation, etc.)
    def __init__(self):
        self.current_theme: str = "default"
        self.available_themes: List[str] = ["default", "dark", "light"]
    
    def set_theme(self, theme: str) -> bool:
        # @probe:workflow How do you validate your assumptions when
        # implementing new functionality?
        if theme not in self.available_themes:
            return False
        self.current_theme = theme
        return True
    
    def get_theme_colors(self) -> Dict[str, str]:
        # @probe:environment Does your editor's color scheme affect how
        # you write code that deals with colors and themes?
        themes = {
            "default": {"background": "#FFFFFF", "text": "#000000"},
            "dark": {"background": "#1E1E1E", "text": "#FFFFFF"},
            "light": {"background": "#F5F5F5", "text": "#333333"}
        }
        return themes[self.current_theme]

class SettingsManager:
    def __init__(self):
        # @probe:tools Which tools do you use to manage configuration and settings?
        self.preferences = UserPreferences()
        self.theme_manager = ThemeManager()
    
    def apply_user_settings(self, settings: Dict) -> None:
        # @probe:workflow How do you approach implementing features that
        # affect multiple components?
        if "theme" in settings:
            self.theme_manager.set_theme(settings["theme"])
        self.preferences.preferences.update(settings)
    
    def get_current_settings(self) -> Dict:
        return {
            "theme": self.theme_manager.current_theme,
            **self.preferences.preferences
        }

# Example usage
if __name__ == "__main__":
    # @probe:environment How do you test new features in your development environment?
    settings = SettingsManager()
    
    # Apply some user settings
    user_settings = {
        "theme": "dark",
        "font_size": 14,
        "show_line_numbers": True
    }
    
    settings.apply_user_settings(user_settings)
    current_settings = settings.get_current_settings()
    print("Current Settings:", json.dumps(current_settings, indent=2))
