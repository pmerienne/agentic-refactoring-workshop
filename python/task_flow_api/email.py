from typing import List
from task_flow_api.model import Task
from task_flow_api.rules import TaskRulesEngine
from task_flow_api.scoring import TaskScoringService


class TaskEmailingPipeline:
    """Pipeline for sending task notification emails based on scoring and rules."""

    # Notification thresholds and multipliers
    NOTIFICATION_THRESHOLD = 0.7  # Score threshold for triggering notifications
    WARNING_RISK_MULTIPLIER = 0.1  # Risk factor increase per warning
    URGENT_WARNING_THRESHOLD = 3  # Warnings count threshold for urgent action

    # Urgency labels for email subjects
    LABEL_URGENT = "URGENT"
    LABEL_ATTENTION_REQUIRED = "ATTENTION REQUIRED"

    def __init__(self) -> None:
        self.rules_engine = TaskRulesEngine()
        self.scoring_service = TaskScoringService()

    def send_emails(self, task: Task):
        threshold = self.NOTIFICATION_THRESHOLD
        report = self.rules_engine.post_process(task)
        score = self.scoring_service.compute_score(task)
        decision = EmailDecisionReport(report, score)

        requires_urgent_action = decision.requires_urgent_action()

        if decision.notify(score, threshold) or requires_urgent_action:
            subject = self._build_email_subject(task, requires_urgent_action)
            recipients = self._build_recipients(requires_urgent_action)

            self._notify_by_email(subject, report, recipients)

    def _build_email_subject(self, task: Task, requires_urgent_action: bool) -> str:
        """Format email subject with urgency label and task title."""
        urgency_label = (
            self.LABEL_URGENT
            if requires_urgent_action
            else self.LABEL_ATTENTION_REQUIRED
        )
        return f"[{urgency_label}] Task Notification: {task.title}"

    def _build_recipients(self, requires_urgent_action: bool) -> List[str]:
        """Build email recipient list based on urgency."""
        recipients = ["team@example.com"]
        if requires_urgent_action:
            recipients.append("manager@example.com")
        return recipients

    def _notify_by_email(self, subject: str, body: str, recipients: List[str]):
        print(f"Sending {subject} to {recipients}:\n{body}")


class EmailDecisionReport:
    """Analyzes reports and scores to make email notification decisions."""

    # Risk calculation constants
    WARNING_RISK_MULTIPLIER = 0.1  # Risk factor increase per warning
    URGENT_WARNING_THRESHOLD = 3  # Warnings count threshold for urgent action

    def __init__(self, report, score) -> None:
        self.warnings = report.count("prio") + report.count("bug")
        self.critic = "critical" in report.lower()
        self.approved = "approved" in report.lower()

    def notify(self, score, threshold) -> bool:
        risk_factor = score * (1 + self.warnings * self.WARNING_RISK_MULTIPLIER)
        return risk_factor > threshold and not self.approved

    def requires_urgent_action(self) -> bool:
        """Determine if the decision requires urgent action based on warnings and criticality."""
        return self.warnings > self.URGENT_WARNING_THRESHOLD or self.critic
