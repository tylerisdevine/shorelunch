# ShoreLunch - Recipe Management & Meal Planning App

A local recipe database application for viewing, editing, and organizing recipes on mobile devices. Built with Flask, MySQL, and Docker for easy deployment and household sharing.

## Features

- Create, view, edit, and delete recipes
- Tag and categorize recipes (cuisine, meal type, dietary restrictions)
- Search and filter recipes
- Rate and comment on recipes
- Mark favorites and create "want to cook" lists
- Track when recipes were last made
- Mobile-friendly responsive design
- Photo upload for recipes

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL 8.0
- **Containerization**: Docker + Docker Compose
- **Frontend**: HTML5, CSS3, Jinja2 templates

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- See [SETUP.md](SETUP.md) for detailed installation instructions

### Installation

1. **Clone the repository**
   ```bash
   cd /home/ubunturoot/shorelunch
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred passwords
   ```

3. **Build and start containers**
   ```bash
   docker compose build
   docker compose up -d
   ```

4. **Initialize database**
   ```bash
   docker compose exec web flask db init
   docker compose exec web flask db migrate -m "Initial migration"
   docker compose exec web flask db upgrade
   ```

5. **Access the application**
   - Open browser to http://localhost:5000
   - From mobile on same network: http://[YOUR_IP]:5000

## Project Structure

```
shorelunch/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── routes.py            # View routes
│   ├── static/
│   │   └── css/
│   │       └── style.css    # Styling
│   └── templates/           # Jinja2 templates
│       ├── base.html
│       └── index.html
├── uploads/                 # Recipe photos
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Flask container definition
├── docker-compose.yml     # Multi-container orchestration
├── run.py                 # Application entry point
├── PROJECTOVERVIEW.md     # Detailed project plan and roadmap
└── SETUP.md              # Setup and deployment guide
```

## Documentation

- **[PROJECTOVERVIEW.md](PROJECTOVERVIEW.md)** - Complete project overview, features, roadmap, and design decisions
- **[SETUP.md](SETUP.md)** - Detailed setup instructions, Docker commands, and troubleshooting

## Development

### Running in Development Mode

```bash
docker compose up -d
docker compose logs -f web
```

Code changes in the `app/` directory are automatically reloaded.

### Database Migrations

After modifying models:
```bash
docker compose exec web flask db migrate -m "Description"
docker compose exec web flask db upgrade
```

### Common Commands

```bash
# View logs
docker compose logs -f

# Access Flask shell
docker compose exec web flask shell

# Access database
docker compose exec db mysql -u shorelunch -p

# Restart services
docker compose restart web
```

## Current Status

**Phase 1: Project Setup** ✅ Complete
- Docker configuration
- Flask app structure
- Database models
- Basic templates

**Next Up: Phase 2 - Core Recipe CRUD**
- Recipe creation forms
- Recipe detail views
- Edit/delete functionality

See [PROJECTOVERVIEW.md](PROJECTOVERVIEW.md) for full roadmap.

## Contributing

This is a personal project for household use. Feel free to fork and adapt for your own needs!

## License

MIT License - see [LICENSE](LICENSE) file for details
