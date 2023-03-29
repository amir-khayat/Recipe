from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/dashboard')
def recipe():
    if 'user_id' not in session:
        return redirect ('/logout_session')
    else:
        data = {
            'id': session['user_id']
        }
        user = User.get_user(data)
        recipes = Recipe.get_all_with_recipes_with_creator()
    return render_template("recipe.html", user = user , recipes = recipes)

@app.route('/recipes/add')
def add_recipe():
    if 'user_id' not in session:
        return redirect ('/logout_session')
    else:
        return render_template('add_recipe.html')

@app.route('/recipes/new', methods=['POST'])
def new_recipe():
    if 'user_id' not in session:
        return redirect ('/logout_session')
    # validate the form data
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/add')
    
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'under': request.form['under'],
        'user_id': session['user_id']
    }
    Recipe.save(data)
    return redirect('/dashboard')

# create a route to display the form to edit a recipe with Recipe.update class method, make it prepopulate the form with the recipe's information

@app.route('/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect ('/logout_session')

    data = {
        'id': id
    }
    recipe = Recipe.get_one(data)
    return render_template('edit_recipe.html', recipe = recipe)
    
@app.route('/recipes/update', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect ('/logout_session')
    else:
        data = {
            'id': request.form['id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date': request.form['date'],
            'under': request.form['under']
        }
        print(f"id is: {request.form['id']}")
        Recipe.update(data)
        return redirect('/dashboard')
    
# create a route to delete a recipe with Recipe.delete class method

@app.route('/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect ('/logout_session')
    else:
        data = {
            'id': id
        }
        Recipe.delete(data)
        return redirect('/dashboard')
    
# create a route to display a recipe with Recipe.get_one class method

@app.route('/view/<int:recipe_id>/<int:owner_id>')
def show_recipe(recipe_id, owner_id):
    if 'user_id' not in session:
        return redirect ('/logout_session')
    else:
        recipe_data = {
            'id': recipe_id
        }
        owner_data = {
            'id': owner_id
        }
        print(f"id of user posted by is: {owner_id}")
        recipe = Recipe.get_one(recipe_data)
        user = User.get_user(owner_data)
        return render_template('view_recipe.html', recipe = recipe, user = user)
    

    

