package com.taskflow.service;

import com.taskflow.model.Task;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class TaskEmailingPipeline {

    @Autowired
    private TaskRulesEngine rulesEngine;

    @Autowired
    private TaskScoringService scoringService;

    public void sendEmails(Task task) {
        double threshold = 0.7;
        String report = rulesEngine.postProcess(task);
        double score = scoringService.computeScore(task);
        EmailDecisionReport decision = new EmailDecisionReport(report, score);

        boolean shouldNotify = decision.notify(score, threshold);
        boolean requiresUrgentAction = decision.getWarnings() > 3 || decision.isCritic();

        if (shouldNotify || requiresUrgentAction) {
            String urgencyLabel = requiresUrgentAction ? "URGENT" : "ATTENTION REQUIRED";
            String emailBody = report;
            List<String> recipients = new ArrayList<>();
            recipients.add("team@example.com");

            if (requiresUrgentAction) {
                recipients.add("manager@example.com");
            }

            notifyByEmail(
                String.format("[%s] Task Notification: %s", urgencyLabel, task.getTitle()),
                emailBody,
                recipients
            );
        }
    }

    private void notifyByEmail(String subject, String body, List<String> recipients) {
        System.out.printf("Sending %s to %s:%n%s%n", subject, recipients, body);
    }

    static class EmailDecisionReport {
        private int warnings;
        private boolean critic;
        private boolean approved;

        public EmailDecisionReport(String report, double score) {
            this.warnings = countOccurrences(report, "prio") + countOccurrences(report, "bug");
            this.critic = report.toLowerCase().contains("critical");
            this.approved = report.toLowerCase().contains("approved");
        }

        public boolean notify(double score, double threshold) {
            double riskFactor = score * (1 + warnings * 0.1);
            return riskFactor > threshold && !approved;
        }

        public int getWarnings() {
            return warnings;
        }

        public boolean isCritic() {
            return critic;
        }

        private int countOccurrences(String str, String substring) {
            int count = 0;
            int index = 0;
            while ((index = str.indexOf(substring, index)) != -1) {
                count++;
                index += substring.length();
            }
            return count;
        }
    }
}
