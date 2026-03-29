from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple
from uuid import uuid4


_PRIORITY_SCORE = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """Represent one pet-care activity with scheduling details."""

    description: str
    estimated_minutes: int
    time: str = "09:00"
    frequency: str = "daily"
    priority: str = "medium"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: Optional[str] = None
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
        task.pet_name = self.name
        self.tasks.append(task)
        return task

    def create_task(
        self,
        description: str,
        estimated_minutes: int,
        time: str = "09:00",
        frequency: str = "daily",
        priority: str = "medium",
        due_date: date | None = None,
    ) -> Task:
        """Create and add a task using simple input values."""
        task = Task(
            description=description,
            estimated_minutes=estimated_minutes,
            time=time,
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

    def sort_by_time(self, tasks: List[Task] | None = None) -> List[Task]:
        """Return tasks sorted by HH:MM time using a lambda key."""
        source = tasks if tasks is not None else self.get_pending_tasks()
        return sorted(source, key=lambda task: task.time)

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> List[Task]:
        """Filter tasks by optional completion status and pet name."""
        tasks = self.get_all_tasks()

        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        if pet_name is not None:
            target_pet = pet_name.strip().lower()
            tasks = [
                task
                for task in tasks
                if (task.pet_name or "").strip().lower() == target_pet
            ]

        return tasks

    def build_daily_schedule(
        self,
        day: date | None = None,
        time_available_minutes: int | None = None,
    ) -> List[Task]:
        """Build a time-sorted daily schedule within an optional time limit."""
        candidates = self.sort_by_time(self.tasks_for_day(day))

        if time_available_minutes is None:
            return candidates

        selected: List[Task] = []
        used_minutes = 0
        for task in candidates:
            if used_minutes + task.estimated_minutes <= time_available_minutes:
                selected.append(task)
                used_minutes += task.estimated_minutes
        return selected

    def detect_time_conflicts(self, day: date | None = None) -> List[str]:
        """Detect exact HH:MM collisions and return warning messages."""
        target_day = day or date.today()
        day_tasks = self.tasks_for_day(target_day)
        tasks_by_time: Dict[str, List[Task]] = defaultdict(list)

        for task in day_tasks:
            tasks_by_time[task.time].append(task)

        warnings: List[str] = []
        for time in sorted(tasks_by_time):
            tasks = tasks_by_time[time]
            if len(tasks) > 1:
                labels = ", ".join(
                    f"{task.description} ({task.pet_name or 'Unknown pet'})"
                    for task in tasks
                )
                warnings.append(f"Conflict at {time}: {labels}")

        return warnings

    def _find_pet_and_task(self, task_id: str) -> Tuple[Pet, Task] | Tuple[None, None]:
        """Locate and return the owning pet and task for a task id."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.task_id == task_id:
                    return pet, task
        return None, None

    def _next_due_date(self, task: Task) -> date | None:
        """Compute next due date for supported recurring frequencies."""
        frequency = task.frequency.strip().lower()
        if frequency == "daily":
            return task.due_date + timedelta(days=1)
        if frequency == "weekly":
            return task.due_date + timedelta(days=7)
        return None

    def _spawn_recurring_task(self, pet: Pet, task: Task) -> None:
        """Create the next task instance when a recurring task is completed."""
        next_due = self._next_due_date(task)
        if next_due is None:
            return

        pet.create_task(
            description=task.description,
            estimated_minutes=task.estimated_minutes,
            time=task.time,
            frequency=task.frequency,
            priority=task.priority,
            due_date=next_due,
        )

    def mark_task_complete(self, task_id: str) -> bool:
        """Mark a task complete and spawn the next recurring instance if needed."""
        pet, task = self._find_pet_and_task(task_id)
        if pet is None or task is None:
            return False

        task.mark_complete()
        self._spawn_recurring_task(pet, task)
        return True

    def build_daily_schedule_with_priority(
        self,
        day: date | None = None,
        time_available_minutes: int | None = None,
    ) -> List[Task]:
        """Build a priority-first schedule and break ties by task time."""
        candidates = self.tasks_for_day(day)
        candidates = sorted(
            candidates,
            key=lambda task: (-_PRIORITY_SCORE.get(task.priority, 0), task.time),
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
