from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under = data['under']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, under, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under)s, %(user_id)s);"
        return connectToMySQL('recipe').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipe').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('recipe').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, under = %(under)s WHERE id = %(id)s;"
        return connectToMySQL('recipe').query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipe').query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        # All fields are required, put it in one if statement
        if len(data['name']) == 0 or len(data['description']) == 0 or len(data['instructions']) == 0 or len(data['date']) == 0:
            flash("All fields are required.", "recipe")
            is_valid = False
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.", "recipe")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.", "recipe")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters.", "recipe")
            is_valid = False
        if len(data['date']) == 0:
            flash("Date must be submited", "recipe")
            is_valid = False
        return is_valid


    @classmethod
    def get_all_with_recipes_with_creator(cls):
        query = """
                SELECT * FROM recipes
                JOIN users on recipes.user_id = users.id;
                """
        results = connectToMySQL('recipe').query_db(query)
        recipes = []
        for row in results:
            this_recipe = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_recipe.creator = user.User(user_data)
            # See object as a dictionary
            # print(this_recipe.__dict__)
            # print(this_recipe.creator)
            recipes.append(this_recipe)
        return recipes
