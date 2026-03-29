from datetime import date, timedelta

from pawpal_system import Owner, Scheduler


def print_schedule(title: str, schedule_tasks: list) -> None:
    """Print a clean terminal view of a task list."""
    print(f"\n{title}")
    print("-" * 50)

    if not schedule_tasks:
        print("No tasks found.")
        return

    total_minutes = 0
    for index, task in enumerate(schedule_tasks, start=1):
        total_minutes += task.estimated_minutes
        print(
            f"{index}. {task.description:<22} "
            f"@ {task.time:<5} "
            f"pet={task.pet_name or 'Unknown':<8} "
            f"({task.estimated_minutes:>3} min) "
            f"priority={task.priority:<6} "
            f"freq={task.frequency:<7} "
            f"done={task.completed}"
        )

    print("-" * 50)
    print(f"Total planned time: {total_minutes} minutes")


def main() -> None:
    owner = Owner(name="Jordan")

    dog = owner.create_pet(name="Mochi", species="dog", age=3)
    cat = owner.create_pet(name="Luna", species="cat", age=5)

    today = date.today()

    dog.create_task(
        description="Morning walk",
        estimated_minutes=25,
        time="18:00",
        frequency="daily",
        priority="high",
        due_date=today,
    )
    dog.create_task(
        description="Dinner feeding",
        estimated_minutes=10,
        time="08:00",
        frequency="daily",
        priority="medium",
        due_date=today,
    )
    cat.create_task(
        description="Litter cleanup",
        estimated_minutes=15,
        time="08:00",
        frequency="daily",
        priority="high",
        due_date=today,
    )
    cat.create_task(
        description="Brush coat",
        estimated_minutes=12,
        time="12:30",
        frequency="weekly",
        priority="low",
        due_date=today,
    )

    scheduler = Scheduler(owner=owner)
    unsorted_today_tasks = scheduler.tasks_for_day(today)
    sorted_today_tasks = scheduler.sort_by_time(unsorted_today_tasks)
    filtered_mochi_tasks = scheduler.filter_tasks(completed=False, pet_name="Mochi")
    today_schedule = scheduler.build_daily_schedule(day=today)
    warnings = scheduler.detect_time_conflicts(day=today)

    print_schedule(f"Insertion Order Tasks for {owner.name}", unsorted_today_tasks)
    print_schedule(f"Time-Sorted Tasks for {owner.name}", sorted_today_tasks)
    print_schedule("Filtered Tasks (Mochi, incomplete)", filtered_mochi_tasks)
    print_schedule("Today's Built Schedule", today_schedule)

    if warnings:
        print("\nConflict Warnings")
        print("-" * 50)
        for warning in warnings:
            print(f"- {warning}")

    first_task = sorted_today_tasks[0]
    scheduler.mark_task_complete(first_task.task_id)
    tomorrow_tasks = scheduler.tasks_for_day(today + timedelta(days=1))

    print_schedule(
        "Recurring Task Check (Tomorrow)",
        tomorrow_tasks,
    )


if __name__ == "__main__":
    main()
