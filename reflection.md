# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

1. The user should be able to clearly define their schedule to the assistant easily so that assistant can give the best plan possible.
2. Should return an simple and readable to-do list for pet care
3. Should allow configuration of feeding and other tasks so that owners who want more or less regular timings for some tasks can achieve those.

Initial UML classes:

Owner - the user(needs to hold attributes such as an array of pets, a personal schedule object), needs to be able to own and interact with Pet objects and their schedules
Pet - user's objects linked to their account - have attributes like Tasks and Schedule
Events - objects linked to Pet and Owner - attributes like estimated time to complete, boolean for completed or not, etc.
Schedule - object linked to specific Pet and Owner(Pets may have same Schedule) -  attributes like Events array, needs to display and organize events for every day.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers time, priority of task, and the needs of the individual pet. I put the pet's needs and the priority of the task as what mattered most so that the scheduler could make sure the user gets those done for sure in their schedule, boosting the utility of the app.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler uses exact matches for conflict detection instead of checking overlapping from tasks.
This is a tradeoff because it is simple and prone to edge cases, but it's still catching the most obvious collisions for a planning app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used it for refactoring and brainstorming the design mostly, giving the chatbot the ideas and the design and letting it do error-free syntax.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

For my scheduler, I wanted to make sure the method used was correct, so I reviewed what Copilot proposed and compared it to what my priorities were in making this project, and what the consumer wants. Against this, I made changes to ensure I get the job done right.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested that the scheduler could schedule tasks based on priority, get the optimal amount of tasks in, and take the user's inputs into consideration. These tests are important because the user needs those functions as the core of the project, and it needs to be personalizable.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm probably about 86% confident. I would probably test more overlapping schedules, where no task may fit without overlapping. This would force the scheduler to try and minimize or eliminate overlap.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I was satisfied with how the scheduler turned out. It works well, and I even managed to get it working for some edge cases.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would probably make the UI cleaner, redesign it from scratch to look like a real company.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Presentation is something AI cannot do on its own. When building the UI with AI, it often looked messy or unprofessional without more detailed guidance. In the future, I would start my prompts more strongly detailed to get the look I want.
