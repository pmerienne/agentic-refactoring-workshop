from task_flow_api.model import Task
from datetime import datetime, timedelta
from enum import Enum


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNDEFINED = "undefined"


class TaskRulesEngine:
    # Magic numbers replaced with named constants
    HIGH_PRIORITY_DUE_DAYS = 1
    URGENT_ADDITIONAL_DAYS = -1
    MEDIUM_PRIORITY_DUE_DAYS = 3
    LOW_PRIORITY_DUE_DAYS = 30

    # Keyword mappings for priority detection
    PRIORITY_KEYWORDS = {
        Priority.HIGH: ["urgent", "asap", "critical"],
        Priority.MEDIUM: ["important", "priority"],
    }

    # Keyword mappings for tag detection
    TAG_KEYWORDS = {
        "bug": ["bug", "fix", "error"],
        "feature": ["feature", "new", "add"],
        "refactoring": ["refactor", "improve", "clean"],
        "testing": ["test", "qa"],
        "documentation": ["doc", "documentation"],
    }

    def post_process(self, task: Task) -> str:
        priority = self._determine_priority(task)
        due_date = self._calculate_due_date(priority, task)
        tags = self._extract_tags(task, priority)
        self._trigger_actions(task, priority)
        return self._generate_report(priority, due_date, tags)

    def _get_normalized_description(self, task: Task) -> str:
        """Extract and normalize task description to avoid duplication."""
        return task.description.lower() if task.description else ""

    def _determine_priority(self, task: Task) -> Priority:
        """Determine task priority based on description keywords."""
        if not task.description:
            return Priority.UNDEFINED

        desc_lower = self._get_normalized_description(task)

        for priority, keywords in self.PRIORITY_KEYWORDS.items():
            if any(keyword in desc_lower for keyword in keywords):
                return priority

        return Priority.LOW

    def _calculate_due_date(self, priority: Priority, task: Task) -> datetime:
        """Calculate due date based on priority and urgency keywords."""
        if priority == Priority.HIGH:
            due_date = datetime.now() + timedelta(days=self.HIGH_PRIORITY_DUE_DAYS)
            desc_lower = self._get_normalized_description(task)
            if any(
                keyword in desc_lower
                for keyword in self.PRIORITY_KEYWORDS[Priority.HIGH]
            ):
                due_date = due_date + timedelta(days=self.URGENT_ADDITIONAL_DAYS)
            return due_date
        elif priority == Priority.MEDIUM:
            return datetime.now() + timedelta(days=self.MEDIUM_PRIORITY_DUE_DAYS)
        else:
            return datetime.now() + timedelta(days=self.LOW_PRIORITY_DUE_DAYS)

    def _extract_tags(self, task: Task, priority: Priority) -> list[str]:
        """Extract tags from task description based on keywords."""
        tags = []

        if not task.description:
            return tags

        desc_lower = self._get_normalized_description(task)

        for tag, keywords in self.TAG_KEYWORDS.items():
            if any(keyword in desc_lower for keyword in keywords):
                tags.append(tag)

        tags.append(priority.value)
        return tags

    def _trigger_actions(self, task: Task, priority: Priority) -> None:
        """Trigger appropriate actions based on task priority."""
        if priority == Priority.HIGH:
            self._book_appointment(task)
            self._notify_users(task)
        elif priority == Priority.MEDIUM:
            self._notify_users(task)
        elif priority == Priority.LOW:
            self._log_task(task)

    def _generate_report(
        self, priority: Priority, due_date: datetime, tags: list[str]
    ) -> str:
        """Generate a summary report of task processing."""
        if priority == Priority.UNDEFINED:
            report = "NO PRIO"
        else:
            report = f"Prio: {priority.value}"

        report += f"\nDue to: {due_date}"

        if tags:
            report += f"\nTags: {', '.join(tags)}"

        return report

    def _book_appointment(self, task: Task):
        print(f"Booked appointment for {task.id}")

    def _notify_users(self, task: Task):
        print(f"Notifying users for {task.id}")

    def _log_task(self, task: Task):
        print(f"Logging {task.id}")
