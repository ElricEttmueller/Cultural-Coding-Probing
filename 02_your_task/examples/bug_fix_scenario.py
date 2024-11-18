"""
Example scenario: Bug Fix Task
This example shows how probes can be integrated into a typical bug fixing workflow.
"""

def calculate_total(items):
    # @probe:workflow How do you typically approach debugging tasks like this?
    # Is there a systematic method you follow?
    total = 0
    for item in items:
        # @probe:tools Which debugging tools are you using to track the values here?
        try:
            total += float(item['price'])
        except (KeyError, ValueError) as e:
            # @probe:environment When encountering errors, how does your environment
            # help or hinder your debugging process?
            print(f"Error processing item: {item}")
            continue
    return total

class ShoppingCart:
    def __init__(self):
        # @probe:sustainability How do you balance between using simple data structures
        # versus more sophisticated ones that might use more memory?
        self.items = []
    
    def add_item(self, item):
        """Add an item to the cart."""
        # @probe:workflow Do you prefer to add validation immediately or
        # implement basic functionality first?
        if not isinstance(item, dict) or 'price' not in item:
            raise ValueError("Invalid item format")
        self.items.append(item)
    
    def get_total(self):
        """Calculate total price of items in cart."""
        return calculate_total(self.items)

# Example usage with intentional bug for demonstration
if __name__ == "__main__":
    # @probe:tools What tools do you use to test edge cases?
    cart = ShoppingCart()
    
    # Test cases
    items = [
        {'name': 'apple', 'price': '1.99'},
        {'name': 'orange', 'price': '0.99'},
        {'name': 'banana', 'price': 'invalid'},  # Bug: invalid price
        {'name': 'grape'}  # Bug: missing price
    ]
    
    for item in items:
        try:
            cart.add_item(item)
        except ValueError as e:
            print(f"Failed to add item: {e}")
