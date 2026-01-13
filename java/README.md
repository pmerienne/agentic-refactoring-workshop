# Task Flow API

## Project Structure

The `task_flow_api` project is organized into a three-layer architecture consisting of the following directories:
```
src/main/java/com/taskflow/
├── controller/
│   └── TaskController.java    # API layer with routes for handling HTTP requests
├── service/
│   └── TaskService.java        # Business logic layer interacting with repository
├── repository/
│   └── TaskRepository.java     # Database interactions and CRUD operations
├── model/
│   └── Task.java               # Data models used in the application
└── TaskFlowApplication.java    # Spring Boot application entry point

src/main/resources/
├── application.properties      # Application configuration
└── application.yml             # Alternative YAML configuration

pom.xml                         # Maven dependencies and project configuration
```


## Prerequisites

Before running this project, ensure you have the following installed:

- **JDK 17**: [Download JDK 17](https://www.oracle.com/java/technologies/downloads/#java17) or use [OpenJDK 17](https://jdk.java.net/17/)
- **Maven 3.6+**: [Download Maven](https://maven.apache.org/download.cgi) and follow the [installation guide](https://maven.apache.org/install.html)

Verify your installations:
```bash
java -version  # Should show Java 17
mvn -version   # Should show Maven 3.6 or higher
```


## Dev guide

To set up the project, you must follow these steps:
```bash
mvn clean install
```


To launch the Spring Boot application, use the following command:

```bash
mvn spring-boot:run
```

This command starts the server with auto-reload enabled (via Spring Boot DevTools if configured), allowing you to see changes without restarting the server.

```bash
# Expected response: {"version":"1.0.0"}
curl 127.0.0.1:8080/version
```
