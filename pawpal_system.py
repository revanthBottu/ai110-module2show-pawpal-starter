from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List
from uuid import uuid4


_PRIORITY_SCORE = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """Represent one pet-care activity with scheduling details."""

    description: str
    estimated_minutes: int
    frequency: str = "daily"
    priority: str = "medium"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    task_id: str = field(default_factory=lambda: str(uuid4()))

    def mark_complete(self) -> None:
        """Set this task status to completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Set this task status to incomplete."""
        self.completed = False


@dataclass
class Pet:
    """Store pet profile data and that pet's care tasks."""

    name: str
    species: str
    age: int = 0
    pet_id: str = field(default_factory=lambda: str(uuid4()))
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> Task:
        """Add one task to this pet and return it."""
        self.tasks.append(task)
        return task

    def create_task(
        self,
        description: str,
        estimated_minutes: int,
        frequency: str = "daily",
        priority: str = "medium",
        due_date: date | None = None,
    ) -> Task:
        """Create and add a task using simple input values."""
        task = Task(
            description=description,
            estimated_minutes=estimated_minutes,
            frequency=frequency,
            priority=priority,
            due_date=due_date or date.today(),
        )
        return self.add_task(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by id and return whether removal succeeded."""
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[index]
                return True
        return False

    def pending_tasks(self) -> List[Task]:
        """Return all tasks that are not yet completed."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Represent an owner account with multiple pets."""

    name: str
    owner_id: str = field(default_factory=lambda: str(uuid4()))
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> Pet:
        """Attach one pet to this owner and return it."""
        if pet not in self.pets:
            self.pets.append(pet)
        return pet

    def create_pet(self, name: str, species: str, age: int = 0) -> Pet:
        """Create a pet, add it to this owner, and return it."""
        return self.add_pet(Pet(name=name, species=species, age=age))

    def remove_pet(self, pet_id: str) -> bool:
        """Remove a pet by id and return whether removal succeeded."""
        for index, pet in enumerate(self.pets):
            if pet.pet_id == pet_id:
                del self.pets[index]
                return True
        return False

    def get_pet(self, pet_id: str) -> Pet | None:
        """Find and return a pet by id, or None if missing."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def all_tasks(self) -> List[Task]:
        """Return a flattened list of tasks across every owned pet."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


@dataclass
class Scheduler:
    """Retrieve and organize tasks across all of an owner's pets."""

    owner: Owner

    def get_all_tasks(self) -> List[Task]:
        """Return every task available through the linked owner."""
        return self.owner.all_tasks()

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across the owner's pets."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def tasks_for_day(self, day: date | None = None) -> List[Task]:
        """Return pending tasks that match the selected day."""
        target_day = day or date.today()
        return [task for task in self.get_pending_tasks() if task.due_date == target_day]

    def build_daily_schedule(
        self,
        day: date | None = None,
        time_available_minutes: int | None = None,
    ) -> List[Task]:
        """Build a priority-ordered daily schedule within an optional time limit."""
        candidates = self.tasks_for_day(day)
        candidates.sort(
            key=lambda task: (_PRIORITY_SCORE.get(task.priority, 0), -task.estimated_minutes),
            reverse=True,
        )

        if time_available_minutes is None:
            return candidates

        selected: List[Task] = []
        used_minutes = 0
        for task in candidates:
            if used_minutes + task.estimated_minutes <= time_available_minutes:
                selected.append(task)
                used_minutes += task.estimated_minutes
        return selected

    def mark_task_complete(self, task_id: str) -> bool:
        """Mark a task complete by id and report success."""
        for task in self.get_all_tasks():
            if task.task_id == task_id:
                task.mark_complete()
                return True
        return False
