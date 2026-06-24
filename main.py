from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name='Jordan', available_minutes=300)

    pet1 = Pet(name='Mochi', species='dog', age=3)
    pet2 = Pet(name='Biscuit', species='cat', age=5)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    t1 = Task(title='Morning walk', duration_minutes=30, priority_score=9, pet=pet1)
    t2 = Task(title='Feeding Mochi', duration_minutes=10, priority_score=10, pet=pet1)
    t3 = Task(title='Play session', duration_minutes=20, priority_score=7, pet=pet2)
    t4 = Task(title='Grooming Biscuit', duration_minutes=25, priority_score=6, pet=pet2)

    owner.add_task(t1)
    owner.add_task(t2)
    owner.add_task(t3)
    owner.add_task(t4)

    sched = Scheduler()
    plan = sched.generate_daily_plan(owner, date.today(), day_start=time(8, 0), day_end=time(18, 0))

    print(f"Today's Schedule for {owner.name} ({date.today()}):")
    print(plan.get_summary())
    print('\nTotal duration:', plan.total_duration)
    print('\nReasoning:', sched.explain_plan(plan))


if __name__ == '__main__':
    main()
