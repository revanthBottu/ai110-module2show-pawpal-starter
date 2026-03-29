import streamlit as st
from datetime import date

from pawpal_system import Owner, Scheduler


def _pet_name_for_task(owner: Owner, task_id: str) -> str:
    """Return the pet name that owns a task id."""
    for pet in owner.pets:
        for task in pet.tasks:
            if task.task_id == task_id:
                return pet.name
    return "Unknown"

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
owner_preference = st.text_input(
    "Owner preference (optional)",
    value="prioritize essentials first",
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)

owner: Owner = st.session_state.owner
owner.name = owner_name
owner.preferences["planning_preference"] = owner_preference

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    clean_name = pet_name.strip()
    if not clean_name:
        st.warning("Please enter a pet name.")
    else:
        existing = next(
            (
                pet
                for pet in owner.pets
                if pet.name.lower() == clean_name.lower() and pet.species == species
            ),
            None,
        )
        active_pet = existing or owner.create_pet(name=clean_name, species=species)
        st.session_state.active_pet_id = active_pet.pet_id
        st.success(f"Active pet: {active_pet.name} ({active_pet.species})")

if owner.pets:
    pet_labels = [f"{pet.name} ({pet.species})" for pet in owner.pets]
    pet_ids = [pet.pet_id for pet in owner.pets]

    default_index = 0
    active_pet_id = st.session_state.get("active_pet_id")
    if active_pet_id in pet_ids:
        default_index = pet_ids.index(active_pet_id)

    selected_pet_label = st.selectbox("Active pet", options=pet_labels, index=default_index)
    selected_index = pet_labels.index(selected_pet_label)
    st.session_state.active_pet_id = pet_ids[selected_index]
else:
    st.info("No pets yet. Add a pet to begin.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    task_time = st.text_input("Task time (HH:MM)", value="09:00")
with col5:
    task_frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], index=0)

if st.button("Add task"):
    active_pet = owner.get_pet(st.session_state.get("active_pet_id", ""))
    clean_title = task_title.strip()
    if active_pet is None:
        st.warning("Please add/select a pet before adding tasks.")
    elif not clean_title:
        st.warning("Please enter a task title.")
    else:
        active_pet.create_task(
            description=clean_title,
            estimated_minutes=int(duration),
            time=task_time,
            frequency=task_frequency,
            priority=priority,
            due_date=date.today(),
        )
        st.success(f"Added task to {active_pet.name}: {clean_title}")

active_pet = owner.get_pet(st.session_state.get("active_pet_id", ""))

if active_pet and active_pet.tasks:
    st.write(f"Current tasks for {active_pet.name}:")
    st.table(
        [
            {
                "description": task.description,
                "duration_minutes": task.estimated_minutes,
                "time": task.time,
                "priority": task.priority,
                "frequency": task.frequency,
                "completed": task.completed,
            }
            for task in active_pet.tasks
        ]
    )
elif active_pet:
    st.info(f"No tasks yet for {active_pet.name}. Add one above.")

if owner.pets:
    st.caption("Pets in current session")
    st.table(
        [
            {
                "name": pet.name,
                "species": pet.species,
                "task_count": len(pet.tasks),
            }
            for pet in owner.pets
        ]
    )

st.divider()

st.subheader("Build Schedule")
st.caption("Build a daily plan from all pets' incomplete tasks.")

scheduler = Scheduler(owner=owner)
strategy = st.selectbox(
    "Schedule strategy",
    ["time-first", "priority-first"],
    index=0,
)

filter_status = st.selectbox("Task filter status", ["all", "pending", "completed"], index=0)
pet_filter_options = ["all"] + [pet.name for pet in owner.pets]
filter_pet = st.selectbox("Task filter pet", pet_filter_options, index=0)

if filter_status == "pending":
    filtered_tasks = scheduler.filter_tasks(completed=False, pet_name=None if filter_pet == "all" else filter_pet)
elif filter_status == "completed":
    filtered_tasks = scheduler.filter_tasks(completed=True, pet_name=None if filter_pet == "all" else filter_pet)
else:
    if filter_pet == "all":
        filtered_tasks = scheduler.get_all_tasks()
    else:
        filtered_tasks = scheduler.filter_tasks(pet_name=filter_pet)

if filtered_tasks:
    st.write("Filtered tasks")
    st.table(
        [
            {
                "task": task.description,
                "pet": task.pet_name,
                "time": task.time,
                "duration_minutes": task.estimated_minutes,
                "priority": task.priority,
                "frequency": task.frequency,
                "completed": task.completed,
            }
            for task in scheduler.sort_by_time(filtered_tasks)
        ]
    )

time_available = st.number_input(
    "Time available today (minutes)", min_value=10, max_value=600, value=120, step=5
)

if st.button("Generate schedule"):
    if strategy == "priority-first":
        today_schedule = scheduler.build_daily_schedule_with_priority(
            day=date.today(), time_available_minutes=int(time_available)
        )
    else:
        today_schedule = scheduler.build_daily_schedule(
            day=date.today(), time_available_minutes=int(time_available)
        )

    warnings = scheduler.detect_time_conflicts(day=date.today())
    for warning in warnings:
        st.warning(warning)

    if not today_schedule:
        st.info("No pending tasks fit today's schedule yet.")
    else:
        st.write("Today's Schedule")
        st.table(
            [
                {
                    "task": task.description,
                    "pet": _pet_name_for_task(owner, task.task_id),
                    "time": task.time,
                    "duration_minutes": task.estimated_minutes,
                    "priority": task.priority,
                }
                for task in today_schedule
            ]
        )

        total_minutes = sum(task.estimated_minutes for task in today_schedule)
        st.success(
            f"Plan created with {len(today_schedule)} task(s), using {total_minutes} / {int(time_available)} minutes."
        )
        st.caption(
            f"Why this plan: strategy={strategy}, only incomplete tasks due today were considered, and your preference is '{owner.preferences.get('planning_preference', 'none')}'."
        )
