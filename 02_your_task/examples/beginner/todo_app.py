"""
Simple To-Do List Application 📝

This is a beginner-friendly example that demonstrates:
- Basic Python syntax
- Simple data structures (lists, dictionaries)
- File I/O operations
- Command-line interaction

@probe:organization 🏗️ How do you organize your code?
- Do you prefer classes or functions?
- How do you group related functionality?
- What naming conventions do you follow?

@probe:error_handling ⚠️ How do you handle errors?
- What exceptions would you add?
- How would you make the app more robust?
- What user mistakes should we catch?

@probe:user_experience 👥 How would you improve the UX?
- What feedback would you add?
- How would you make it more intuitive?
- What features are missing?
"""

import json
from datetime import datetime
from pathlib import Path

class TodoList:
    """A simple to-do list manager."""
    
    def __init__(self):
        """Initialize the to-do list."""
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()
    
    def add_task(self, description: str) -> bool:
        """Add a new task to the list."""
        # @probe:validation ✅ How do you validate user input?
        # - What checks would you add?
        # - How do you handle invalid input?
        # - What feedback do you provide?
        
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "done": False,
            "created_at": datetime.now().isoformat()
        }
        
        self.tasks.append(task)
        return self.save_tasks()
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete.
        
        Args:
            task_id: ID of task to complete
            
        Returns:
            bool: True if task was marked complete
        """
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = True
                return self.save_tasks()
        return False
    
    def list_tasks(self) -> None:
        """Display all tasks."""
        if not self.tasks:
            print("No tasks yet! 🎉")
            return
        
        print("\nYour Tasks:")
        print("-" * 40)
        
        for task in self.tasks:
            status = "✅" if task["done"] else "❌"
            print(f"{task['id']}. [{status}] {task['description']}")
        
        print("-" * 40)
    
    def save_tasks(self) -> bool:
        """Save tasks to file.
        
        Returns:
            bool: True if save was successful
        """
        try:
            with open(self.filename, "w") as f:
                json.dump(self.tasks, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def load_tasks(self) -> None:
        """Load tasks from file."""
        try:
            if Path(self.filename).exists():
                with open(self.filename, "r") as f:
                    self.tasks = json.load(f)
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []

def main():
    """Main program loop."""
    todo = TodoList()
    
    while True:
        print("\n📝 Todo List Menu:")
        print("1. Add Task")
        print("2. Complete Task")
        print("3. List Tasks")
        print("4. Exit")
        
        choice = input("\nWhat would you like to do? (1-4): ")
        
        if choice == "1":
            task = input("Enter task description: ")
            if todo.add_task(task):
                print("Task added successfully! ✨")
            else:
                print("Failed to add task 😢")
                
        elif choice == "2":
            todo.list_tasks()
            task_id = input("Enter task ID to complete: ")
            try:
                if todo.complete_task(int(task_id)):
                    print("Task completed! 🎉")
                else:
                    print("Task not found 😕")
            except ValueError:
                print("Please enter a valid task ID!")
                
        elif choice == "3":
            todo.list_tasks()
            
        elif choice == "4":
            print("Goodbye! 👋")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
