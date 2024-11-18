"""
✨ Feature Development Challenge: Smart Task Scheduler

Background:
-----------
We're building a smart task scheduling system that helps users organize their
work more efficiently. Your task is to implement the core scheduling algorithm
that considers task priority, dependencies, and time constraints.

Your Task:
----------
Implement the TaskScheduler class with these features:
- Task priority handling
- Dependency resolution
- Time slot optimization
- Conflict resolution

Requirements:
------------
1. Tasks can have priorities (1-5)
2. Tasks can depend on other tasks
3. Tasks need specific time slots
4. Handle scheduling conflicts gracefully

Remember: Document your design decisions as you work! 💡
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from enum import Enum
import heapq

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

@dataclass
class TimeSlot:
    start: datetime
    duration: timedelta
    
    @property
    def end(self) -> datetime:
        return self.start + self.duration

@dataclass
class Task:
    id: str
    name: str
    priority: Priority
    estimated_duration: timedelta
    dependencies: Set[str]
    deadline: Optional[datetime] = None

class TaskScheduler:
    def __init__(self):
        # @probe:design 🎨 How do you approach system design?
        # - Do you sketch it first?
        # - Start with interfaces?
        # - Build incrementally?
        self.tasks: Dict[str, Task] = {}
        self.schedule: Dict[str, TimeSlot] = {}
        self.available_slots: List[TimeSlot] = []
    
    def add_task(self, task: Task) -> bool:
        """Add a new task to the scheduler."""
        # @probe:validation ✅ What validation do you add first?
        # - Basic type checking?
        # - Business logic rules?
        # - Edge cases?
        
        # Validate task
        if task.id in self.tasks:
            raise ValueError(f"Task {task.id} already exists")
            
        # Validate dependencies
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                raise ValueError(f"Dependency {dep_id} not found")
        
        self.tasks[task.id] = task
        return True
    
    def schedule_task(self, task_id: str) -> Optional[TimeSlot]:
        """Schedule a task in the best available time slot."""
        # @probe:algorithm 🧮 How do you approach algorithm design?
        # - Start simple and refine?
        # - Consider all edge cases first?
        # - Balance efficiency vs. readability?
        
        task = self.tasks.get(task_id)
        if not task:
            return None
            
        # Check dependencies
        for dep_id in task.dependencies:
            if dep_id not in self.schedule:
                return None  # Dependencies not scheduled yet
        
        # Find best slot
        return self._find_best_slot(task)
    
    def _find_best_slot(self, task: Task) -> Optional[TimeSlot]:
        """Find the best time slot for a task."""
        # @probe:optimization 🚀 How do you handle optimization?
        # - What metrics matter most?
        # - How do you measure improvement?
        # - When do you stop optimizing?
        
        available_slots = self._get_available_slots()
        if not available_slots:
            return None
            
        # Score each slot
        scored_slots = []
        for slot in available_slots:
            score = self._score_slot(slot, task)
            if score > 0:
                heapq.heappush(scored_slots, (-score, slot))
        
        return scored_slots[0][1] if scored_slots else None
    
    def _score_slot(self, slot: TimeSlot, task: Task) -> float:
        """Score a time slot for a specific task."""
        # @probe:metrics 📊 What factors do you consider?
        # - How do you weigh different criteria?
        # - What trade-offs do you make?
        score = 0.0
        
        # Priority bonus
        score += task.priority.value * 10
        
        # Deadline proximity
        if task.deadline:
            time_to_deadline = task.deadline - slot.end
            if time_to_deadline.total_seconds() < 0:
                return 0  # Past deadline
            score += min(100, time_to_deadline.total_seconds() / 3600)
        
        # Dependency optimization
        dep_score = self._calculate_dependency_score(task, slot)
        score += dep_score
        
        return score
    
    def _calculate_dependency_score(self, task: Task, slot: TimeSlot) -> float:
        """Calculate score based on dependency satisfaction."""
        # @probe:complexity 🤔 How do you manage complexity?
        # - When do you break down functions?
        # - How do you name things?
        # - What patterns do you use?
        score = 0.0
        
        for dep_id in task.dependencies:
            dep_slot = self.schedule.get(dep_id)
            if dep_slot:
                # Prefer slots closer to dependencies
                time_gap = slot.start - dep_slot.end
                if time_gap.total_seconds() < 0:
                    return 0  # Can't schedule before dependency
                score += 50 / (1 + time_gap.total_seconds() / 3600)
        
        return score

    def _get_available_slots(self) -> List[TimeSlot]:
        """Get list of available time slots."""
        # @probe:efficiency 🎯 How do you handle performance?
        # - What data structures do you choose?
        # - How do you optimize lookups?
        # - When do you cache?
        return self.available_slots

# Example usage
def main():
    # @probe:testing 🧪 How do you test complex features?
    # - What scenarios do you test first?
    # - How do you verify correctness?
    # - What edge cases matter most?
    
    scheduler = TaskScheduler()
    
    # Available time slots (9 AM to 5 PM)
    start_time = datetime(2024, 1, 1, 9, 0)
    for hour in range(8):
        slot = TimeSlot(
            start=start_time + timedelta(hours=hour),
            duration=timedelta(hours=1)
        )
        scheduler.available_slots.append(slot)
    
    # Create some tasks
    tasks = [
        Task(
            id="task1",
            name="Setup Database",
            priority=Priority.HIGH,
            estimated_duration=timedelta(hours=2),
            dependencies=set(),
            deadline=datetime(2024, 1, 1, 12, 0)
        ),
        Task(
            id="task2",
            name="Configure API",
            priority=Priority.MEDIUM,
            estimated_duration=timedelta(hours=1),
            dependencies={"task1"},
            deadline=datetime(2024, 1, 1, 15, 0)
        ),
        Task(
            id="task3",
            name="Deploy Service",
            priority=Priority.CRITICAL,
            estimated_duration=timedelta(hours=1),
            dependencies={"task1", "task2"},
            deadline=datetime(2024, 1, 1, 17, 0)
        )
    ]
    
    # Add and schedule tasks
    for task in tasks:
        scheduler.add_task(task)
        slot = scheduler.schedule_task(task.id)
        if slot:
            print(f"Scheduled {task.name} at {slot.start}")
        else:
            print(f"Could not schedule {task.name}")

if __name__ == "__main__":
    main()
