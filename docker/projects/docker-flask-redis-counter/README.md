# Docker Flask Redis Counter Project

## Overview

This project demonstrates a simple web application built with Flask that uses Redis for persistent data storage. The application consists of two main services:

- **Flask Web App**: A lightweight Python web server that tracks visit counts
- **Redis Database**: An in-memory database used for storing and persisting the visit counter

## Architecture

```
User Browser → Flask App (Port 5001) → Redis Database (Port 6379)
```

### Key Features

- **Visit Counter**: Tracks the number of visits to the `/count` endpoint
- **Redis Persistence**: Data persists across container restarts using Redis append-only file (AOF)
- **Environment Configuration**: Redis connection details configurable via environment variables
- **Docker Compose**: Multi-container setup with service orchestration
- **Scalability**: Demonstrates container scaling concepts

## Project Structure

```
docker-flask-redis-counter/
├── app/
│   ├── app.py              # Flask application code
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Flask app container definition
├── docker-compose.yml      # Multi-container orchestration
└── README.md              # This documentation
```

## Step-by-Step Implementation

### Step 1: Build the Flask App

#### 1.1 Create `app/app.py`

The Flask application provides two endpoints:

```python
import os
from flask import Flask
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_KEY = os.getenv("REDIS_KEY", "visits")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route("/")
def home():
    return "Welcome! Go to /count to increment the visit counter."

@app.route("/count")
def count():
    visits = r.incr(REDIS_KEY)
    return f"Visit count: {visits}"
```

**What this does:**
- `/` endpoint: Shows a welcome message with navigation hint
- `/count` endpoint: Increments a Redis key and returns the current count
- Redis connection details are configurable via environment variables

#### 1.2 Create `app/requirements.txt`

```
flask==3.0.0
redis==5.0.1
gunicorn==22.0.0
```

**Dependencies:**
- **Flask**: Web framework for the application
- **Redis**: Python client for Redis database
- **Gunicorn**: Production-grade WSGI server for better container performance

### Step 2: Dockerise the Flask App

#### 2.1 Create `app/Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

**Dockerfile breakdown:**
- Uses Python 3.12 slim image for smaller footprint
- Sets working directory to `/app`
- Installs dependencies without cache for smaller image size
- Exposes port 5000 for web traffic
- Runs Gunicorn as production server (better than Flask development server)

### Step 3: Docker Compose Configuration

#### 3.1 Create `docker-compose.yml`

```yaml
services:
  web:
    build: ./app
    ports:
      - "5001:5000"
    environment:
      REDIS_HOST: redis
      REDIS_PORT: 6379
      REDIS_KEY: visits
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: ["redis-server", "--appendonly", "yes"]

volumes:
  redis_data:
```

**Key features:**
- **Service orchestration**: Manages both Flask and Redis containers
- **Port mapping**: Maps host port 5001 to container port 5000
- **Environment variables**: Passes Redis connection details to Flask
- **Service dependencies**: Ensures Redis starts before Flask app
- **Data persistence**: Uses named volume for Redis data persistence
- **Redis AOF**: Enables append-only file for durability

### Step 4: Build and Run

```bash
# Build and start all services
docker compose up --build

# Or run in detached mode
docker compose up --build -d
```

### Step 5: Test the Application

#### 5.1 Test Welcome Page

```bash
curl http://localhost:5001
```

**Expected output:**
```
Welcome! Go to /count to increment the visit counter.
```

#### 5.2 Test Counter Functionality

```bash
# First visit
curl http://localhost:5001/count
# Output: Visit count: 1

# Second visit
curl http://localhost:5001/count
# Output: Visit count: 2

# Third visit
curl http://localhost:5001/count
# Output: Visit count: 3
```

### Step 6: Redis Persistence Testing

#### 6.1 Test Data Persistence

1. Visit `/count` several times to increment the counter
2. Stop all containers:
   ```bash
   docker compose down
   ```
3. Restart containers:
   ```bash
   docker compose up -d
   ```
4. Test `/count` again - the counter should continue from the previous value

**This proves Redis persistence is working correctly.**

### Step 7: Container Scaling (Demonstration)

#### 7.1 Scale Web Service

```bash
# Scale to 3 web containers
docker compose up --build --scale web=3

# Check running containers
docker compose ps
```

**Important Note on Scaling:**
- Multiple containers are created but only one can bind to port 5001
- Proper load balancing would require a reverse proxy (NGINX/HAProxy)
- This demonstrates the concept but shows the limitation of simple port mapping

#### 7.2 Scaling Limitations

With current setup:
- Only one container can publish to port 5001
- Other scaled containers run but aren't accessible via port mapping
- Solution: Add NGINX as load balancer in front of multiple web containers

### Step 8: Cleanup

```bash
# Stop and remove containers
docker compose down

# Stop containers and remove volumes (wipes Redis data)
docker compose down -v
```

## Environment Variables

The Flask application supports the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `redis` | Redis server hostname |
| `REDIS_PORT` | `6379` | Redis server port |
| `REDIS_KEY` | `visits` | Redis key name for counter |

## Docker Commands Reference

### Essential Commands

```bash
# Build and start services
docker compose up --build

# Start in background
docker compose up -d

# View running containers
docker compose ps

# View logs
docker compose logs

# View logs for specific service
docker compose logs web
docker compose logs redis

# Stop services
docker compose down

# Stop services and remove volumes
docker compose down -v

# Scale services
docker compose up --scale web=3

# Rebuild specific service
docker compose up --build web
```

### Advanced Commands

```bash
# Execute commands in running container
docker compose exec web sh
docker compose exec redis redis-cli

# Monitor resource usage
docker stats

# Inspect container details
docker compose inspect web
```

## Technical Concepts Demonstrated

### 1. Multi-Container Applications
- Service orchestration with Docker Compose
- Inter-service communication
- Service dependencies

### 2. Data Persistence
- Docker volumes for data persistence
- Redis append-only file (AOF) configuration
- Data survival across container restarts

### 3. Environment Configuration
- Environment variable injection
- Configuration flexibility
- Development vs production setups

### 4. Container Networking
- Service discovery via service names
- Port mapping
- Internal container communication

### 5. Application Architecture
- Web application with database backend
- Separation of concerns
- Scalable design patterns

## Troubleshooting

### Common Issues

#### Port Conflicts
**Problem:** `port is already allocated` error
**Solution:** 
- Change port mapping in docker-compose.yml
- Stop services using the port: `lsof -i :5001` then `kill -9 <PID>`

#### Redis Connection Issues
**Problem:** Flask can't connect to Redis
**Solution:**
- Ensure Redis service is running: `docker compose ps`
- Check Redis logs: `docker compose logs redis`
- Verify service name matches `REDIS_HOST` environment variable

#### Container Build Issues
**Problem:** Build fails during `pip install`
**Solution:**
- Check requirements.txt for correct versions
- Clear Docker cache: `docker system prune -a`
- Rebuild: `docker compose build --no-cache`

#### Volume Issues
**Problem:** Data not persisting
**Solution:**
- Verify volume exists: `docker volume ls`
- Check volume mounting: `docker compose inspect redis`
- Ensure Redis AOF is enabled

### Debugging Commands

```bash
# Check container status
docker compose ps

# View service logs
docker compose logs web
docker compose logs redis

# Test Redis connection
docker compose exec redis redis-cli ping

# Check Redis data
docker compose exec redis redis-cli get visits

# Inspect container configuration
docker compose inspect web
docker compose inspect redis

# Access container shell
docker compose exec web sh
docker compose exec redis sh
```

## Performance Considerations

### Optimization Tips

1. **Image Size**: Use `--no-cache-dir` in pip install
2. **Multi-stage builds**: For production, consider multi-stage Dockerfiles
3. **Health checks**: Add health checks to docker-compose.yml
4. **Resource limits**: Set memory and CPU limits in production
5. **Redis configuration**: Tune Redis settings for production workloads

### Production Enhancements

For production deployment, consider:

1. **Load Balancer**: Add NGINX/HAProxy for proper load distribution
2. **SSL/TLS**: Implement HTTPS with certificates
3. **Monitoring**: Add health checks and monitoring
4. **Logging**: Centralized logging solution
5. **Security**: Network policies and secrets management

## Learning Outcomes

This project demonstrates:

- **Container Orchestration**: Managing multi-container applications
- **Data Persistence**: Implementing durable storage with Docker volumes
- **Service Communication**: Inter-service networking and dependencies
- **Configuration Management**: Environment-based configuration
- **Scaling Concepts**: Understanding container scaling limitations
- **Production Practices**: Using Gunicorn instead of development server

## Next Steps

Potential enhancements:

1. **Add NGINX**: Implement proper load balancing
2. **SSL/TLS**: Add HTTPS support
3. **Monitoring**: Add health checks and metrics
4. **CI/CD**: Automate builds and deployments
5. **Kubernetes**: Migrate to Kubernetes for advanced orchestration

---

**Project Status:** ✅ Complete  
**Last Updated:** February 2026  
**Technologies Used:** Docker, Docker Compose, Flask, Redis, Gunicorn  
**Features:** Web counter, Redis persistence, container orchestration
