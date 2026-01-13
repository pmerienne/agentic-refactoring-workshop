package com.taskflow.service;

import com.taskflow.model.Task;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class TaskRulesEngine {
    
    public String postProcess(Task task) {
        StringBuilder report = new StringBuilder();
        boolean devFlag = false;
        String priority;
        if (task.getDescription() != null) {
            String descLower = task.getDescription().toLowerCase();
            if (descLower.contains("urgent") || descLower.contains("asap") || descLower.contains("critical")) {
                priority = "high";
            } else if (descLower.contains("important") || descLower.contains("priority")) {
                priority = "medium";
            } else {
                priority = "low";
            }
            report.append("Prio: ").append(priority);
        } else {
            priority = "NO";
            report.append("NO PRIO");
        }
        LocalDateTime dueDate;
        if (priority.equals("high")) {
            dueDate = LocalDateTime.now().minusDays(1);
            String descLower = task.getDescription() != null ? task.getDescription().toLowerCase() : "";
            if (descLower.contains("urgent") || descLower.contains("asap") || descLower.contains("critical")) {
                dueDate = dueDate.minusDays(1);
            }
        } else if (priority.equals("medium")) {
            dueDate = LocalDateTime.now().plusDays(3);
        } else {
            dueDate = LocalDateTime.now().plusDays(30);
        }
        report.append("\nDue to: ").append(dueDate);
        List<String> tags = new ArrayList<>();
        if (task.getDescription() != null) {
            String descLower = task.getDescription() != null ? task.getDescription().toLowerCase() : "";
            if (descLower.contains("bug") || descLower.contains("fix") || descLower.contains("error")) {
                tags.add("bug");
            }
            if (descLower.contains("feature") || descLower.contains("new") || descLower.contains("add")) {
                tags.add("feature");
            }
            if (descLower.contains("refactor") || descLower.contains("improve") || descLower.contains("clean")) {
                tags.add("refactoring");
            }
            if (descLower.contains("test") || descLower.contains("qa")) {
                tags.add("testing");
            }
            if (descLower.contains("doc") || descLower.contains("documentation")) {
                tags.add("documentation");
            }
            tags.add(priority);
            report.append(String.join(", ", tags));
        }
        if (priority.equals("high")) {
            bookAppointment(task);
            notifyUsers(task);
        } else if (priority.equals("medium")) {
            notifyUsers(task);
        } else if (priority.equals("low")) {
            logTask(task);
        }
        if (devFlag) {
            tags.add("dev");
            task.setUpdatedAt(LocalDateTime.now());
        }
        
        return report.toString();
    }
    
    private void bookAppointment(Task task) {
        System.out.println("Booked appointment for {task.id}");
    }
    
    private void notifyUsers(Task task) {
        System.out.println("Notifying users for {task.id}");
    }
    
    private void logTask(Task task) {
        System.out.println("Logging {task.id}");
    }
}
