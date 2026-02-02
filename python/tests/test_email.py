import pytest
from task_flow_api.email import EmailDecisionReport, TaskEmailingPipeline
from task_flow_api.model import Task


class TestEmailDecisionReport:
    """Tests for urgency determination logic in EmailDecisionReport"""

    def test_requires_urgent_action_when_warnings_exceed_threshold(self):
        """Should require urgent action when warnings > 3"""
        # Arrange: Create a report with 4 warnings (exceeds threshold of 3)
        report = "prio prio prio prio"  # 4 occurrences of 'prio'
        decision = EmailDecisionReport(report, score=0.5)
        
        # Act & Assert
        assert decision.warnings == 4
        assert decision.requires_urgent_action() is True

    def test_requires_urgent_action_when_critical(self):
        """Should require urgent action when report contains 'critical'"""
        # Arrange: Create a report with critical issue
        report = "This is a critical issue"
        decision = EmailDecisionReport(report, score=0.5)
        
        # Act & Assert
        assert decision.critic is True
        assert decision.requires_urgent_action() is True

    def test_no_urgent_action_when_warnings_at_threshold(self):
        """Should not require urgent action when warnings == 3 (at threshold)"""
        # Arrange: Create a report with exactly 3 warnings
        report = "prio prio prio"  # 3 occurrences of 'prio'
        decision = EmailDecisionReport(report, score=0.5)
        
        # Act & Assert
        assert decision.warnings == 3
        assert decision.requires_urgent_action() is False

    def test_no_urgent_action_when_low_warnings_and_not_critical(self):
        """Should not require urgent action when warnings <= 3 and not critical"""
        # Arrange: Create a report with 2 warnings and no critical marker
        report = "prio prio"  # 2 occurrences of 'prio'
        decision = EmailDecisionReport(report, score=0.5)
        
        # Act & Assert
        assert decision.warnings == 2
        assert decision.critic is False
        assert decision.requires_urgent_action() is False

    def test_requires_urgent_action_with_both_conditions(self):
        """Should require urgent action when both warnings > 3 AND critical"""
        # Arrange: Create a report with many warnings AND critical marker
        report = "prio prio prio prio critical issue"
        decision = EmailDecisionReport(report, score=0.5)
        
        # Act & Assert
        assert decision.warnings == 4
        assert decision.critic is True
        assert decision.requires_urgent_action() is True

    def test_warnings_count_includes_bug_mentions(self):
        """Should count both 'prio' and 'bug' in warnings"""
        # Arrange: Create a report with 2 'prio' and 2 'bug' mentions
        report = "prio bug prio bug"
        decision = EmailDecisionReport(report, score=0.5)
        
        # Act & Assert
        assert decision.warnings == 4
        assert decision.requires_urgent_action() is True


class TestEmailDecisionNotify:
    """Tests for notification decision logic with threshold and risk calculation"""

    def test_notify_when_score_exceeds_threshold_no_warnings(self):
        """Should notify when score (0.8) > threshold (0.7) with no warnings"""
        # Arrange: score=0.8, no warnings, not approved
        report = "Some issue here"
        decision = EmailDecisionReport(report, score=0.8)
        
        # Act: risk_factor = 0.8 * (1 + 0 * 0.1) = 0.8
        # threshold = 0.7, so 0.8 > 0.7 and not approved
        result = decision.notify(score=0.8, threshold=0.7)
        
        # Assert
        assert result is True

    def test_notify_when_score_below_threshold_but_warnings_push_over(self):
        """Should notify when warnings increase risk_factor above threshold"""
        # Arrange: score=0.65, 1 warning (prio), not approved
        report = "prio issue"
        decision = EmailDecisionReport(report, score=0.65)
        
        # Act: risk_factor = 0.65 * (1 + 1 * 0.1) = 0.65 * 1.1 = 0.715
        # threshold = 0.7, so 0.715 > 0.7 and not approved
        result = decision.notify(score=0.65, threshold=0.7)
        
        # Assert
        assert decision.warnings == 1
        assert result is True

    def test_no_notify_when_score_below_threshold(self):
        """Should not notify when score < threshold with no warnings"""
        # Arrange: score=0.6, no warnings, not approved
        report = "Some minor issue"
        decision = EmailDecisionReport(report, score=0.6)
        
        # Act: risk_factor = 0.6 * (1 + 0 * 0.1) = 0.6
        # threshold = 0.7, so 0.6 < 0.7
        result = decision.notify(score=0.6, threshold=0.7)
        
        # Assert
        assert result is False

    def test_no_notify_when_approved(self):
        """Should not notify when task is approved regardless of score"""
        # Arrange: score=0.9, no warnings, but approved
        report = "approved for deployment"
        decision = EmailDecisionReport(report, score=0.9)
        
        # Act: risk_factor = 0.9 * (1 + 0 * 0.1) = 0.9
        # threshold = 0.7, so 0.9 > 0.7 BUT approved
        result = decision.notify(score=0.9, threshold=0.7)
        
        # Assert
        assert decision.approved is True
        assert result is False

    def test_risk_factor_multiplier_calculation(self):
        """Should apply 0.1 multiplier per warning to risk calculation"""
        # Arrange: score=0.5, 2 warnings (prio + bug)
        report = "prio bug issue"
        decision = EmailDecisionReport(report, score=0.5)
        
        # Act: risk_factor = 0.5 * (1 + 2 * 0.1) = 0.5 * 1.2 = 0.6
        # threshold = 0.7, so 0.6 < 0.7
        result = decision.notify(score=0.5, threshold=0.7)
        
        # Assert
        assert decision.warnings == 2
        assert result is False

    def test_risk_factor_with_many_warnings(self):
        """Should correctly apply multiplier with multiple warnings"""
        # Arrange: score=0.6, 4 warnings
        report = "prio prio bug bug"
        decision = EmailDecisionReport(report, score=0.6)
        
        # Act: risk_factor = 0.6 * (1 + 4 * 0.1) = 0.6 * 1.4 = 0.84
        # threshold = 0.7, so 0.84 > 0.7 and not approved
        result = decision.notify(score=0.6, threshold=0.7)
        
        # Assert
        assert decision.warnings == 4
        assert result is True

    def test_threshold_boundary_just_below(self):
        """Should not notify when risk_factor equals threshold (edge case)"""
        # Arrange: score=0.7, no warnings
        report = "Some issue"
        decision = EmailDecisionReport(report, score=0.7)
        
        # Act: risk_factor = 0.7 * (1 + 0 * 0.1) = 0.7
        # threshold = 0.7, so 0.7 == 0.7 (not greater)
        result = decision.notify(score=0.7, threshold=0.7)
        
        # Assert
        assert result is False


class TestMagicNumberBehavior:
    """Integration tests to lock down magic number behavior before refactoring"""

    def test_threshold_value_0_7_in_notify_method(self):
        """Verify that 0.7 threshold is used in notify calculation"""
        # Test exact boundary: score = 0.7, risk_factor = 0.7 (equals threshold, should NOT notify)
        report = "some issue"
        decision = EmailDecisionReport(report, score=0.7)
        assert decision.notify(score=0.7, threshold=0.7) is False
        
        # Test just above: score = 0.71, risk_factor = 0.71 (above threshold, should notify)
        decision2 = EmailDecisionReport(report, score=0.71)
        assert decision2.notify(score=0.71, threshold=0.7) is True

    def test_multiplier_value_0_1_per_warning(self):
        """Verify that 0.1 multiplier per warning is applied correctly"""
        # Base: score=0.5, warnings=0, risk_factor = 0.5 * (1 + 0*0.1) = 0.5
        report = "issue"
        decision = EmailDecisionReport(report, score=0.5)
        assert decision.warnings == 0
        assert decision.notify(score=0.5, threshold=0.7) is False
        
        # With 3 warnings: risk_factor = 0.5 * (1 + 3*0.1) = 0.5 * 1.3 = 0.65 (still below 0.7)
        report2 = "prio prio prio"
        decision2 = EmailDecisionReport(report2, score=0.5)
        assert decision2.warnings == 3
        assert decision2.notify(score=0.5, threshold=0.7) is False
        
        # With 5 warnings: risk_factor = 0.5 * (1 + 5*0.1) = 0.5 * 1.5 = 0.75 (above 0.7)
        report3 = "prio prio prio bug bug"
        decision3 = EmailDecisionReport(report3, score=0.5)
        assert decision3.warnings == 5
        assert decision3.notify(score=0.5, threshold=0.7) is True

    def test_urgent_threshold_value_3_warnings(self):
        """Verify that warnings > 3 triggers urgent action"""
        # At threshold: warnings = 3 should NOT trigger urgent
        report = "prio prio prio"
        decision = EmailDecisionReport(report, score=0.5)
        assert decision.warnings == 3
        assert decision.requires_urgent_action() is False
        
        # Above threshold: warnings = 4 should trigger urgent
        report2 = "prio prio prio prio"
        decision2 = EmailDecisionReport(report2, score=0.5)
        assert decision2.warnings == 4
        assert decision2.requires_urgent_action() is True


class TestTaskEmailingPipeline:
    """Tests for recipient building logic in TaskEmailingPipeline"""

    def test_build_recipients_normal_notification(self):
        """Should return only team email for normal notifications"""
        # Arrange
        pipeline = TaskEmailingPipeline()
        
        # Act
        recipients = pipeline._build_recipients(requires_urgent_action=False)
        
        # Assert
        assert recipients == ['team@example.com']

    def test_build_recipients_urgent_notification(self):
        """Should return team and manager emails for urgent notifications"""
        # Arrange
        pipeline = TaskEmailingPipeline()
        
        # Act
        recipients = pipeline._build_recipients(requires_urgent_action=True)
        
        # Assert
        assert recipients == ['team@example.com', 'manager@example.com']

    def test_format_email_subject_with_urgent_label(self):
        """Should format subject with URGENT label when urgent action required"""
        # Arrange
        pipeline = TaskEmailingPipeline()
        task = Task(id=1, title="Fix critical bug", description="Bug in production", status="TODO")
        
        # Act
        subject = pipeline._format_email_subject(task, requires_urgent_action=True)
        
        # Assert
        assert subject == "[URGENT] Task Notification: Fix critical bug"

    def test_format_email_subject_with_attention_required_label(self):
        """Should format subject with ATTENTION REQUIRED label for normal notifications"""
        # Arrange
        pipeline = TaskEmailingPipeline()
        task = Task(id=2, title="Update documentation", description="Docs need updating", status="TODO")
        
        # Act
        subject = pipeline._format_email_subject(task, requires_urgent_action=False)
        
        # Assert
        assert subject == "[ATTENTION REQUIRED] Task Notification: Update documentation"

    def test_format_email_subject_includes_task_title(self):
        """Should include task title in the subject line"""
        # Arrange
        pipeline = TaskEmailingPipeline()
        task = Task(id=3, title="Review pull request", description="PR needs review", status="TODO")
        
        # Act
        urgent_subject = pipeline._format_email_subject(task, requires_urgent_action=True)
        normal_subject = pipeline._format_email_subject(task, requires_urgent_action=False)
        
        # Assert
        assert "Review pull request" in urgent_subject
        assert "Review pull request" in normal_subject
