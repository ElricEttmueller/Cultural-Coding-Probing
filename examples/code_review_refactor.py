"""
Example scenario: Code Review and Refactoring
This example shows how probes can gather insights during code review and refactoring tasks.
"""

from typing import List, Dict, Optional
from abc import ABC, abstractmethod

# @probe:workflow When reviewing code, what's your process for understanding
# the existing codebase structure?
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Dict) -> Dict:
        pass

class JSONProcessor(DataProcessor):
    # @probe:tools What tools do you use to ensure consistency when
    # refactoring similar classes?
    def process(self, data: Dict) -> Dict:
        # @probe:environment How does your editor's code navigation features
        # affect your refactoring approach?
        processed = {}
        for key, value in data.items():
            if isinstance(value, dict):
                processed[key] = self.process(value)
            elif isinstance(value, str):
                processed[key] = value.strip()
            else:
                processed[key] = value
        return processed

class DataValidator:
    # @probe:sustainability How do you balance validation thoroughness
    # with performance impact?
    def __init__(self, schema: Dict):
        self.schema = schema
    
    def validate(self, data: Dict) -> List[str]:
        # @probe:workflow During code review, how do you verify that all
        # edge cases are properly handled?
        errors = []
        for field, rules in self.schema.items():
            if field not in data:
                if rules.get("required", False):
                    errors.append(f"Missing required field: {field}")
                continue
            
            value = data[field]
            if "type" in rules:
                if not isinstance(value, rules["type"]):
                    errors.append(f"Invalid type for {field}")
            
            if "min_length" in rules and isinstance(value, (str, list)):
                if len(value) < rules["min_length"]:
                    errors.append(f"{field} is too short")
        
        return errors

class DataTransformer:
    # @probe:tools What refactoring tools do you rely on most heavily?
    def __init__(self, processor: DataProcessor, validator: DataValidator):
        self.processor = processor
        self.validator = validator
    
    def transform(self, data: Dict) -> tuple[Dict, List[str]]:
        # @probe:environment How does your testing environment influence
        # your refactoring decisions?
        processed_data = self.processor.process(data)
        validation_errors = self.validator.validate(processed_data)
        return processed_data, validation_errors

# Example usage
if __name__ == "__main__":
    # @probe:workflow How do you approach testing after significant refactoring?
    # Define a schema for user data
    user_schema = {
        "name": {"type": str, "required": True, "min_length": 2},
        "email": {"type": str, "required": True},
        "settings": {"type": dict, "required": False}
    }
    
    # Create processor and validator
    processor = JSONProcessor()
    validator = DataValidator(user_schema)
    transformer = DataTransformer(processor, validator)
    
    # Test with sample data
    test_data = {
        "name": "  John Doe  ",  # Extra whitespace to be processed
        "email": "john@example.com",
        "settings": {
            "theme": "  dark  ",  # Extra whitespace in nested dict
            "notifications": True
        }
    }
    
    processed_data, errors = transformer.transform(test_data)
    
    print("Processed Data:", processed_data)
    if errors:
        print("Validation Errors:", errors)
