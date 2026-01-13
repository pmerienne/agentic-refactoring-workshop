from typing import List
from task_flow_api.model import Task
from task_flow_api.rules import TaskRulesEngine
from task_flow_api.scoring import TaskScoringService


class TaskEmailingPipeline:
    def __init__(self) -> None:
        self.rules_engine = TaskRulesEngine()
        self.scoring_service = TaskScoringService()

    def send_emails(self, task: Task):
        threshold = 0.7
        report = self.rules_engine.post_process(task)
        score = self.scoring_service.compute_score(task)
        decision = EmailDecisionReport(report, score)

        should_notify = decision.notify(score, threshold)
        requires_urgent_action = decision.warnings > 3 or decision.critic

        if should_notify or requires_urgent_action:
            urgency_label = "URGENT" if requires_urgent_action else "ATTENTION REQUIRED"
            email_body = report
            recipients = ['team@example.com']

            if requires_urgent_action:
                recipients.append('manager@example.com')

            self._notify_by_email(
                f"[{urgency_label}] Task Notification: {task.title}",
                email_body,
                recipients
            )

    def _notify_by_email(self, object: str, body: str, recipients: List[str]):
        print(f'Sending {object} to {recipients}:\n{body}')


class EmailDecisionReport:
    def __init__(self, report, score) -> None:
        self.warnings = report.count('prio') + report.count('bug')
        self.critic = 'critical' in report.lower()
        self.approved = 'approved' in report.lower()

    def notify(self, score, threshold) -> bool:
        risk_factor = score * (1 + self.warnings * 0.1)
        return risk_factor > threshold and not self.approved
