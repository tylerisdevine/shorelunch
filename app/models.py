from datetime import datetime
from app import db


class Recipe(db.Model):
    """Recipe model."""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    servings = db.Column(db.Integer)
    photo_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_made = db.Column(db.Date)

    # Relationships
    tags = db.relationship('Tag', secondary='recipe_tags', backref=db.backref('recipes', lazy='dynamic'))
    ratings = db.relationship('Rating', backref='recipe', lazy='dynamic', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='recipe', lazy='dynamic', cascade='all, delete-orphan')
    want_to_cook = db.relationship('WantToCook', backref='recipe', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Recipe {self.title}>'

    @property
    def total_time(self):
        """Calculate total cooking time."""
        prep = self.prep_time or 0
        cook = self.cook_time or 0
        return prep + cook

    @property
    def average_rating(self):
        """Calculate average rating."""
        ratings = self.ratings.all()
        if not ratings:
            return None
        return sum(r.rating for r in ratings) / len(ratings)

    @property
    def is_favorite(self):
        """Check if recipe is marked as favorite."""
        return self.favorites.first() is not None

    @property
    def is_want_to_cook(self):
        """Check if recipe is in want to cook list."""
        return self.want_to_cook.first() is not None


class Tag(db.Model):
    """Tag model for categorizing recipes."""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50))  # cuisine, meal_type, dietary, etc.

    def __repr__(self):
        return f'<Tag {self.name}>'


# Association table for many-to-many relationship
recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Rating(db.Model):
    """Rating model for recipe feedback."""
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    rated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Rating {self.rating} stars for Recipe {self.recipe_id}>'


class Favorite(db.Model):
    """Favorite model for marking favorite recipes."""
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False, unique=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Favorite Recipe {self.recipe_id}>'


class WantToCook(db.Model):
    """Want to cook list for meal planning."""
    __tablename__ = 'want_to_cook'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False, unique=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WantToCook Recipe {self.recipe_id}>'
