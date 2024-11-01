# Docker Readme

This document provides instructions and details for managing the Docker setup used in this project.

## Table of Contents
1. [Starting the Docker Environment](#starting-the-docker-environment)
2. [Shutting Down the Docker Environment](#shutting-down-the-docker-environment)
3. [Docker Compose Commands Overview](#docker-compose-commands-overview)
4. [Project Structure and Services](#project-structure-and-services)

---

### Starting the Docker Environment

To build and start the Docker containers with the latest updates, navigate to the Docker folder and use the following command:

```bash
docker compose up --build
```

- **Explanation**:
  - `docker compose up`: Starts the Docker environment defined in the `docker-compose.yml` file.
  - `--build`: Forces a rebuild of the images before starting the containers, ensuring the latest code changes are applied.

### Shutting Down the Docker Environment

To gracefully stop and remove the running containers, use:

```bash
docker compose down
```

- **Explanation**:
  - `docker compose down`: Stops all containers defined in the `docker-compose.yml` file and removes them, along with any associated networks. This ensures a clean environment for the next time you start it.

---

### Docker Compose Commands Overview

Here are a few additional Docker Compose commands that may be useful for specific actions:

- **View Running Containers**:
  ```bash
  docker compose ps
  ```
  Lists all containers managed by Docker Compose, along with their status.

- **Start Containers in Detached Mode**:
  ```bash
  docker compose up -d
  ```
  Starts the Docker environment in the background, allowing you to continue using the terminal.

- **Restart Containers**:
  ```bash
  docker compose restart
  ```
  Restarts all running containers without rebuilding them.

- **View Logs**:
  ```bash
  docker compose logs -f
  ```
  Streams the logs from all containers, useful for debugging and monitoring live activity.

- **Remove All Containers, Networks, and Volumes (Cleanup)**:
  ```bash
  docker compose down -v
  ```
  Removes containers, networks, and any persistent data in volumes. Use with caution, as this will delete stored data.

---

### Project Structure and Services

The `docker-compose.yml` file defines the services, volumes, and networks for this project. Here's a breakdown of the typical structure and functionality:

1. **App Service (e.g., HueMIDI Server)**:
   - **Purpose**: Hosts the main application service for handling MIDI commands and controlling Philips Hue lights via a REST API.
   - **Ports**: Exposes ports defined in the Dockerfile to make the application accessible (e.g., `9010`).
   - **Dependencies**: May depend on other services (e.g., database, backend API).
   
2. **Environment Variables**:
   - The `.env` file is loaded by Docker Compose to pass configuration values (e.g., `SERVER_IP`, `SERVER_PORT`, `BRIDGE_IP`, `USERNAME`).
   - **Example**:
     ```plaintext
     SERVER_IP=localhost
     SERVER_PORT=9010
     BRIDGE_IP=<Your_Hue_Bridge_IP>
     USERNAME=<Hue_API_Username>
     ```
   
3. **Dockerfile**:
   - Specifies the build process for the main application image, including base image selection, dependency installation, and application setup.
   - **Example**:
     ```Dockerfile
     FROM python:3.9
     WORKDIR /app
     COPY . /app
     RUN pip install -r requirements.txt
     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9010"]
     ```

4. **Volumes**:
   - Ensures that code and configuration changes persist across container restarts or can be shared across services if necessary.
   - **Example**:
     ```yaml
     volumes:
       - .:/app  # Mounts the current directory to /app in the container
     ```

5. **Networks**:
   - Custom networks can be defined to isolate communication between services, enhancing security and performance.
   - **Example**:
     ```yaml
     networks:
       default:
         external:
           name: my_network
     ```

---

### Troubleshooting Tips

- **Container Build Issues**: If you encounter issues with outdated images or dependencies, try rebuilding without cache:
  ```bash
  docker compose build --no-cache
  ```

- **Application Logs**: Use `docker compose logs -f` to monitor real-time logs from all containers for any errors or issues.

- **Data Persistence**: If your application uses volumes for persistence, make sure to check your volume paths to avoid data loss during `down -v` operations.

- **Environment Variable Updates**: If `.env` values are changed, use `docker compose down` followed by `docker compose up --build` to apply the changes.

---

This setup allows you to easily build, run, and manage the entire application stack in Docker, providing an isolated environment to ensure consistency and easy deployment.