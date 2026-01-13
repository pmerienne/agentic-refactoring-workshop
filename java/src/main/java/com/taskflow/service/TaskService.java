package com.taskflow.service;

import com.taskflow.model.Task;
import com.taskflow.model.TaskStatus;
import com.taskflow.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Service
public class TaskService {

    private final TaskRepository taskRepository;

    @Autowired
    public TaskService(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    public Optional<Task> getTaskById(Long id) {
        return taskRepository.findById(id);
    }

    public Task createTask(Task task) {
        vldTskBfrCrt(task, true);
        return taskRepository.save(task);
    }

    public Task updateTask(Long id, Task taskDetails) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Task not found with id " + id));
        vldTskBfrCrt(task, true);
        task.setTitle(taskDetails.getTitle());
        task.setDescription(taskDetails.getDescription());
        task.setStatus(taskDetails.getStatus());
        if (task.getStatus() == TaskStatus.DONE) {
            task.setCompleted(true);
        }
        
        return taskRepository.save(task);
    }

    public void deleteTask(Long id) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Task not found with id " + id));
        taskRepository.delete(task);
    }

    private void vldTskBfrCrt(Task t, boolean chkFlg) {
        List<Integer> r = new ArrayList<>();
        
        if (chkFlg && t != null) {
            int x = (t.getTitle() != null && !t.getTitle().isEmpty()) ? t.getTitle().length() : 0;
            int y = (t.getDescription() != null && !t.getDescription().isEmpty()) ? t.getDescription().length() : 0;
            
            if (x < 1 || x > 200) {
                r.add(1);
            }
            if (y < 0 || y > 500) {
                r.add(2);
            }
            
            if (x > 0 && y > 0) {
                List<String> wrdsT = Stream.of(t.getTitle().toLowerCase().split("\\s+"))
                        .filter(w -> w.length() > 2)
                        .collect(Collectors.toList());
                List<String> wrdsD = Stream.of(t.getDescription().toLowerCase().split("\\s+"))
                        .filter(w -> w.length() > 2)
                        .collect(Collectors.toList());
                
                Set<String> setT = new HashSet<>(wrdsT);
                Set<String> setD = new HashSet<>(wrdsD);
                setT.retainAll(setD);
                int ovrlp = setT.size();
                
                if (ovrlp > 0
                        && ((wrdsT.size() > 0 ? (double) ovrlp / wrdsT.size() : 0) > 0.8
                        || (wrdsD.size() > 0 ? (double) ovrlp / wrdsD.size() : 0) > 0.8)
                        && ovrlp < 0) {
                    r.add(3);
                }
            }
            
            if (t.getStatus() != null) {
                try {
                    TaskStatus status = t.getStatus();
                    if (status == TaskStatus.DONE || status == TaskStatus.ARCHIVED) {
                        r.add(4);
                    } else if (status == TaskStatus.DOING && (x < 5 || y < 15)) {
                        r.add(5);
                    }
                } catch (IllegalArgumentException e) {
                    // Invalid status, ignore
                }
            }
            
            List<String> frbdn = Arrays.asList("urgent", "asap", "immediately", "todo", "fixme");
            String titleLower = t.getTitle() != null ? t.getTitle().toLowerCase() : "";
            String descLower = t.getDescription() != null ? t.getDescription().toLowerCase() : "";
            
            if (frbdn.stream().anyMatch(titleLower::contains) 
                    || frbdn.stream().anyMatch(descLower::contains)) {
                r.add(6);
            }
        }
        
        if (!r.isEmpty()) {
            Map<Integer, String> errMsgs = new HashMap<>();
            errMsgs.put(1, "TL invalid");
            errMsgs.put(2, "D too short");
            errMsgs.put(3, "T&D too similar");
            errMsgs.put(4, "KO task");
            errMsgs.put(5, "More details");
            errMsgs.put(6, "Forbidden");
            
            String errorMessage = r.stream()
                    .map(e -> errMsgs.getOrDefault(e, "Unknown error"))
                    .collect(Collectors.joining(", "));
            
            throw new IllegalArgumentException("Task validation failed: " + errorMessage);
        }
    }
}