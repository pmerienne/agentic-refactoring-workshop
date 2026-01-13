package com.taskflow.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class VersionController {

    @GetMapping("/version")
    public Map<String, String> getVersion() {
        return Map.of("version", "1.0.0");
    }
}
