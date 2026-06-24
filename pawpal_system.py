from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority_score: int = 1
    category: Optional[str] = None
    recurring: bool = False
    pet: Optional["Pet"] = None
    notes: Optional[str] = None
    dependencies: List["Task"] = field(default_factory=list)

    def estimate_effort(self) -> int:
        return int(self.duration_minutes)

    def is_high_priority(self) -> bool:
        return self.priority_score >= 8

    def summary(self) -> str:
        return f"{self.title} ({self.duration_minutes}m, priority={self.priority_score})"


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    notes: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass

    def get_care_summary(self) -> str:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int = 480
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def get_available_time(self) -> int:
        pass

    def get_preferred_tasks(self) -> List[Task]:
        pass


@dataclass
class ScheduleItem:
    task: Task
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    reason: Optional[str] = None

    def format_entry(self) -> str:
        pass


@dataclass
class DailyPlan:
    date: date
    items: List[ScheduleItem] = field(default_factory=list)
    total_duration: int = 0

    def add_item(self, item: ScheduleItem) -> None:
        pass

    def get_summary(self) -> str:
        pass

    def get_reasoning(self) -> str:
        pass


class Scheduler:
    def generate_daily_plan(self, owner: Owner, plan_date: date) -> DailyPlan:
        pass

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def filter_tasks_by_time(self, tasks: List[Task], available_minutes: int) -> List[Task]:
        pass

    def explain_plan(self, plan: DailyPlan) -> str:
        pass
