import os

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

from app import db
from app.models import Favorite, Rating, Recipe, Tag, WantToCook

bp = Blueprint("main", __name__)


def process_tags(tag_string):
    """Process comma-separated tag string and return list of Tag objects."""
    if not tag_string:
        return []

    tag_names = [name.strip() for name in tag_string.split(",") if name.strip()]
    tags = []

    for tag_name in tag_names:
        # Get or create tag
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        tags.append(tag)

    return tags


@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@bp.route("/")
def index():
    """Homepage - display all recipes."""
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template("index.html", recipes=recipes)


@bp.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    """Display a single recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)


@bp.route("/recipe/new", methods=["GET", "POST"])
def recipe_new():
    """Create a new recipe."""
    if request.method == "POST":
        # Get form data
        title = request.form.get("title")
        description = request.form.get("description")
        ingredients = request.form.get("ingredients")
        instructions = request.form.get("instructions")
        prep_time = request.form.get("prep_time")
        cook_time = request.form.get("cook_time")
        servings = request.form.get("servings")

        # Handle photo upload
        photo_url = None
        if "photo" in request.files:
            photo = request.files["photo"]
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                # Add timestamp to avoid filename collisions
                from datetime import datetime

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{filename}"
                photo_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
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
            photo_url=photo_url,
        )

        # Process tags
        tag_string = request.form.get("tags", "")
        recipe.tags = process_tags(tag_string)

        db.session.add(recipe)
        db.session.commit()

        flash("Recipe created successfully!", "success")
        return redirect(url_for("main.recipe_detail", recipe_id=recipe.id))

    return render_template("recipe_form.html", recipe=None)


@bp.route("/recipe/<int:recipe_id>/edit", methods=["GET", "POST"])
def recipe_edit(recipe_id):
    """Edit an existing recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == "POST":
        # Update form data
        recipe.title = request.form.get("title")
        recipe.description = request.form.get("description")
        recipe.ingredients = request.form.get("ingredients")
        recipe.instructions = request.form.get("instructions")

        prep_time = request.form.get("prep_time")
        cook_time = request.form.get("cook_time")
        servings = request.form.get("servings")

        recipe.prep_time = int(prep_time) if prep_time else None
        recipe.cook_time = int(cook_time) if cook_time else None
        recipe.servings = int(servings) if servings else None

        # Handle photo upload
        if "photo" in request.files:
            photo = request.files["photo"]
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                # Add timestamp to avoid filename collisions
                from datetime import datetime

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{filename}"
                photo_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                photo.save(photo_path)
                recipe.photo_url = f"/uploads/{filename}"

        # Process tags
        tag_string = request.form.get("tags", "")
        recipe.tags = process_tags(tag_string)

        db.session.commit()

        flash("Recipe updated successfully!", "success")
        return redirect(url_for("main.recipe_detail", recipe_id=recipe.id))

    return render_template("recipe_form.html", recipe=recipe)


@bp.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
def recipe_delete(recipe_id):
    """Delete a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe deleted successfully!", "success")
    return redirect(url_for("main.index"))


@bp.route("/recipe/<int:recipe_id>/rating", methods=["POST"])
def add_rating(recipe_id):
    """Add a rating and comment to a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)

    rating_value = request.form.get("rating")
    comment = request.form.get("comment")

    if rating_value:
        rating = Rating(
            recipe_id=recipe_id, rating=int(rating_value), comment=comment if comment else None
        )
        db.session.add(rating)
        db.session.commit()
        flash("Rating added successfully!", "success")
    else:
        flash("Please select a rating.", "error")

    return redirect(url_for("main.recipe_detail", recipe_id=recipe_id))


@bp.route("/recipe/<int:recipe_id>/favorite/toggle", methods=["POST"])
def toggle_favorite(recipe_id):
    """Toggle recipe favorite status."""
    recipe = Recipe.query.get_or_404(recipe_id)

    existing_favorite = Favorite.query.filter_by(recipe_id=recipe_id).first()

    if existing_favorite:
        db.session.delete(existing_favorite)
        db.session.commit()
        flash("Removed from favorites.", "success")
    else:
        favorite = Favorite(recipe_id=recipe_id)
        db.session.add(favorite)
        db.session.commit()
        flash("Added to favorites!", "success")

    return redirect(url_for("main.recipe_detail", recipe_id=recipe_id))


@bp.route("/recipe/<int:recipe_id>/want-to-cook/toggle", methods=["POST"])
def toggle_want_to_cook(recipe_id):
    """Toggle recipe want to cook status."""
    recipe = Recipe.query.get_or_404(recipe_id)

    existing_wtc = WantToCook.query.filter_by(recipe_id=recipe_id).first()

    if existing_wtc:
        db.session.delete(existing_wtc)
        db.session.commit()
        flash("Removed from want to cook list.", "success")
    else:
        wtc = WantToCook(recipe_id=recipe_id)
        db.session.add(wtc)
        db.session.commit()
        flash("Added to want to cook list!", "success")

    return redirect(url_for("main.recipe_detail", recipe_id=recipe_id))


@bp.route("/favorites")
def favorites():
    """Display favorite recipes."""
    favorites = Favorite.query.order_by(Favorite.added_at.desc()).all()
    recipes = [fav.recipe for fav in favorites]
    return render_template("favorites.html", recipes=recipes)


@bp.route("/want-to-cook")
def want_to_cook():
    """Display want to cook list."""
    want_to_cook_list = WantToCook.query.order_by(WantToCook.added_at.desc()).all()
    recipes = [wtc.recipe for wtc in want_to_cook_list]
    return render_template("want_to_cook.html", recipes=recipes)


@bp.route("/search")
def search():
    """Search recipes."""
    query = request.args.get("q", "")
    tag_filter = request.args.get("tag", "")

    recipes = Recipe.query

    if query:
        search_pattern = f"%{query}%"
        recipes = recipes.filter(
            db.or_(
                Recipe.title.ilike(search_pattern),
                Recipe.ingredients.ilike(search_pattern),
                Recipe.instructions.ilike(search_pattern),
            )
        )

    if tag_filter:
        tag = Tag.query.filter_by(name=tag_filter).first()
        if tag:
            recipes = recipes.filter(Recipe.tags.contains(tag))

    recipes = recipes.order_by(Recipe.created_at.desc()).all()
    return render_template("search.html", recipes=recipes, query=query, tag_filter=tag_filter)


@bp.route("/tags")
def tags():
    """Display all tags with recipe counts."""
    all_tags = Tag.query.order_by(Tag.name).all()
    # Build a list of tags with their recipe counts
    tags_with_counts = []
    for tag in all_tags:
        count = tag.recipes.count()
        tags_with_counts.append({"tag": tag, "count": count})
    return render_template("tags.html", tags_with_counts=tags_with_counts)
