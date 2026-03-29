# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features

- Task tracking across multiple pets with description, time, duration, priority, and recurrence.
- Daily schedule generation with a configurable time budget.
- Two scheduling strategies: time-first and priority-first.
- Task filtering by pet and completion status.
- Conflict warnings for exact-time collisions.
- Recurring task rollover for daily and weekly tasks after completion.

## Testing PawPal+

Run the automated suite:

```bash
python -m pytest
```

What the tests cover:

- Core task behavior (completion toggles, task addition to pets).
- Sorting correctness (chronological `HH:MM` ordering).
- Recurrence logic (daily and weekly next-instance creation).
- Conflict detection (warnings for duplicate times, no-warning case).
- Edge cases (owner with no tasks, schedule constrained by time budget, non-recurring completion behavior).

Confidence Level: ★★★★☆ (4/5)

The suite exercises critical scheduler flows and key edge cases. Remaining risk is mainly around richer overlap detection and advanced preference optimization.

## 📸 Demo

Add your final Streamlit screenshot using the required embed format:

<a href="/course_images/ai110/pawpal_demo.png" target="_blank"><img src='/course_images/ai110/pawpal_demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Final UML

The finalized class diagram source is stored in `uml_final.mmd`.