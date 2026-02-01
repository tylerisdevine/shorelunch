import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from app import db
from app.models import Recipe, Tag, Rating, Favorite, WantToCook

bp = Blueprint('main', __name__)


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route('/')
def index():
    """Homepage - display all recipes."""
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes)


@bp.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Display a single recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)


@bp.route('/recipe/new', methods=['GET', 'POST'])
def recipe_new():
    """Create a new recipe."""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        prep_time = request.form.get('prep_time')
        cook_time = request.form.get('cook_time')
        servings = request.form.get('servings')

        # Handle photo upload
        photo_url = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                # Add timestamp to avoid filename collisions
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
                photo_url = f"/uploads/{filename}"

        # Create recipe
        recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            prep_time=int(prep_time) if prep_time else None,
            cook_time=int(cook_time) if cook_time else None,
            servings=int(servings) if servings else None,
            photo_url=photo_url
        )

        db.session.add(recipe)
        db.session.commit()

        flash('Recipe created successfully!', 'success')
        return redirect(url_for('main.recipe_detail', recipe_id=recipe.id))

    return render_template('recipe_form.html', recipe=None)


@bp.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
def recipe_edit(recipe_id):
    """Edit an existing recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        # Update form data
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')

        prep_time = request.form.get('prep_time')
        cook_time = request.form.get('cook_time')
        servings = request.form.get('servings')

        recipe.prep_time = int(prep_time) if prep_time else None
        recipe.cook_time = int(cook_time) if cook_time else None
        recipe.servings = int(servings) if servings else None

        # Handle photo upload
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                # Add timestamp to avoid filename collisions
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
                recipe.photo_url = f"/uploads/{filename}"

        db.session.commit()

        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('main.recipe_detail', recipe_id=recipe.id))

    return render_template('recipe_form.html', recipe=recipe)


@bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def recipe_delete(recipe_id):
    """Delete a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('main.index'))


@bp.route('/favorites')
def favorites():
    """Display favorite recipes."""
    favorites = Favorite.query.order_by(Favorite.added_at.desc()).all()
    recipes = [fav.recipe for fav in favorites]
    return render_template('favorites.html', recipes=recipes)


@bp.route('/want-to-cook')
def want_to_cook():
    """Display want to cook list."""
    want_to_cook_list = WantToCook.query.order_by(WantToCook.added_at.desc()).all()
    recipes = [wtc.recipe for wtc in want_to_cook_list]
    return render_template('want_to_cook.html', recipes=recipes)


@bp.route('/search')
def search():
    """Search recipes."""
    query = request.args.get('q', '')
    tag_filter = request.args.get('tag', '')

    recipes = Recipe.query

    if query:
        search_pattern = f'%{query}%'
        recipes = recipes.filter(
            db.or_(
                Recipe.title.ilike(search_pattern),
                Recipe.ingredients.ilike(search_pattern),
                Recipe.instructions.ilike(search_pattern)
            )
        )

    if tag_filter:
        tag = Tag.query.filter_by(name=tag_filter).first()
        if tag:
            recipes = recipes.filter(Recipe.tags.contains(tag))

    recipes = recipes.order_by(Recipe.created_at.desc()).all()
    return render_template('search.html', recipes=recipes, query=query, tag_filter=tag_filter)
