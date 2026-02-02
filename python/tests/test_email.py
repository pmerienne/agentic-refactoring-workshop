import pytest
from unittest.mock import Mock, patch
from task_flow_api.email import TaskEmailingPipeline, EmailDecisionReport
from task_flow_api.model import Task, TaskStatus


class TestEmailDecisionReport:
    """Tests for EmailDecisionReport class focusing on magic number edge cases."""

    def test_notify_score_exactly_at_threshold_no_warnings(self):
        """Score exactly at 0.7 threshold with no warnings should not notify."""
        report = EmailDecisionReport("Task is fine", score=0.7)
        assert report.notify(0.7, 0.7) is False

    def test_notify_score_just_above_threshold_no_warnings(self):
        """Score just above 0.7 threshold should notify."""
        report = EmailDecisionReport("Task is fine", score=0.71)
        risk_factor = 0.71  # no warnings
        # risk_factor (0.71) > threshold (0.7)
        assert report.notify(0.71, 0.7) is True

    def test_notify_score_just_below_threshold_no_warnings(self):
        """Score just below 0.7 threshold should not notify."""
        report = EmailDecisionReport("Task is fine", score=0.69)
        assert report.notify(0.69, 0.7) is False

    def test_warnings_exactly_at_boundary_three_warnings(self):
        """Exactly 3 warnings should not trigger urgent action."""
        report = EmailDecisionReport("prio prio prio", score=0.5)
        assert report.warnings == 3

    def test_warnings_exactly_above_boundary_four_warnings(self):
        """Exactly 4 warnings should trigger urgent action (warnings > 3)."""
        report = EmailDecisionReport("prio prio prio prio", score=0.5)
        assert report.warnings == 4

    def test_warnings_count_bug_keyword(self):
        """Bug keyword should contribute to warning count."""
        report = EmailDecisionReport("bug bug", score=0.5)
        assert report.warnings == 2

    def test_warnings_count_mixed_keywords(self):
        """Mixed prio and bug keywords should sum correctly."""
        report = EmailDecisionReport("prio bug prio bug", score=0.5)
        assert report.warnings == 4

    def test_interaction_threshold_score_with_three_warnings(self):
        """Score at threshold (0.7) with exactly 3 warnings."""
        report = EmailDecisionReport("prio prio prio", score=0.7)
        # risk_factor = 0.7 * (1 + 3 * 0.1) = 0.7 * 1.3 = 0.91
        # 0.91 > 0.7, so should notify
        assert report.notify(0.7, 0.7) is True

    def test_interaction_threshold_score_with_four_warnings(self):
        """Score at threshold (0.7) with exactly 4 warnings."""
        report = EmailDecisionReport("prio prio prio prio", score=0.7)
        # risk_factor = 0.7 * (1 + 4 * 0.1) = 0.7 * 1.4 = 0.98
        # 0.98 > 0.7, so should notify
        assert report.notify(0.7, 0.7) is True

    def test_interaction_below_threshold_with_warnings_amplifies_risk(self):
        """Score below threshold but warnings amplify risk above threshold."""
        report = EmailDecisionReport("prio prio prio prio prio", score=0.6)
        # risk_factor = 0.6 * (1 + 5 * 0.1) = 0.6 * 1.5 = 0.9
        # 0.9 > 0.7, so should notify
        assert report.notify(0.6, 0.7) is True

    def test_approved_overrides_notification(self):
        """Approved status should prevent notification even above threshold."""
        report = EmailDecisionReport("Task approved", score=0.9)
        assert report.approved is True
        assert report.notify(0.9, 0.7) is False

    def test_critical_flag_detection(self):
        """Critical keyword should set critic flag."""
        report = EmailDecisionReport("This is CRITICAL", score=0.5)
        assert report.critic is True


class TestTaskEmailingPipeline:
    """Tests for TaskEmailingPipeline focusing on magic number edge cases."""

    @pytest.fixture
    def pipeline(self):
        return TaskEmailingPipeline()

    @pytest.fixture
    def sample_task(self):
        return Task(
            id=1,
            title="Test Task",
            description="Test description",
            status=TaskStatus.TODO,
            completed=False
        )

    def test_send_emails_score_exactly_at_threshold(self, pipeline, sample_task):
        """Score exactly at 0.7 threshold without warnings or critic flag."""
        with patch.object(pipeline.rules_engine, 'post_process', return_value="Task is fine"):
            with patch.object(pipeline.scoring_service, 'compute_score', return_value=0.7):
                with patch.object(pipeline, '_notify_by_email') as mock_notify:
                    pipeline.send_emails(sample_task)
                    # Score at 0.7 with no warnings: risk_factor = 0.7 * 1 = 0.7
                    # 0.7 is not > 0.7, so should not notify
                    mock_notify.assert_not_called()

    def test_send_emails_score_just_above_threshold(self, pipeline, sample_task):
        """Score just above 0.7 threshold should trigger notification."""
        with patch.object(pipeline.rules_engine, 'post_process', return_value="Task is fine"):
            with patch.object(pipeline.scoring_service, 'compute_score', return_value=0.71):
                with patch.object(pipeline, '_notify_by_email') as mock_notify:
                    pipeline.send_emails(sample_task)
                    mock_notify.assert_called_once()
                    assert "ATTENTION REQUIRED" in mock_notify.call_args[0][0]
                    assert ['team@example.com'] == mock_notify.call_args[0][2]

    def test_send_emails_exactly_three_warnings(self, pipeline, sample_task):
        """Exactly 3 warnings should not trigger urgent action (needs > 3)."""
        with patch.object(pipeline.rules_engine, 'post_process', return_value="prio prio prio"):
            with patch.object(pipeline.scoring_service, 'compute_score', return_value=0.5):
                with patch.object(pipeline, '_notify_by_email') as mock_notify:
                    pipeline.send_emails(sample_task)
                    # 3 warnings: risk_factor = 0.5 * 1.3 = 0.65, not > 0.7
                    # warnings = 3, not > 3
                    # no critic flag
                    mock_notify.assert_not_called()

    def test_send_emails_exactly_four_warnings(self, pipeline, sample_task):
        """Exactly 4 warnings should trigger urgent action (warnings > 3)."""
        with patch.object(pipeline.rules_engine, 'post_process', return_value="prio prio prio prio"):
            with patch.object(pipeline.scoring_service, 'compute_score', return_value=0.5):
                with patch.object(pipeline, '_notify_by_email') as mock_notify:
                    pipeline.send_emails(sample_task)
                    mock_notify.assert_called_once()
                    assert "URGENT" in mock_notify.call_args[0][0]
                    assert 'manager@example.com' in mock_notify.call_args[0][2]

    def test_send_emails_interaction_threshold_score_with_three_warnings(self, pipeline, sample_task):
        """Score at 0.7 with exactly 3 warnings should notify but not urgent."""
        with patch.object(pipeline.rules_engine, 'post_process', return_value="prio prio prio"):
            with patch.object(pipeline.scoring_service, 'compute_score', return_value=0.7):
                with patch.object(pipeline, '_notify_by_email') as mock_notify:
                    pipeline.send_emails(sample_task)
                    # risk_factor = 0.7 * 1.3 = 0.91 > 0.7, so notify
                    # warnings = 3, not > 3, so not urgent
                    mock_notify.assert_called_once()
                    assert "ATTENTION REQUIRED" in mock_notify.call_args[0][0]
                    assert ['team@example.com'] == mock_notify.call_args[0][2]

    def test_send_emails_interaction_threshold_score_with_four_warnings(self, pipeline, sample_task):
        """Score at 0.7 with exactly 4 warnings should trigger urgent notification."""
        with patch.object(pipeline.rules_engine, 'post_process', return_value="prio prio prio prio"):
            with patch.object(pipeline.scoring_service, 'compute_score', return_value=0.7):
                with patch.object(pipeline, '_notify_by_email') as mock_notify:
                    pipeline.send_emails(sample_task)
                    # risk_factor = 0.7 * 1.4 = 0.98 > 0.7, so notify
                    # warnings = 4 > 3, so urgent
                    mock_notify.assert_called_once()
                    assert "URGENT" in mock_notify.call_args[0][0]
                    assert 'manager@example.com' in mock_notify.call_args[0][2]

    def test_send_emails_critical_flag_triggers_urgent(self, pipeline, sample_task):
        """Critical flag should trigger urgent action regardless of warnings."""
        with patch.object(pipeline.rules_engine, 'post_process', return_value="This is CRITICAL"):
            with patch.object(pipeline.scoring_service, 'compute_score', return_value=0.5):
                with patch.object(pipeline, '_notify_by_email') as mock_notify:
                    pipeline.send_emails(sample_task)
                    mock_notify.assert_called_once()
                    assert "URGENT" in mock_notify.call_args[0][0]
                    assert 'manager@example.com' in mock_notify.call_args[0][2]

    def test_send_emails_below_threshold_no_warnings_no_email(self, pipeline, sample_task):
        """Score below threshold with no warnings should not send email."""
        with patch.object(pipeline.rules_engine, 'post_process', return_value="All good"):
            with patch.object(pipeline.scoring_service, 'compute_score', return_value=0.5):
                with patch.object(pipeline, '_notify_by_email') as mock_notify:
                    pipeline.send_emails(sample_task)
                    mock_notify.assert_not_called()
