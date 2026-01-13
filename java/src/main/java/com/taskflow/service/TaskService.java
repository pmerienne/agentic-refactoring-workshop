package com.taskflow.service;

import com.taskflow.model.Task;
import com.taskflow.model.TaskStatus;
import com.taskflow.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class TaskService {

    private final TaskRepository taskRepository;
    private final TaskValidationService taskValidationService;
    private final TaskRulesEngine taskRulesEngine;

    @Autowired
    public TaskService(TaskRepository taskRepository, TaskValidationService taskValidationService, TaskRulesEngine taskRulesEngine) {
        this.taskRepository = taskRepository;
        this.taskValidationService = taskValidationService;
        this.taskRulesEngine = taskRulesEngine;
    }

    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    public Optional<Task> getTaskById(Long id) {
        return taskRepository.findById(id);
    }

    public Task createTask(Task task) {
        taskValidationService.vldTskBfrCrt(task, true);
        return taskRepository.save(task);
    }

    public Task updateTask(Long id, Task taskDetails) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Task not found with id " + id));
        taskValidationService.vldTskBfrCrt(task, true);
        task.setTitle(taskDetails.getTitle());
        task.setDescription(taskDetails.getDescription());
        task.setStatus(taskDetails.getStatus());
        if (task.getStatus() == TaskStatus.DONE) {
            task.setCompleted(true);
        }

        String report = this.taskRulesEngine.postProcess(task);
        System.out.println(report);

        return taskRepository.save(task);
    }

    public void deleteTask(Long id) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Task not found with id " + id));
        taskRepository.delete(task);
    }
}