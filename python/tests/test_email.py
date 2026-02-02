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
