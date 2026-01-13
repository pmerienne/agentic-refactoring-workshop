package com.taskflow.service;

import com.taskflow.model.Task;
import com.taskflow.model.TaskStatus;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class TaskScoringService {
    
    private static final Map<TaskStatus, Integer> STATUS_BASE_SCORES = new HashMap<>();
    
    static {
        STATUS_BASE_SCORES.put(TaskStatus.TODO, 100);
        STATUS_BASE_SCORES.put(TaskStatus.DOING, 250);
        STATUS_BASE_SCORES.put(TaskStatus.DONE, 500);
        STATUS_BASE_SCORES.put(TaskStatus.ARCHIVED, -50);
    }
    
    private static final List<String> URGENT_KEYWORDS = Arrays.asList(
        "urgent", "asap", "critical", "emergency", "now", "immediately"
    );
    
    private static final List<String> PRIORITY_KEYWORDS = Arrays.asList(
        "important", "priority", "high", "crucial", "vital"
    );
    
    private static final List<String> COMPLEXITY_KEYWORDS = Arrays.asList(
        "complex", "difficult", "challenging", "hard", "tricky"
    );
    
    private static final List<String> TECH_KEYWORDS = Arrays.asList(
        "bug", "fix", "refactor", "optimize", "performance", "security"
    );
    
    private static final List<String> BUSINESS_KEYWORDS = Arrays.asList(
        "revenue", "customer", "client", "deadline", "meeting"
    );
    
    private static final List<String> NEGATIVE_KEYWORDS = Arrays.asList(
        "maybe", "later", "consider", "think", "discuss", "review"
    );
    
    private static final List<String> FORBIDDEN_KEYWORDS = Arrays.asList(
        "impossible", "cannot", "blocked", "waiting", "postpone"
    );
    
    
    public double computeScore(Task task) {
        double score = 0.0;
        score += STATUS_BASE_SCORES.getOrDefault(task.getStatus(), 0);
        
        if (task.getStatus() == TaskStatus.DONE && task.isCompleted()) {
            score *= 1.5;
        } else if (task.getStatus() == TaskStatus.DONE && !task.isCompleted()) {
            score *= 0.3;
        } else if (task.getStatus() != TaskStatus.DONE && task.isCompleted()) {
            score *= 0.5;
        }
        
        // Combine title and description for analysis
        String text = (task.getTitle() + " " + task.getDescription()).toLowerCase();
        
        // Count various keyword categories
        int urgentCount = countKeywords(text, URGENT_KEYWORDS);
        int priorityCount = countKeywords(text, PRIORITY_KEYWORDS);
        int complexityCount = countKeywords(text, COMPLEXITY_KEYWORDS);
        int techCount = countKeywords(text, TECH_KEYWORDS);
        int businessCount = countKeywords(text, BUSINESS_KEYWORDS);
        int negativeCount = countKeywords(text, NEGATIVE_KEYWORDS);
        int forbiddenCount = countKeywords(text, FORBIDDEN_KEYWORDS);
        
        // Urgent keywords add exponential score
        if (urgentCount > 0) {
            score += Math.pow(urgentCount, 2) * 75;
        }
        
        // Priority keywords multiply by Fibonacci-ish sequence
        if (priorityCount > 0) {
            int[] fibonacciLike = {1, 1, 2, 3, 5, 8, 13};
            int multiplier = fibonacciLike[Math.min(priorityCount - 1, fibonacciLike.length - 1)];
            score *= (1 + multiplier * 0.1);
        }
        
        // Complexity increases score
        if (complexityCount > 0) {
            score += complexityCount * 120;
        }
        
        // Tech keywords have diminishing returns
        if (techCount > 0) {
            score += 200.0 / (1 + techCount);  // More keywords = less value each
        }
        
        // Business keywords interact with status
        if (businessCount > 0) {
            if (task.getStatus() == TaskStatus.DOING) {
                score += businessCount * 150;
            } else if (task.getStatus() == TaskStatus.TODO) {
                score += businessCount * 80;
            } else {
                score += businessCount * 30;
            }
        }
        
        // Negative keywords are multiplicative penalties
        if (negativeCount > 0) {
            score *= Math.pow(0.7, negativeCount);  // Each negative word reduces by 30%
        }
        
        // Forbidden keywords have severe impact
        if (forbiddenCount > 0) {
            score -= forbiddenCount * 300;
            if (forbiddenCount >= 3) {
                score *= 0.1;  // Catastrophic penalty
            }
        }
        
        int textLength = text.length();
        if (textLength < 20) {
            score *= 0.6;  // Too short, probably not serious
        } else if (textLength > 500) {
            score *= 0.8;  // Too long, probably rambling
        } else if (textLength >= 50 && textLength <= 200) {
            score *= 1.3;  // Sweet spot
        }
        
        // Special character analysis
        Pattern specialCharsPattern = Pattern.compile("[!@#$%^&*()]");
        Matcher matcher = specialCharsPattern.matcher(text);
        int specialChars = 0;
        while (matcher.find()) {
            specialChars++;
        }
        
        if (specialChars > 5 && specialChars <= 10) {
            score += specialChars * 15;  // Emphasis matters
        } else if (specialChars > 10) {
            score *= 0.7;  // Too many, seems spammy
        }
        
        // Final adjustment: ensure score is at least -1000 and at most 10000
        score = Math.max(-1000, Math.min(10000, score));
        return Math.round(score * 100.0) / 100.0;
    }
    
    /**
     * Count how many times any of the keywords appear in the text.
     */
    private int countKeywords(String text, List<String> keywords) {
        int count = 0;
        for (String keyword : keywords) {
            Pattern pattern = Pattern.compile("\\b" + Pattern.quote(keyword) + "\\b");
            Matcher matcher = pattern.matcher(text);
            while (matcher.find()) {
                count++;
            }
        }
        return count;
    }
}
