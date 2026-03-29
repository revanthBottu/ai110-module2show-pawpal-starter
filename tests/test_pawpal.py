from pawpal_system import Pet, Task


def test_task_completion_marks_status_true() -> None:
    task = Task(description="Give medicine", estimated_minutes=5)

    task.mark_complete()

    assert task.completed is True


def test_adding_task_to_pet_increases_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Evening walk", estimated_minutes=20))

    assert len(pet.tasks) == initial_count + 1
