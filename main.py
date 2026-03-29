from datetime import date

from pawpal_system import Owner, Scheduler


def print_schedule(owner_name: str, schedule_tasks: list) -> None:
    """Print a clean terminal view of today's pet-care schedule."""
    print(f"\nToday's Schedule for {owner_name}")
    print("-" * 50)

    if not schedule_tasks:
        print("No tasks scheduled for today.")
        return

    total_minutes = 0
    for index, task in enumerate(schedule_tasks, start=1):
        total_minutes += task.estimated_minutes
        print(
            f"{index}. {task.description:<22} "
            f"({task.estimated_minutes:>3} min) "
            f"priority={task.priority:<6} "
            f"freq={task.frequency}"
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
        frequency="daily",
        priority="high",
        due_date=today,
    )
    dog.create_task(
        description="Dinner feeding",
        estimated_minutes=10,
        frequency="daily",
        priority="medium",
        due_date=today,
    )
    cat.create_task(
        description="Litter cleanup",
        estimated_minutes=15,
        frequency="daily",
        priority="high",
        due_date=today,
    )

    scheduler = Scheduler(owner=owner)
    today_schedule = scheduler.build_daily_schedule(day=today)

    print_schedule(owner.name, today_schedule)


if __name__ == "__main__":
    main()
