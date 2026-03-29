from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_marks_status_true() -> None:
    task = Task(description="Give medicine", estimated_minutes=5)

    task.mark_complete()

    assert task.completed is True


def test_adding_task_to_pet_increases_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Evening walk", estimated_minutes=20))

    assert len(pet.tasks) == initial_count + 1


def test_sort_by_time_orders_hhmm_values() -> None:
    owner = Owner(name="Jordan")
    pet = owner.create_pet(name="Mochi", species="dog")
    today = date.today()

    pet.create_task(description="Late task", estimated_minutes=10, time="18:00", due_date=today)
    pet.create_task(description="Early task", estimated_minutes=10, time="08:00", due_date=today)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(scheduler.tasks_for_day(today))

    assert [task.description for task in sorted_tasks] == ["Early task", "Late task"]


def test_filter_tasks_by_pet_name_and_completion() -> None:
    owner = Owner(name="Jordan")
    dog = owner.create_pet(name="Mochi", species="dog")
    cat = owner.create_pet(name="Luna", species="cat")
    today = date.today()

    mochi_task = dog.create_task(description="Walk", estimated_minutes=20, due_date=today)
    cat.create_task(description="Litter", estimated_minutes=10, due_date=today)
    mochi_task.mark_complete()

    scheduler = Scheduler(owner=owner)
    filtered = scheduler.filter_tasks(completed=True, pet_name="Mochi")

    assert len(filtered) == 1
    assert filtered[0].description == "Walk"


def test_mark_task_complete_spawns_next_daily_instance() -> None:
    owner = Owner(name="Jordan")
    pet = owner.create_pet(name="Mochi", species="dog")
    today = date.today()

    task = pet.create_task(
        description="Morning walk",
        estimated_minutes=20,
        frequency="daily",
        due_date=today,
    )

    scheduler = Scheduler(owner=owner)
    scheduler.mark_task_complete(task.task_id)

    tomorrow_tasks = scheduler.tasks_for_day(today + timedelta(days=1))
    assert any(t.description == "Morning walk" for t in tomorrow_tasks)


def test_detect_time_conflicts_returns_warning_message() -> None:
    owner = Owner(name="Jordan")
    dog = owner.create_pet(name="Mochi", species="dog")
    cat = owner.create_pet(name="Luna", species="cat")
    today = date.today()

    dog.create_task(description="Walk", estimated_minutes=20, time="09:00", due_date=today)
    cat.create_task(description="Feeding", estimated_minutes=10, time="09:00", due_date=today)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_time_conflicts(day=today)

    assert len(warnings) == 1
    assert "Conflict at 09:00" in warnings[0]


def test_tasks_for_day_with_no_tasks_returns_empty_list() -> None:
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)

    assert scheduler.tasks_for_day(date.today()) == []


def test_build_daily_schedule_respects_time_limit() -> None:
    owner = Owner(name="Jordan")
    pet = owner.create_pet(name="Mochi", species="dog")
    today = date.today()

    pet.create_task(description="Walk", estimated_minutes=30, time="08:00", due_date=today)
    pet.create_task(description="Feed", estimated_minutes=10, time="09:00", due_date=today)

    scheduler = Scheduler(owner=owner)
    schedule = scheduler.build_daily_schedule(day=today, time_available_minutes=20)

    assert len(schedule) == 1
    assert schedule[0].description == "Feed"


def test_mark_task_complete_weekly_spawns_next_week() -> None:
    owner = Owner(name="Jordan")
    pet = owner.create_pet(name="Luna", species="cat")
    today = date.today()

    task = pet.create_task(
        description="Grooming",
        estimated_minutes=15,
        frequency="weekly",
        due_date=today,
    )

    scheduler = Scheduler(owner=owner)
    scheduler.mark_task_complete(task.task_id)

    next_week_tasks = scheduler.tasks_for_day(today + timedelta(days=7))
    assert any(t.description == "Grooming" for t in next_week_tasks)


def test_mark_task_complete_one_time_does_not_spawn_new_task() -> None:
    owner = Owner(name="Jordan")
    pet = owner.create_pet(name="Mochi", species="dog")
    today = date.today()

    task = pet.create_task(
        description="Vet visit",
        estimated_minutes=60,
        frequency="once",
        due_date=today,
    )

    scheduler = Scheduler(owner=owner)
    scheduler.mark_task_complete(task.task_id)

    tomorrow_tasks = scheduler.tasks_for_day(today + timedelta(days=1))
    assert tomorrow_tasks == []


def test_detect_time_conflicts_without_collision_returns_empty() -> None:
    owner = Owner(name="Jordan")
    dog = owner.create_pet(name="Mochi", species="dog")
    cat = owner.create_pet(name="Luna", species="cat")
    today = date.today()

    dog.create_task(description="Walk", estimated_minutes=20, time="09:00", due_date=today)
    cat.create_task(description="Feed", estimated_minutes=10, time="09:30", due_date=today)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_time_conflicts(day=today)

    assert warnings == []
