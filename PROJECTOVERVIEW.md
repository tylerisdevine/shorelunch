# ShoreLunch - Recipe Management & Meal Planning App

## Project Description
A local recipe database application that allows viewing, editing, and organizing recipes on mobile devices. The goal is to make meal planning easier by providing a searchable recipe collection with ratings, comments, and favorites lists.

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Containerization**: Docker + Docker Compose
- **Frontend**: Responsive web app (Flask templates or lightweight JS framework)
- **Python Libraries**: Flask-SQLAlchemy, Flask-WTF (forms), Flask-Migrate (DB migrations)

## Architecture
```
┌─────────────────┐
│  Mobile Browser │
│   (responsive)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask App      │
│  (Container)    │
│  - Routes/API   │
│  - Business     │
│    Logic        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MySQL DB       │
│  (Container)    │
│  - Recipes      │
│  - Tags         │
│  - Ratings      │
│  - Comments     │
└─────────────────┘
```

## Core Features (MVP)

### Recipe Management
- [x] Manual recipe entry (title, ingredients, instructions, prep/cook time)
- [ ] View recipe details
- [ ] Edit recipes
- [ ] Delete recipes
- [ ] Upload recipe photos

### Organization & Discovery
- [ ] Tag recipes (cuisine type, meal type, dietary restrictions, etc.)
- [ ] Search recipes by name
- [ ] Filter recipes by tags
- [ ] Full-text search in ingredients/instructions

### Rating & Feedback
- [ ] Rate recipes (1-5 stars)
- [ ] Add comments/notes to recipes (e.g., "add more garlic next time")
- [ ] View rating history

### Meal Planning (Simple)
- [ ] Mark recipes as "favorites"
- [ ] Create "want to cook" list
- [ ] Track when recipes were last made

### Mobile Experience
- [ ] Responsive design for mobile viewing
- [ ] Easy navigation while cooking
- [ ] Touch-friendly interface

## Future Features (Post-MVP)

### Import/Export
- [ ] Parse recipe from URL (auto-import)
- [ ] Export recipe to PDF
- [ ] Print-friendly recipe view
- [ ] Batch import/export recipes (JSON/CSV)

### Advanced Meal Planning
- [ ] Weekly calendar view
- [ ] Assign recipes to specific days/meals
- [ ] Meal plan history

### Enhancement Features
- [ ] Nutritional information
- [ ] Recipe scaling (adjust servings)
- [ ] Shopping list generation from recipes
- [ ] Recipe sharing/collaboration

## Database Schema (Draft)

### Tables
- **recipes**: id, title, description, ingredients (text), instructions (text), prep_time, cook_time, servings, photo_url, created_at, updated_at, last_made
- **tags**: id, name, category (cuisine, meal_type, dietary, etc.)
- **recipe_tags**: recipe_id, tag_id (many-to-many)
- **ratings**: id, recipe_id, rating (1-5), comment, rated_at
- **favorites**: id, recipe_id, added_at
- **want_to_cook**: id, recipe_id, added_at

## Development Roadmap

### Phase 1: Project Setup
- [ ] Create Docker Compose configuration
- [ ] Set up Flask project structure
- [ ] Configure MySQL container with persistent volumes
- [ ] Set up Flask-SQLAlchemy
- [ ] Create initial database migrations

### Phase 2: Core Recipe CRUD
- [ ] Design database schema
- [ ] Create Recipe model
- [ ] Build recipe creation form
- [ ] Build recipe list view
- [ ] Build recipe detail view
- [ ] Build recipe edit/delete functionality

### Phase 3: Tagging & Search
- [ ] Create Tag model and relationships
- [ ] Build tag management interface
- [ ] Implement search functionality
- [ ] Implement filtering by tags

### Phase 4: Ratings & Comments
- [ ] Create Rating model
- [ ] Add rating interface to recipe detail page
- [ ] Display average ratings on recipe list
- [ ] Add comment section to recipes

### Phase 5: Meal Planning (Simple)
- [ ] Add favorites toggle to recipes
- [ ] Create favorites list view
- [ ] Add "want to cook" list functionality
- [ ] Track "last made" date

### Phase 6: Mobile Optimization
- [ ] Responsive CSS for mobile devices
- [ ] Test on actual mobile devices
- [ ] Optimize for touch interactions
- [ ] Add PWA features (optional)

## Current Sprint: Phase 1 - Project Setup

### TODO
- [ ] Create Dockerfile for Flask app
- [ ] Create docker-compose.yml
- [ ] Set up Flask project structure (app factory pattern)
- [ ] Configure MySQL connection
- [ ] Set up Flask-Migrate for database migrations
- [ ] Create base templates (layout, navigation)
- [ ] Test containers can communicate

## Notes

### Tech Stack Rationale
- **Flask over Django**: Lightweight, flexible, good for this scope
- **MySQL over SQLite**: More robust, better for concurrent access from mobile
- **Docker**: Consistent environment, easy deployment, can run anywhere

### Design Decisions
- Starting with simple meal planning (favorites list) rather than full calendar to get MVP faster
- Prioritizing mobile-friendly interface since primary use case is viewing on phone while cooking
- **No authentication required**: Shared access for household use without login complexity
- **Single photo per recipe**: Simpler to implement and manage, one main photo is sufficient
- **No version history**: Recipe edits simply overwrite, keeping the system simple
- **No user system**: Two people will use the app, but no need for separate accounts or permissions

### Useful Resources
- Flask Documentation: https://flask.palletsprojects.com/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- MySQL Docker Image: https://hub.docker.com/_/mysql
- Recipe Schema.org markup: https://schema.org/Recipe (useful for future URL parsing)

---
**Last Updated**: 2026-02-01
