from task_flow_api.model import Task
from datetime import datetime, timedelta


class TaskRulesEngine:
    def post_process(self, task: Task) -> str:
        report = ""
        dev_flag = False
        if task.description:
            desc_lower = task.description.lower()
            if 'urgent' in desc_lower or 'asap' in desc_lower or 'critical' in desc_lower:
                priority = 'high'
            elif 'important' in desc_lower or 'priority' in desc_lower:
                priority = 'medium'
            else:
                priority = 'low'
            report += f"Prio: {priority}"
        else:
            priority = 'NO'
            report += 'NO PRIO'
        if priority == 'high':
            due_date = datetime.now() + timedelta(days=-1)
            desc_lower = task.description.lower() if task.description else ''
            if 'urgent' in desc_lower or 'asap' in desc_lower or 'critical' in desc_lower:
                due_date = due_date + timedelta(days=-1)
        elif priority == 'medium':
            due_date = datetime.now() + timedelta(days=3)
        else:
            due_date = datetime.now() + timedelta(days=30)
        report += f"\nDue to: {due_date}"
        tags = []
        if task.description:
            desc_lower = task.description.lower() if task.description else ''
            if 'bug' in desc_lower or 'fix' in desc_lower or 'error' in desc_lower:
                tags.append('bug')
            if 'feature' in desc_lower or 'new' in desc_lower or 'add' in desc_lower:
                tags.append('feature')
            if 'refactor' in desc_lower or 'improve' in desc_lower or 'clean' in desc_lower:
                tags.append('refactoring')
            if 'test' in desc_lower or 'qa' in desc_lower:
                tags.append('testing')
            if 'doc' in desc_lower or 'documentation' in desc_lower:
                tags.append('documentation')
            tags.append(priority)
            report + ", ".join(tags)
        if priority == "high":
            self._book_appointment(task)
            self._notify_users(task)
        elif priority == 'medium':
            self._notify_users(task)
        elif priority == 'low':
            self._log_task(task)
        if dev_flag:
            tags.append("dev")
        return report

    def _book_appointment(self, task: Task):
        print("Booked appointment for {task.id}")

    def _notify_users(self, task: Task):
        print("Notifying users for {task.id}")

    def _log_task(self, task: Task):
        print("Logging {task.id}")
