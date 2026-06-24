# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Some core actions a user should be able to perform is  adding a pet, scheduling a walk, and viewing today's tasks. The user should also be able to track all the care tasks for their pet like walks, feeding, meds, enrichment, and grooming. In the app constraints should also be visible like time available, priority, and owner preferences. 

-> Class Owner will holds the owner’s name, available time, preferences, pets, and tasks.
-> Class Pet will stores each pet’s name, species, age, notes, and its care tasks.
-> Class Task will represents one care activity with duration, priority, category, recurrence, and optional pet association.
-> Class Scheduler will builds the daily plan from owner tasks, sorting and filtering by time and priority.
-> Class DailyPlan/ScheduleItem will capture the final schedule and explain why each task was chosen and when it happens.
This model will keeps the system focused on pets and their care tasks, while separating scheduling logic from the data model.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. I made a few design adjustments after reviewing the implementation needs:
- Replaced Task.pet_name with a direct Task.pet reference. This strengthens relationships and makes it easier for the scheduler to access pet attributes when planning.
- Switched Task.priority from a string to a numeric priority_score to simplify sorting and comparison logic.
- Centralized task ownership on the Owner (Owner.tasks is the canonical list). Pet no longer stores tasks directly; instead Pet.get_tasks(owner) filters the owner's tasks. This avoids duplication while still supporting both single- and multi-pet scenarios.
- Changed ScheduleItem start/end times to use datetime objects for precise arithmetic and calendar-like scheduling.
- Added placeholders for recurrence, dependencies, and conflict handling in the scheduler as future work.

I made these changes to reduce duplication, make scheduling arithmetic straightforward, and prepare the model for multi-pet scheduling and conflict checks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
