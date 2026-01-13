package com.taskflow.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class TaskControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testGetVersion() throws Exception {
        mockMvc.perform(get("/version"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.version").value("1.0.0"));
    }

    @Test
    public void testCreateTaskSuccess() throws Exception {
        String taskJson = """
                {
                    "title": "API Test Task",
                    "description": "This is a test task created via API with sufficient description",
                    "status": "TODO",
                    "completed": false
                }
                """;

        mockMvc.perform(post("/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(taskJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("API Test Task"))
                .andExpect(jsonPath("$.description").value("This is a test task created via API with sufficient description"))
                .andExpect(jsonPath("$.id").exists());
    }

    @Test
    public void testCreateTaskWithInvalidData() throws Exception {
        String taskJson = """
                {
                    "title": "",
                    "description": "Valid description content",
                    "status": "TODO",
                    "completed": false
                }
                """;

        // Expecting a 500 error due to validation failure
        try {
            mockMvc.perform(post("/tasks")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(taskJson))
                    .andExpect(status().is5xxServerError());
        } catch (Exception e) {
            // Expected - validation failed
            assert e.getMessage().contains("Task validation failed");
        }
    }

    @Test
    public void testUpdateTaskSuccess() throws Exception {
        // First, create a task
        String createTaskJson = """
                {
                    "title": "Original Task",
                    "description": "This is the original task description with sufficient content",
                    "status": "TODO",
                    "completed": false
                }
                """;

        String createResponse = mockMvc.perform(post("/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(createTaskJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").exists())
                .andReturn()
                .getResponse()
                .getContentAsString();

        // Extract the task ID from the response
        Long taskId = Long.parseLong(createResponse.split("\"id\":")[1].split(",")[0]);

        // Now, update the task
        String updateTaskJson = """
                {
                    "title": "Updated Task",
                    "description": "This is the updated task description with sufficient content",
                    "status": "DOING",
                    "completed": false
                }
                """;

        mockMvc.perform(put("/tasks/" + taskId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(updateTaskJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(taskId))
                .andExpect(jsonPath("$.title").value("Updated Task"))
                .andExpect(jsonPath("$.description").value("This is the updated task description with sufficient content"))
                .andExpect(jsonPath("$.status").value("DOING"));
    }
}
