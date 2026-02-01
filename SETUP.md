# ShoreLunch Setup Guide

## Prerequisites

### 1. Install Docker
If you don't have Docker installed, follow the instructions for your OS:

**Ubuntu/Debian:**
```bash
# Remove any old Docker installations
sudo apt-get remove docker docker-engine docker.io containerd runc

# Update package index and install prerequisites
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker CE (Community Edition)
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
# Or run: newgrp docker
```

**macOS:**
- Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)

**Windows:**
- Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

### 2. Verify Docker Installation
```bash
docker --version
docker compose version
```

## Getting Started

### 1. Clone/Navigate to Project
```bash
cd /home/ubunturoot/shorelunch
```

### 2. Build and Start Containers
```bash
# Build the containers
docker compose build

# Start the services
docker compose up -d

# Check if containers are running
docker compose ps
```

### 3. Initialize Database
Once the containers are running, initialize the database with migrations:

```bash
# Access the Flask container
docker compose exec web bash

# Inside the container, run:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Exit the container
exit
```

### 4. Access the Application
Open your browser and navigate to:
- **Web App**: http://localhost:5000
- **MySQL**: localhost:3306 (if you need to connect with a client)

## Common Docker Commands

### Start/Stop Services
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes all data)
docker compose down -v
```

### View Logs
```bash
# View all logs
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View logs for specific service
docker compose logs web
docker compose logs db
```

### Restart Services
```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart web
```

### Database Access
```bash
# Access MySQL CLI
docker compose exec db mysql -u shorelunch -p
# Password: shorelunch_password

# Or as root
docker compose exec db mysql -u root -p
# Password: root_password_2026
```

### Flask Shell
```bash
# Access Flask interactive shell
docker compose exec web flask shell
```

### Rebuild After Code Changes
```bash
# If you change requirements.txt or Dockerfile
docker compose build web
docker compose up -d

# If you only change Python code, just restart
docker compose restart web
```

## Development Workflow

### Making Code Changes
1. Edit files in your local `app/` directory
2. Changes are automatically reflected (volume mount)
3. Flask auto-reloads in development mode

### Adding Python Dependencies
1. Add package to `requirements.txt`
2. Rebuild the web container:
   ```bash
   docker compose build web
   docker compose up -d
   ```

### Database Migrations
After changing models in `app/models.py`:
```bash
docker compose exec web flask db migrate -m "Description of changes"
docker compose exec web flask db upgrade
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker compose logs web
docker compose logs db

# Check if ports are already in use
sudo lsof -i :5000
sudo lsof -i :3306
```

### Database Connection Issues
```bash
# Check if database is healthy
docker compose ps

# Wait for database to be ready (it takes ~30 seconds on first start)
docker compose logs db | grep "ready for connections"
```

### Reset Everything
```bash
# Stop and remove all containers and volumes
docker compose down -v

# Rebuild and start fresh
docker compose build
docker compose up -d

# Re-initialize database
docker compose exec web flask db init
docker compose exec web flask db migrate -m "Initial migration"
docker compose exec web flask db upgrade
```

## Mobile Access

To access the app from your phone on the same network:

1. Find your computer's local IP address:
   ```bash
   # Linux/macOS
   ip addr show | grep inet
   # or
   ifconfig | grep inet
   ```

2. Access from phone browser:
   ```
   http://[YOUR_IP]:5000
   ```
   For example: `http://192.168.1.100:5000`

3. Make sure your firewall allows connections on port 5000

## Production Deployment

For production deployment:
1. Change all passwords in `.env`
2. Set `FLASK_ENV=production`
3. Generate a strong `SECRET_KEY`
4. Consider using nginx as reverse proxy
5. Set up SSL/TLS certificates
6. Configure regular database backups

## Next Steps

Once everything is running:
1. Access http://localhost:5000
2. Start adding recipes!
3. Test the mobile interface from your phone
4. See [PROJECTOVERVIEW.md](PROJECTOVERVIEW.md) for the development roadmap
