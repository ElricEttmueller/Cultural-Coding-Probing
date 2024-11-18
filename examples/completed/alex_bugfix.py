"""
Example of a completed bug fix scenario with probe responses.
Original bug: Invalid price handling in shopping cart
"""

from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional

# @probe:workflow How do you typically approach debugging tasks like this?
# Response: I start with logging and reproduction steps, then use the debugger
# for complex cases. I find it helpful to write down my hypotheses before diving in.

def validate_price(price_str: str) -> Optional[Decimal]:
    """Validate and convert price string to Decimal."""
    # @probe:tools Which debugging tools are you using to track the values here?
    # Response: I'm using VS Code's debugger with watch expressions to monitor
    # price_str at different stages of validation. Print statements help trace flow.
    
    try:
        # Strip currency symbols and whitespace
        cleaned_price = price_str.strip().strip('$')
        price = Decimal(cleaned_price)
        
        if price < 0:
            return None
        return price
    except (InvalidOperation, ValueError):
        return None

def calculate_total(items: List[Dict]) -> Decimal:
    """Calculate total price of items in cart."""
    # @probe:environment When encountering errors, how does your environment
    # help or hinder your debugging process?
    # Response: My dual monitor setup helps - code on main screen, debug output
    # on secondary. Standing desk helps maintain focus during long debug sessions.
    
    total = Decimal('0')
    for item in items:
        try:
            if 'price' not in item:
                print(f"Warning: Missing price for item: {item.get('name', 'unknown')}")
                continue
                
            price = validate_price(item['price'])
            if price is None:
                print(f"Warning: Invalid price format for item: {item.get('name', 'unknown')}")
                continue
                
            total += price
        except Exception as e:
            # @probe:sustainability How do you balance error handling with performance?
            # Response: I use specific exceptions where possible, falling back to
            # general Exception only for unexpected cases. Logging helps track issues.
            print(f"Error processing item: {item}")
            continue
    
    return total

class ShoppingCart:
    def __init__(self):
        self.items: List[Dict] = []
    
    def add_item(self, item: Dict) -> bool:
        """Add an item to the cart with validation."""
        # @probe:workflow Do you prefer to add validation immediately or
        # implement basic functionality first?
        # Response: I start with basic functionality and add validation
        # incrementally. This helps identify what validation is actually needed.
        
        if not isinstance(item, dict):
            print("Error: Item must be a dictionary")
            return False
            
        if 'price' not in item:
            print(f"Error: Missing price for item: {item.get('name', 'unknown')}")
            return False
            
        if validate_price(item['price']) is None:
            print(f"Error: Invalid price format for item: {item.get('name', 'unknown')}")
            return False
        
        self.items.append(item)
        return True
    
    def get_total(self) -> Decimal:
        """Calculate total price of items in cart."""
        return calculate_total(self.items)

# Example usage with tests
if __name__ == "__main__":
    # @probe:tools What tools do you use to test edge cases?
    # Response: I create a test suite with pytest, using parameterized tests
    # for different edge cases. VS Code's test explorer helps organize tests.
    
    cart = ShoppingCart()
    
    # Test cases demonstrating fixed functionality
    test_items = [
        {'name': 'apple', 'price': '1.99'},        # Valid price
        {'name': 'orange', 'price': '$0.99'},      # Valid price with symbol
        {'name': 'banana', 'price': 'invalid'},    # Invalid price
        {'name': 'grape'},                         # Missing price
        {'name': 'melon', 'price': '-1.50'},      # Negative price
        {'name': 'pear', 'price': '2.50 '},       # Price with whitespace
    ]
    
    print("\nTesting item addition:")
    for item in test_items:
        success = cart.add_item(item)
        print(f"Adding {item.get('name', 'unknown')}: {'Success' if success else 'Failed'}")
    
    print(f"\nCart total: ${cart.get_total()}")
