from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority_score: int = 5
    category: Optional[str] = None
    recurring: Optional[str] = None  # e.g., 'daily', 'weekly'
    pet: Optional["Pet"] = None
    notes: Optional[str] = None
    dependencies: List["Task"] = field(default_factory=list)
    completed: bool = False
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None

    def estimate_effort(self) -> int:
        return int(self.duration_minutes)

    def mark_complete(self) -> None:
        self.completed = True

    def is_high_priority(self) -> bool:
        return self.priority_score >= 8

    def schedule_at(self, start: datetime) -> None:
        self.scheduled_start = start
        self.scheduled_end = start + timedelta(minutes=self.duration_minutes)

    def summary(self) -> str:
        status = "done" if self.completed else "pending"
        pet_name = self.pet.name if self.pet else "(no pet)"
        return f"{self.title} [{pet_name}] — {self.duration_minutes}m — p={self.priority_score} — {status}"


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    notes: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task, owner: Optional["Owner"] = None) -> None:
        task.pet = self
        if task not in self.tasks:
            self.tasks.append(task)
        if owner is not None:
            owner.add_task(task)

    def get_tasks(self) -> List[Task]:
        return list(self.tasks)

    def get_care_summary(self) -> str:
        return f"{self.name} the {self.species} (age={self.age}) — {len(self.tasks)} tasks"


@dataclass
class Owner:
    name: str
    available_minutes: int = 480
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        if task not in self.tasks:
            self.tasks.append(task)
        if task.pet and task.pet not in self.pets:
            self.pets.append(task.pet)
        # keep pet mirror in sync
        if task.pet and task not in task.pet.tasks:
            task.pet.tasks.append(task)

    def get_available_time(self) -> int:
        return int(self.available_minutes)

    def get_preferred_tasks(self) -> List[Task]:
        preferred = []
        for t in self.tasks:
            if t.category and self.preferences.get(t.category) == "prefer":
                preferred.append(t)
        return preferred

    def get_all_tasks(self) -> List[Task]:
        # Return unique tasks known to the owner (include pet lists to be safe)
        seen = set()
        result: List[Task] = []
        for t in self.tasks:
            if id(t) not in seen:
                seen.add(id(t))
                result.append(t)
        for p in self.pets:
            for t in p.tasks:
                if id(t) not in seen:
                    seen.add(id(t))
                    result.append(t)
        return result


@dataclass
class ScheduleItem:
    task: Task
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    reason: Optional[str] = None

    def format_entry(self) -> str:
        s = self.start_time.strftime("%H:%M") if self.start_time else ""
        e = self.end_time.strftime("%H:%M") if self.end_time else ""
        return f"{s} — {e}: {self.task.summary()} {f'({self.reason})' if self.reason else ''}"


@dataclass
class DailyPlan:
    date: date
    items: List[ScheduleItem] = field(default_factory=list)
    total_duration: int = 0

    def add_item(self, item: ScheduleItem) -> None:
        self.items.append(item)
        if item.task and item.task.duration_minutes:
            self.total_duration += int(item.task.duration_minutes)

    def get_summary(self) -> str:
        if not self.items:
            return "No scheduled items."
        lines = [item.format_entry() for item in self.items]
        return "\n".join(lines)

    def get_reasoning(self) -> str:
        return "Tasks selected by priority and available time; conflict checks and recurrence are placeholders."


class Scheduler:
    def generate_daily_plan(
        self,
        owner: Owner,
        plan_date: date,
        day_start: time = time(8, 0),
        day_end: time = time(20, 0),
    ) -> DailyPlan:
        plan = DailyPlan(date=plan_date)

        start_dt = datetime.combine(plan_date, day_start)
        end_dt = datetime.combine(plan_date, day_end)
        remaining_minutes = owner.get_available_time()

        tasks = [t for t in owner.get_all_tasks() if not t.completed]
        tasks = self.sort_tasks(tasks)

        current = start_dt
        for t in tasks:
            duration_td = timedelta(minutes=t.duration_minutes)
            if current + duration_td > end_dt:
                # no more room in the day
                continue
            if t.duration_minutes > remaining_minutes:
                continue

            # schedule task
            t.schedule_at(current)
            item = ScheduleItem(task=t, start_time=current, end_time=current + duration_td)
            plan.add_item(item)
            current = current + duration_td
            remaining_minutes -= t.duration_minutes

        return plan

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        # Higher priority first, then shorter duration
        return sorted(tasks, key=lambda t: (-t.priority_score, t.duration_minutes))

    def filter_tasks_by_time(self, tasks: List[Task], available_minutes: int) -> List[Task]:
        selected: List[Task] = []
        total = 0
        for t in tasks:
            if total + t.duration_minutes <= available_minutes:
                selected.append(t)
                total += t.duration_minutes
        return selected

    def explain_plan(self, plan: DailyPlan) -> str:
        return plan.get_reasoning()
